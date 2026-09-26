"""Manual test: Memory Inbox Approve / Ignore actions (Phase 1.3).

Verifies that:
  1. Two pending MemoryRecords can be created directly via the storage module.
  2. Approving one record (simulating the Approve button) sets
     approval_status -> 'approved'.
  3. Ignoring the other record (simulating the Ignore button) sets
     approval_status -> 'rejected'  (NOT deleted -- audit trail is preserved).
  4. After both actions:
       - approved record : approval_status == 'approved'
       - ignored record  : approval_status == 'rejected'
       - pending list    : empty (0 records)
       - no status ever changes except through the explicit update call.

Design note: 'Ignore' sets rejected rather than deleting the record.
This preserves a full audit trail in the SQLite store and is consistent
with the ApprovalStatus enum defined in storage.py.

Usage:
    python test_inbox.py

No API key required. All assertions are against the storage module only.
"""

from __future__ import annotations

import os
import sys

from storage import ApprovalStatus, MemoryStorage


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
# Test
# -----------------------------------------------------------------------

TEST_DB = "test_inbox_memory.db"

RECORD_A_ID = "inbox-test-rec-A"
RECORD_B_ID = "inbox-test-rec-B"


def main() -> None:
    # Start clean
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    store = MemoryStorage(db_path=TEST_DB)

    # ------------------------------------------------------------------
    _section("Step 1: Seed two pending candidates")
    # ------------------------------------------------------------------
    rec_a = store.create(
        content="User's name is Bob and he works at Acme Corp.",
        source_turn_id="turn-inbox-001",
        approval_status=ApprovalStatus.PENDING,
        record_id=RECORD_A_ID,
    )
    rec_b = store.create(
        content="User prefers responses in bullet-point format.",
        source_turn_id="turn-inbox-002",
        approval_status=ApprovalStatus.PENDING,
        record_id=RECORD_B_ID,
    )

    print(f"  Created: [{rec_a.id[:8]}] {rec_a.content!r}  status={rec_a.approval_status.value}")
    print(f"  Created: [{rec_b.id[:8]}] {rec_b.content!r}  status={rec_b.approval_status.value}")

    pending = store.list(approval_status=ApprovalStatus.PENDING)
    assert len(pending) == 2, f"Expected 2 pending records, got {len(pending)}"
    _pass("Two pending records seeded successfully.")

    # ------------------------------------------------------------------
    _section("Step 2: Approve Record A (simulate Approve button)")
    # ------------------------------------------------------------------
    updated_a = store.update(RECORD_A_ID, approval_status=ApprovalStatus.APPROVED)
    print(f"  After approve: [{updated_a.id[:8]}] status={updated_a.approval_status.value}")

    assert updated_a.approval_status == ApprovalStatus.APPROVED, (
        f"Expected APPROVED, got {updated_a.approval_status}"
    )
    # Content must be unchanged
    assert updated_a.content == rec_a.content, "Content must not change on approve"
    _pass("Record A approved correctly.")

    # ------------------------------------------------------------------
    _section("Step 3: Ignore Record B (simulate Ignore button -> sets REJECTED)")
    # ------------------------------------------------------------------
    updated_b = store.update(RECORD_B_ID, approval_status=ApprovalStatus.REJECTED)
    print(f"  After ignore:  [{updated_b.id[:8]}] status={updated_b.approval_status.value}")

    assert updated_b.approval_status == ApprovalStatus.REJECTED, (
        f"Expected REJECTED, got {updated_b.approval_status}"
    )
    # Record still exists in storage (not deleted)
    fetched_b = store.get(RECORD_B_ID)
    assert fetched_b is not None, "Ignored record must still exist in storage (not deleted)"
    assert fetched_b.approval_status == ApprovalStatus.REJECTED
    _pass("Record B ignored (set to 'rejected') correctly. Record still exists in storage.")

    # ------------------------------------------------------------------
    _section("Step 4: Verify final states via storage queries")
    # ------------------------------------------------------------------
    all_records = store.list()
    pending_after = store.list(approval_status=ApprovalStatus.PENDING)
    approved_after = store.list(approval_status=ApprovalStatus.APPROVED)
    rejected_after = store.list(approval_status=ApprovalStatus.REJECTED)

    print(f"  Total records in store : {len(all_records)}")
    print(f"  Pending                : {len(pending_after)}")
    print(f"  Approved               : {len(approved_after)}")
    print(f"  Rejected               : {len(rejected_after)}")

    for r in all_records:
        print(f"    [{r.id[:8]}] {r.content!r:55s}  -> {r.approval_status.value}")

    assert len(pending_after) == 0, (
        f"Expected 0 pending records after approve+ignore, got {len(pending_after)}"
    )
    assert len(approved_after) == 1 and approved_after[0].id == RECORD_A_ID, (
        "Only Record A should be approved"
    )
    assert len(rejected_after) == 1 and rejected_after[0].id == RECORD_B_ID, (
        "Only Record B should be rejected"
    )
    _pass("Final state verified: 0 pending, 1 approved, 1 rejected.")

    # ------------------------------------------------------------------
    _section("Step 5: Confirm no silent status changes (re-read from disk)")
    # ------------------------------------------------------------------
    # Open a fresh storage instance (new connection) to confirm persistence
    store2 = MemoryStorage(db_path=TEST_DB)
    a_check = store2.get(RECORD_A_ID)
    b_check = store2.get(RECORD_B_ID)

    assert a_check.approval_status == ApprovalStatus.APPROVED, (
        f"Record A should still be APPROVED after re-open, got {a_check.approval_status}"
    )
    assert b_check.approval_status == ApprovalStatus.REJECTED, (
        f"Record B should still be REJECTED after re-open, got {b_check.approval_status}"
    )
    _pass("Persisted states confirmed on fresh connection.")

    # Cleanup
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    _section("SUMMARY")
    print("  All Memory Inbox tests passed successfully!\n")


if __name__ == "__main__":
    main()
