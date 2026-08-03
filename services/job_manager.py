from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

from config import DB_PATH, JOBS_DIR, OUTPUTS_DIR, ensure_workspace
from services.common import ensure_dir, utc_now_iso


@dataclass(slots=True)
class JobRecord:
    job_id: str
    created_at: str
    updated_at: str
    status: str
    source_type: str
    source_value: str | None
    media_title: str | None
    output_dir: str
    settings_json: str
    error: str | None = None

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)

    def settings(self) -> dict[str, Any]:
        try:
            return json.loads(self.settings_json)
        except json.JSONDecodeError:
            return {}


class JobManager:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        ensure_workspace()
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_value TEXT,
                    media_title TEXT,
                    output_dir TEXT NOT NULL,
                    settings_json TEXT NOT NULL,
                    error TEXT
                )
                """
            )
            conn.commit()

    def create_job(
        self,
        source_type: str,
        source_value: str | None,
        settings: dict[str, Any],
        media_title: str | None = None,
        output_root: Path | None = None,
    ) -> JobRecord:
        job_id = uuid4().hex[:12]
        created_at = utc_now_iso()
        base_output = output_root if output_root is not None else OUTPUTS_DIR
        output_dir = ensure_dir(Path(base_output) / job_id)
        ensure_dir(JOBS_DIR / job_id)
        record = JobRecord(
            job_id=job_id,
            created_at=created_at,
            updated_at=created_at,
            status="queued",
            source_type=source_type,
            source_value=source_value,
            media_title=media_title,
            output_dir=str(output_dir),
            settings_json=json.dumps(settings, ensure_ascii=False),
        )
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO jobs (
                    job_id, created_at, updated_at, status, source_type,
                    source_value, media_title, output_dir, settings_json, error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.job_id,
                    record.created_at,
                    record.updated_at,
                    record.status,
                    record.source_type,
                    record.source_value,
                    record.media_title,
                    record.output_dir,
                    record.settings_json,
                    record.error,
                ),
            )
            conn.commit()
        return record

    def update_job(
        self,
        job_id: str,
        *,
        status: str | None = None,
        media_title: str | None = None,
        error: str | None = None,
        settings: dict[str, Any] | None = None,
    ) -> None:
        updates: list[str] = ["updated_at = ?"]
        values: list[Any] = [utc_now_iso()]
        if status is not None:
            updates.append("status = ?")
            values.append(status)
        if media_title is not None:
            updates.append("media_title = ?")
            values.append(media_title)
        if error is not None:
            updates.append("error = ?")
            values.append(error)
        if settings is not None:
            updates.append("settings_json = ?")
            values.append(json.dumps(settings, ensure_ascii=False))
        values.append(job_id)
        with self._connect() as conn:
            conn.execute(f"UPDATE jobs SET {', '.join(updates)} WHERE job_id = ?", values)
            conn.commit()

    def get_job(self, job_id: str) -> JobRecord | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        if row is None:
            return None
        return JobRecord(**dict(row))

    def list_jobs(self, limit: int = 20) -> list[JobRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [JobRecord(**dict(row)) for row in rows]

    def job_dir(self, job_id: str) -> Path:
        return JOBS_DIR / job_id

    def job_output_dir(self, job_id: str) -> Path:
        job = self.get_job(job_id)
        if job is not None:
            return job.output_path
        return OUTPUTS_DIR / job_id

    def log_path(self, job_id: str) -> Path:
        return self.job_dir(job_id) / "job.log"

    def append_log(self, job_id: str, message: str) -> None:
        ensure_dir(self.job_dir(job_id))
        with self.log_path(job_id).open("a", encoding="utf-8") as handle:
            handle.write(message.rstrip() + "\n")

    def load_log(self, job_id: str) -> str:
        path = self.log_path(job_id)
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")
