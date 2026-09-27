"""AppTest verification for Subphase 2.3 — Memory Timeline (BL-06 / FR-003).

Exercises the *actual* button-click code paths in app.py using Streamlit's
AppTest framework.  Each test:
  - Uses an isolated SQLite file (PERSONAL_AI_DB env var) so production
    memory.db is never touched.
  - Seeds records *before* the AppTest run (same DB the app will open).
  - Clicks real widget keys and verifies outcomes with a fresh storage query
    (different MemoryStorage connection — confirms storage persistence, not
    just rendered state).

Three checks:
  CHECK 1 — Edit: click Edit, enter new text, click Save, confirm the change
             is in storage via a fresh DB query.
  CHECK 2 — Delete: click Delete, click Confirm Delete, confirm the record is
             gone from storage entirely (not just missing from the page).
  CHECK 3 — Inbox regression: seed a pending record, confirm Approve and
             Ignore buttons still exist after the tab restructure.
"""

from __future__ import annotations

import os
import sys
import tempfile
import uuid

# Windows: force UTF-8 output so emoji in widget labels don't crash the runner.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from streamlit.testing.v1 import AppTest

from storage import ApprovalStatus, MemoryStorage

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
SEP = "=" * 68


def section(title: str) -> None:
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)


def ok(msg: str) -> None:
    print(f"  [PASS] {msg}")


def fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")
    sys.exit(1)


def dump_buttons(at: AppTest) -> None:
    """Print all visible button keys/labels for debugging."""
    print("  Visible buttons:")
    for b in at.button:
        try:
            print(f"    key={b.key!r:45s} label={b.label!r}")
        except Exception:
            print(f"    key={b.key!r}")


