"""Persistent SQLite storage module for chat app memory records."""

from __future__ import annotations

import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Generator, Optional, Union


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class MemoryRecord:
    id: str
    content: str
    source_turn_id: str
    timestamp: datetime
    approval_status: ApprovalStatus

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "source_turn_id": self.source_turn_id,
            "timestamp": self.timestamp.isoformat(),
            "approval_status": self.approval_status.value,
        }


def _parse_approval_status(status: Union[ApprovalStatus, str]) -> ApprovalStatus:
    if isinstance(status, ApprovalStatus):
        return status
    try:
        return ApprovalStatus(status.lower())
    except (ValueError, AttributeError):
        valid = [s.value for s in ApprovalStatus]
        raise ValueError(f"Invalid approval_status '{status}'. Must be one of: {valid}")


class MemoryStorage:
    """SQLite-backed persistent store for MemoryRecords."""

    def __init__(self, db_path: Union[str, Path] = "memory.db"):
        self.db_path = str(db_path)
        self._init_db()

    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_records (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    source_turn_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    approval_status TEXT NOT NULL CHECK(approval_status IN ('pending', 'approved', 'rejected'))
                )
                """
            )

    def create(
        self,
        content: str,
        source_turn_id: str,
        approval_status: Union[ApprovalStatus, str] = ApprovalStatus.PENDING,
        record_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ) -> MemoryRecord:
        """Create and persist a new memory record."""
        rec_id = record_id or str(uuid.uuid4())
        rec_time = timestamp or datetime.now(timezone.utc)
        parsed_status = _parse_approval_status(approval_status)

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO memory_records (id, content, source_turn_id, timestamp, approval_status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    rec_id,
                    content,
                    source_turn_id,
                    rec_time.isoformat(),
                    parsed_status.value,
                ),
            )

        return MemoryRecord(
            id=rec_id,
            content=content,
            source_turn_id=source_turn_id,
            timestamp=rec_time,
            approval_status=parsed_status,
        )

    def get(self, record_id: str) -> Optional[MemoryRecord]:
        """Fetch a single memory record by its id."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT id, content, source_turn_id, timestamp, approval_status FROM memory_records WHERE id = ?",
                (record_id,),
            ).fetchone()

        if row is None:
            return None

        return MemoryRecord(
            id=row["id"],
            content=row["content"],
            source_turn_id=row["source_turn_id"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            approval_status=ApprovalStatus(row["approval_status"]),
        )

    def list(
        self,
        approval_status: Optional[Union[ApprovalStatus, str]] = None,
    ) -> list[MemoryRecord]:
        """List memory records, optionally filtered by approval status."""
        query = "SELECT id, content, source_turn_id, timestamp, approval_status FROM memory_records"
        params: tuple = ()

        if approval_status is not None:
            parsed_status = _parse_approval_status(approval_status)
            query += " WHERE approval_status = ?"
            params = (parsed_status.value,)

        query += " ORDER BY timestamp ASC"

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()

        return [
            MemoryRecord(
                id=row["id"],
                content=row["content"],
                source_turn_id=row["source_turn_id"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                approval_status=ApprovalStatus(row["approval_status"]),
            )
            for row in rows
        ]

    def update(
        self,
        record_id: str,
        content: Optional[str] = None,
        approval_status: Optional[Union[ApprovalStatus, str]] = None,
        source_turn_id: Optional[str] = None,
    ) -> Optional[MemoryRecord]:
        """Update fields of an existing record and return the updated record."""
        updates: list[str] = []
        params: list = []

        if content is not None:
            updates.append("content = ?")
            params.append(content)

        if approval_status is not None:
            parsed_status = _parse_approval_status(approval_status)
            updates.append("approval_status = ?")
            params.append(parsed_status.value)

        if source_turn_id is not None:
            updates.append("source_turn_id = ?")
            params.append(source_turn_id)

        if not updates:
            return self.get(record_id)

        params.append(record_id)
        query = f"UPDATE memory_records SET {', '.join(updates)} WHERE id = ?"

        with self._get_connection() as conn:
            cursor = conn.execute(query, tuple(params))
            if cursor.rowcount == 0:
                return None

        return self.get(record_id)

    def delete(self, record_id: str) -> bool:
        """Delete a record by id. Returns True if a record was deleted, False otherwise."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM memory_records WHERE id = ?",
                (record_id,),
            )
            return cursor.rowcount > 0


_default_storage: Optional[MemoryStorage] = None


def get_default_storage() -> MemoryStorage:
    global _default_storage
    if _default_storage is None:
        _default_storage = MemoryStorage()
    return _default_storage


def create(*args, **kwargs) -> MemoryRecord:
    return get_default_storage().create(*args, **kwargs)


def get(record_id: str) -> Optional[MemoryRecord]:
    return get_default_storage().get(record_id)


def list_records(
    approval_status: Optional[Union[ApprovalStatus, str]] = None,
) -> list[MemoryRecord]:
    return get_default_storage().list(approval_status=approval_status)


def update(*args, **kwargs) -> Optional[MemoryRecord]:
    return get_default_storage().update(*args, **kwargs)


def delete(record_id: str) -> bool:
    return get_default_storage().delete(record_id)

