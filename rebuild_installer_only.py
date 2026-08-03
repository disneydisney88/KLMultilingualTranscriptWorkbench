from __future__ import annotations

import build_windows_installer as builder


def main() -> None:
    if not builder.PAYLOAD_ZIP.exists():
        raise FileNotFoundError(
            "Existing app payload is missing. Run build_windows_installer.py for a full build."
        )
    builder.build_installer(builder.PAYLOAD_ZIP)
    destination = builder.copy_to_outputs()
    print(f"Installer ready: {destination}")


if __name__ == "__main__":
    main()