def dump_textareas(at: AppTest) -> None:
    print("  Visible text_areas:")
    for ta in at.text_area:
        print(f"    key={ta.key!r}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

APP_PATH = os.path.join(os.path.dirname(__file__), "app.py")


def run_tests() -> None:
    # Use one isolated DB for all checks so seeded records coexist safely.
    db_file = tempfile.mktemp(suffix="_timeline_apptest.db")
    os.environ["PERSONAL_AI_DB"] = db_file

    # Seed DB *before* any AppTest run (app opens the same path).
    seed_store = MemoryStorage(db_file)

    # -------------------------------------------------------------------------
    # CHECK 1 — Edit: button click → text_area → Save → confirm storage change
    # -------------------------------------------------------------------------
    section("CHECK 1 — Edit: click Edit, enter new text, click Save, verify in storage")

    rec_edit_id = f"edit-test-{uuid.uuid4()}"
    original_text = "I use PyTorch for all deep learning work"
    edited_text   = "I use PyTorch AND JAX for all deep learning work"

    seed_store.create(
        content=original_text,
        source_turn_id="turn-edit-001",
        approval_status=ApprovalStatus.APPROVED,
        record_id=rec_edit_id,
    )
    print(f"  Seeded approved record: {rec_edit_id[:8]}... -> {original_text!r}")

    # --- Boot app and verify initial view-mode render ---
    at = AppTest.from_file(APP_PATH, default_timeout=30)
    at.run()
    if at.exception:
        fail(f"App raised exception on initial load: {at.exception}")

    print("  App loaded. Scanning for Edit button...")
    edit_btn_key = f"edit_start_{rec_edit_id}"
    if not at.button(key=edit_btn_key):
        dump_buttons(at)
        fail(f"Edit button not found with key {edit_btn_key!r}")
    ok(f"Edit button found (key={edit_btn_key!r})")

    # --- Click Edit: app reruns, text_area appears in edit mode ---
    at.button(key=edit_btn_key).click().run()
    if at.exception:
        fail(f"Exception after clicking Edit: {at.exception}")

    textarea_key = f"textarea_{rec_edit_id}"
    print(f"  Scanning for text_area with key={textarea_key!r}...")
    if not at.text_area(key=textarea_key):
        dump_textareas(at)
        fail(f"text_area not found after clicking Edit (key={textarea_key!r})")
    ok("text_area appeared in edit mode")

    # --- Enter new text and click Save ---
    at.text_area(key=textarea_key).set_value(edited_text)
    save_key = f"save_{rec_edit_id}"
    if not at.button(key=save_key):
        dump_buttons(at)
        fail(f"Save button not found (key={save_key!r})")
    at.button(key=save_key).click().run()
    if at.exception:
        fail(f"Exception after clicking Save: {at.exception}")
    ok("Save button clicked; app re-ran")

    # --- Fresh storage query (new connection) to verify persistence ---
    verify_store = MemoryStorage(db_file)
    updated_rec = verify_store.get(rec_edit_id)
    if updated_rec is None:
        fail("Record not found in storage after Save")
    print(f"  Storage content after Save: {updated_rec.content!r}")
    if updated_rec.content != edited_text:
        fail(
            f"Content did NOT change in storage.\n"
            f"  Expected: {edited_text!r}\n"
            f"  Got:      {updated_rec.content!r}"
        )
    ok(f"Storage reflects new content after Save: {updated_rec.content!r}")

    # -------------------------------------------------------------------------
    # CHECK 2 — Delete: button click → Confirm Delete → confirm gone from storage
    # -------------------------------------------------------------------------
    section("CHECK 2 — Delete: click Delete, confirm, verify record gone from storage")

    rec_del_id = f"del-test-{uuid.uuid4()}"
    del_text = "My hackathon deadline is October 30, 2026"

    seed_store.create(
        content=del_text,
        source_turn_id="turn-del-001",
        approval_status=ApprovalStatus.APPROVED,
        record_id=rec_del_id,
    )
    print(f"  Seeded approved record: {rec_del_id[:8]}... -> {del_text!r}")

    # Re-boot the app (fresh run so the new record appears in the Timeline)
    at2 = AppTest.from_file(APP_PATH, default_timeout=30)
    at2.run()
    if at2.exception:
        fail(f"App raised exception on load: {at2.exception}")

    del_btn_key = f"del_{rec_del_id}"
    if not at2.button(key=del_btn_key):
        dump_buttons(at2)
        fail(f"Delete button not found (key={del_btn_key!r})")
    ok(f"Delete button found (key={del_btn_key!r})")

    # --- Click Delete: arms the confirm prompt ---
    at2.button(key=del_btn_key).click().run()
    if at2.exception:
        fail(f"Exception after clicking Delete: {at2.exception}")

    confirm_btn_key = f"del_confirm_{rec_del_id}"
    if not at2.button(key=confirm_btn_key):
        dump_buttons(at2)
        fail(f"Confirm Delete button not found after arming (key={confirm_btn_key!r})")
    ok("Confirm Delete button appeared after first click")

    # --- Click Confirm Delete ---
    at2.button(key=confirm_btn_key).click().run()
    if at2.exception:
        fail(f"Exception after clicking Confirm Delete: {at2.exception}")
    ok("Confirm Delete clicked; app re-ran")

    # --- Fresh storage query: record must be entirely gone ---
    verify_store2 = MemoryStorage(db_file)
    gone = verify_store2.get(rec_del_id)
    if gone is not None:
        fail(
            f"Record still in storage after Confirm Delete!\n"
            f"  ID: {rec_del_id}\n  Content: {gone.content!r}\n  Status: {gone.approval_status}"
        )
    ok("Record is gone from storage — not just hidden in UI")

    # Also confirm it doesn't appear in the approved list
    all_approved = [r.id for r in verify_store2.list(ApprovalStatus.APPROVED)]
    if rec_del_id in all_approved:
        fail(f"Deleted record still appears in list(APPROVED): {all_approved}")
    ok("Deleted record absent from storage list(APPROVED) query")

    # -------------------------------------------------------------------------
    # CHECK 3 — Inbox regression: pending record shows Approve + Ignore buttons
    # -------------------------------------------------------------------------
    section("CHECK 3 — Inbox regression: pending record has Approve/Ignore buttons")

    rec_pend_id = f"pend-test-{uuid.uuid4()}"
    pend_text = "User prefers Python over JavaScript for backend work"

    seed_store.create(
        content=pend_text,
        source_turn_id="turn-pend-001",
        approval_status=ApprovalStatus.PENDING,
        record_id=rec_pend_id,
    )
    print(f"  Seeded pending record: {rec_pend_id[:8]}... -> {pend_text!r}")

    at3 = AppTest.from_file(APP_PATH, default_timeout=30)
    at3.run()
    if at3.exception:
        fail(f"App raised exception on load: {at3.exception}")

    approve_key = f"approve_{rec_pend_id}"
    ignore_key  = f"ignore_{rec_pend_id}"

    approve_found = bool(at3.button(key=approve_key))
    ignore_found  = bool(at3.button(key=ignore_key))

    print(f"  Approve button (key={approve_key!r}) found: {approve_found}")
    print(f"  Ignore  button (key={ignore_key!r}) found: {ignore_found}")

    if not approve_found:
        dump_buttons(at3)
        fail(f"Approve button missing — Inbox broken after tab restructure")
    ok("Approve button present for pending record")

    if not ignore_found:
        dump_buttons(at3)
        fail(f"Ignore button missing — Inbox broken after tab restructure")
    ok("Ignore button present for pending record")

    # --- Click Approve and verify storage reflects APPROVED ---
    at3.button(key=approve_key).click().run()
    if at3.exception:
        fail(f"Exception after clicking Approve: {at3.exception}")

    verify_store3 = MemoryStorage(db_file)
    pend_rec = verify_store3.get(rec_pend_id)
    if pend_rec is None:
        fail("Pending record not found in storage after Approve click")
    if pend_rec.approval_status != ApprovalStatus.APPROVED:
        fail(
            f"Record status not updated after Approve click.\n"
            f"  Expected: approved\n"
            f"  Got:      {pend_rec.approval_status.value}"
        )
    ok(f"Approve button works: status is now {pend_rec.approval_status.value!r} in storage")

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------
    try:
        os.unlink(db_file)
    except Exception:
        pass

    section("SUMMARY — Subphase 2.3 AppTest Verification")
    print("  CHECK 1 (Edit)   PASSED — storage updated via Save button click")
    print("  CHECK 2 (Delete) PASSED — record gone from storage via Confirm Delete click")
    print("  CHECK 3 (Inbox)  PASSED — Approve/Ignore buttons present and functional after tab restructure")
    print()


if __name__ == "__main__":
    run_tests()
