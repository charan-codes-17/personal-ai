"""Test: Memory Extraction Pipeline (Phase 1.2).

Runs two cases against the live Nemotron Nano/Super model:

  Case 1 -- FACT:    A message that clearly contains a memorable personal fact.
             Expected: candidate extracted, pending record stored.

  Case 2 -- NON-FACT: A message that is ephemeral filler with nothing to remember.
             Expected: no candidate, no record stored (valid / expected outcome).

Usage:
    python test_extraction.py

Prerequisites:
    NEBIUS_API_KEY must be set in the environment or .env file.
"""

from __future__ import annotations

import logging
import os
import sys

from storage import ApprovalStatus, MemoryStorage
from memory_extraction import extract_and_store_pending, extract_memory_candidate
from nebius_smoke_test import load_env_file

# -----------------------------------------------------------------------
# Logging: show INFO-level messages so extraction decisions are visible
# -----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

SEPARATOR = "=" * 68


def _section(title: str) -> None:
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def _pass(msg: str) -> None:
    print(f"  [PASS] {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")
    sys.exit(1)


# -----------------------------------------------------------------------
# Test cases
# -----------------------------------------------------------------------

FACT_MESSAGE = (
    "By the way, my name is Alice and I am a software engineer based in Berlin. "
    "I am allergic to penicillin."
)

NON_FACT_MESSAGE = "ok thanks"


def test_fact_case(api_key: str, store: MemoryStorage) -> None:
    """A message with clear personal facts must produce a pending record."""
    _section("Case 1 — FACT (should produce a pending record)")
    print(f"  Input: {FACT_MESSAGE!r}\n")

    turn_id = "test-turn-fact-001"
    record = extract_and_store_pending(
        user_message=FACT_MESSAGE,
        source_turn_id=turn_id,
        api_key=api_key,
        storage=store,
    )

    if record is None:
        _fail(
            "Expected a pending MemoryRecord for a fact-rich message, but got None. "
            "Check model response and extraction prompt."
        )

    print(f"  Record ID      : {record.id}")
    print(f"  Content        : {record.content!r}")
    print(f"  Source turn    : {record.source_turn_id}")
    print(f"  Status         : {record.approval_status.value}")

    assert record.approval_status == ApprovalStatus.PENDING, (
        f"Expected PENDING status, got {record.approval_status}"
    )
    assert record.source_turn_id == turn_id, (
        f"Expected source_turn_id={turn_id!r}, got {record.source_turn_id!r}"
    )
    assert record.content, "Record content must be a non-empty string"

    # Verify it is actually persisted in the store
    fetched = store.get(record.id)
    assert fetched is not None, "Record not found in storage after creation"
    assert fetched.approval_status == ApprovalStatus.PENDING

    _pass("Fact case: pending record created and persisted correctly.")


def test_non_fact_case(api_key: str, store: MemoryStorage) -> None:
    """A message that is pure filler must NOT produce any record."""
    _section("Case 2 — NON-FACT (should produce nothing)")
    print(f"  Input: {NON_FACT_MESSAGE!r}\n")

    pending_before = store.list(approval_status=ApprovalStatus.PENDING)
    count_before = len(pending_before)

    record = extract_and_store_pending(
        user_message=NON_FACT_MESSAGE,
        source_turn_id="test-turn-nonfact-001",
        api_key=api_key,
        storage=store,
    )

    if record is not None:
        _fail(
            f"Expected None for a filler message, but got a record: "
            f"content={record.content!r}. "
            "The extraction prompt may be too eager. Review the system prompt."
        )

    pending_after = store.list(approval_status=ApprovalStatus.PENDING)
    count_after = len(pending_after)

    assert count_after == count_before, (
        f"Storage grew from {count_before} to {count_after} pending records "
        "after a non-fact message -- nothing should have been stored."
    )

    _pass("Non-fact case: no record created (correct / expected outcome).")


# -----------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------

def main() -> None:
    load_env_file()
    api_key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not api_key:
        print(
            "[CONFIG ERROR] NEBIUS_API_KEY is not set.\n"
            "Set it in your environment or .env file."
        )
        sys.exit(1)

    # Use an isolated test database so we do not pollute the production store
    test_db = "test_extraction_memory.db"
    store = MemoryStorage(db_path=test_db)

    print(f"\nUsing test database: {test_db}")
    print(f"Model: Nemotron Nano/Super (NEBIUS_NANO_MODEL env or default)")

    test_fact_case(api_key=api_key, store=store)
    test_non_fact_case(api_key=api_key, store=store)

    _section("SUMMARY")
    all_pending = store.list(approval_status=ApprovalStatus.PENDING)
    print(f"  Total pending records in test DB: {len(all_pending)}")
    for r in all_pending:
        print(f"    - [{r.id[:8]}...] {r.content!r}  (turn: {r.source_turn_id})")

    print("\n  All extraction tests passed successfully!\n")


if __name__ == "__main__":
    main()
