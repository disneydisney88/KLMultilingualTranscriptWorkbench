from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse, urlunparse


ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "169.254.169.254",
}


def _resolve_host(hostname: str) -> list[str]:
    addresses: list[str] = []
    try:
        for family, _, _, _, sockaddr in socket.getaddrinfo(hostname, None):
            if family in (socket.AF_INET, socket.AF_INET6):
                addresses.append(sockaddr[0])
    except socket.gaierror as exc:
        raise ValueError(f"?⊥?閫??銝餅?嚗hostname}") from exc
    return addresses


def _is_public_ip(host: str) -> bool:
    ip = ipaddress.ip_address(host)
    return not (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_public_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError("?芣??http ??https URL")
    if not parsed.hostname:
        raise ValueError("URL 蝻箏?銝餅??迂")

    hostname = parsed.hostname.lower()
    if hostname in BLOCKED_HOSTNAMES or hostname.endswith(".local"):
        raise ValueError("URL 銝餅?銝?閮?)

    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        resolved = _resolve_host(hostname)
        for address in resolved:
            if not _is_public_ip(address):
                raise ValueError("URL 閫???啣?冽?靽?雿?嚗歇?餅?")
    else:
        if not _is_public_ip(str(ip)):
            raise ValueError("URL ???折?????嚗歇?餅?")

    if parsed.fragment:
        parsed = parsed._replace(fragment="")
    return urlunparse(parsed)
