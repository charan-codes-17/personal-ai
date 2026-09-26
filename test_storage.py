"""Test script for memory storage module.

Demonstrates:
1. Creating a memory record
2. Simulating process restart by closing connection and initializing a new MemoryStorage instance
3. Confirming the persisted record is still readable with intact schema and data
4. Testing list, update, and delete operations
"""

import os
from datetime import datetime, timezone
from storage import ApprovalStatus, MemoryStorage


def main():
    test_db_path = "test_memory.db"

    # Clean up any leftover database from previous runs
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    print("=== Step 1: Initialize Storage Session 1 & Create Record ===")
    store_session1 = MemoryStorage(db_path=test_db_path)

    custom_id = "mem-101"
    turn_id = "turn-42"
    content = "User prefers dark mode and concise responses."
    now = datetime.now(timezone.utc)

    created = store_session1.create(
        content=content,
        source_turn_id=turn_id,
        approval_status=ApprovalStatus.PENDING,
        record_id=custom_id,
        timestamp=now,
    )
    print(f"Created Record: {created}")
    assert created.id == custom_id
    assert created.approval_status == ApprovalStatus.PENDING

    # Simulate process restart: drop the session object entirely
    del store_session1
    print("\n[Simulating process restart... All connections closed and objects dropped]\n")

    print("=== Step 2: Initialize Storage Session 2 (New Process Simulation) ===")
    store_session2 = MemoryStorage(db_path=test_db_path)

    # Confirm record is still readable
    retrieved = store_session2.get(custom_id)
    print(f"Retrieved Record after restart: {retrieved}")
    assert retrieved is not None, "Failed to retrieve record after restart!"
    assert retrieved.id == custom_id
    assert retrieved.content == content
    assert retrieved.source_turn_id == turn_id
    assert retrieved.approval_status == ApprovalStatus.PENDING
    assert retrieved.timestamp == now
    print("[OK] Persistence check passed: Record successfully read after restart.")

    print("\n=== Step 3: Test List Functionality ===")
    # Add a second record with approved status
    store_session2.create(
        content="User lives in San Francisco.",
        source_turn_id="turn-45",
        approval_status=ApprovalStatus.APPROVED,
        record_id="mem-102",
    )

    all_records = store_session2.list()
    print(f"All records count: {len(all_records)}")
    assert len(all_records) == 2

    pending_records = store_session2.list(approval_status=ApprovalStatus.PENDING)
    print(f"Pending records count: {len(pending_records)}")
    assert len(pending_records) == 1
    assert pending_records[0].id == "mem-101"

    approved_records = store_session2.list(approval_status="approved")
    print(f"Approved records count: {len(approved_records)}")
    assert len(approved_records) == 1
    assert approved_records[0].id == "mem-102"
    print("[OK] List operations passed.")

    print("\n=== Step 4: Test Update Functionality ===")
    updated = store_session2.update(
        record_id=custom_id,
        approval_status=ApprovalStatus.APPROVED,
        content="User prefers dark mode, compact view, and concise responses.",
    )
    print(f"Updated Record: {updated}")
    assert updated is not None
    assert updated.approval_status == ApprovalStatus.APPROVED
    assert updated.content == "User prefers dark mode, compact view, and concise responses."

    # Verify update persisted
    check_updated = store_session2.get(custom_id)
    assert check_updated.approval_status == ApprovalStatus.APPROVED
    print("[OK] Update operation passed.")

    print("\n=== Step 5: Test Delete Functionality ===")
    deleted = store_session2.delete(custom_id)
    assert deleted is True
    assert store_session2.get(custom_id) is None
    remaining = store_session2.list()
    assert len(remaining) == 1
    assert remaining[0].id == "mem-102"
    print("[OK] Delete operation passed.")

    # Cleanup test db
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    print("\nAll tests passed successfully!")


if __name__ == "__main__":
    main()
