"""Personal AI - Streamlit Application.

Subphase 2.3 — Memory Timeline (BL-06):
  A new 'Memory Timeline' tab lists all approval_status='approved' records,
  most recent first. Each record has inline Edit and Delete controls.
  Edit updates content in storage via _store.update(); Delete calls
  _store.delete() — a hard removal from the DB, not a UI hide.

Subphase 2.2 — Memory Inbox / Staged Approval (BL-05):
  Sidebar section listing all pending MemoryRecords extracted from past turns.
  Each record has Approve (sets approval_status='approved') and Ignore (sets
  approval_status='rejected') buttons. Status changes only happen through
  explicit user actions. 'Ignore' sets rejected rather than deleting,
  preserving the full audit trail in storage.

Subphase 2.1 — Memory Extraction (BL-04):
  After each user turn, prompts Nemotron Nano/Super to extract any
  memory-worthy fact/preference/decision and stores it as a pending
  MemoryRecord via the Phase 0 storage module.

Phase 1.1 — Core AI Chat Loop (BL-03):
  Maintains session state conversation turns {role, content, timestamp},
  formats running context, and invokes Nemotron Nano/Super on Nebius Token
  Factory. Preserves Phase 0.3 connectivity diagnostics."""

import logging
import os
from typing import Optional
import streamlit as st

# Verify clean imports of project modules inside the Streamlit runtime
import storage
from storage import ApprovalStatus, MemoryStorage
from memory_extraction import extract_and_store_pending
from nebius_smoke_test import (
    DEFAULT_BASE_URL,
    ULTRA_TIER_MODEL,
    NANO_SUPER_TIER_MODEL,
    call_nemotron_ultra,
    call_nemotron_nano_super,
    NebiusAPIError,
    load_env_file,
)
from chat import (
    init_chat_session,
    get_or_create_session_id,
    add_turn,
    clear_chat_history,
    get_conversation_history,
    call_chat_turn,
    ROLE_USER,
    ROLE_ASSISTANT,
)

logger = logging.getLogger(__name__)

# Shared storage instance.
# PERSONAL_AI_DB env var lets tests redirect to an isolated DB file
# without touching the production memory.db.
_db_path = os.environ.get("PERSONAL_AI_DB", "memory.db")
_store = MemoryStorage(_db_path)


def get_nebius_api_key() -> Optional[str]:
    """Retrieve Nebius API key from st.secrets (cloud) or os.environ / .env (local dev)."""
    # 1. Check Streamlit secrets first (for Streamlit Community Cloud)
    try:
        if "NEBIUS_API_KEY" in st.secrets:
            val = st.secrets["NEBIUS_API_KEY"]
            if val and str(val).strip():
                return str(val).strip()
    except Exception:
        # Gracefully handle when secrets are not configured
        pass

    # 2. Check environment variable
    key = os.environ.get("NEBIUS_API_KEY")
    if key and key.strip():
        return key.strip()

    # 3. Fall back to loading from .env if present
    load_env_file()
    key = os.environ.get("NEBIUS_API_KEY")
    if key and key.strip():
        return key.strip()

    return None


# Configure Streamlit page
st.set_page_config(
    page_title="Personal AI - Chat",
    page_icon="🧠",
    layout="centered",
)

# Initialize chat session state (session_id, messages list)
init_chat_session()
session_id = get_or_create_session_id()
conversation = get_conversation_history()

# --- Sidebar: Session Management, Memory Inbox & Phase 0.3 Diagnostics ---
with st.sidebar:
    st.header("⚙️ System & Session")
    pending_records = _store.list(approval_status=ApprovalStatus.PENDING)
    st.caption(f"**Session ID:** `{session_id}`")
    st.caption(f"**Turns in Memory:** {len(conversation)}")
    st.caption(f"**Chat Model:** `{NANO_SUPER_TIER_MODEL}`")
    st.caption(f"**Pending memories:** {len(pending_records)}")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        clear_chat_history()
        st.rerun()

    st.divider()

    # ------------------------------------------------------------------
    # Memory Inbox
    # ------------------------------------------------------------------
    inbox_label = (
        f"🧠 Memory Inbox ({len(pending_records)} pending)"
        if pending_records
        else "🧠 Memory Inbox (empty)"
    )
    with st.expander(inbox_label, expanded=bool(pending_records)):
        st.caption(
            "Facts and preferences extracted from your conversation. "
            "**Approve** to remember them, **Ignore** to discard."
        )
        st.caption(
            "_Note: Ignore sets status to `rejected` (not deleted) — "
            "preserving the full audit trail in storage._"
        )

        if not pending_records:
            st.info("No pending memories right now. Keep chatting!")
        else:
            for rec in pending_records:
                short_id = rec.id[:8]
                st.markdown(f"**{rec.content}**")
                st.caption(
                    f"Turn: `{rec.source_turn_id}` · "
                    f"ID: `{short_id}…` · "
                    f"{rec.timestamp.strftime('%Y-%m-%d %H:%M UTC')}"
                )
                col_approve, col_ignore = st.columns(2)
                with col_approve:
                    if st.button(
                        "✅ Approve",
                        key=f"approve_{rec.id}",
                        use_container_width=True,
                        type="primary",
                    ):
                        _store.update(rec.id, approval_status=ApprovalStatus.APPROVED)
                        st.rerun()
                with col_ignore:
                    if st.button(
                        "🚫 Ignore",
                        key=f"ignore_{rec.id}",
                        use_container_width=True,
                    ):
                        # Sets to 'rejected' — preserves audit trail, not deleted
                        _store.update(rec.id, approval_status=ApprovalStatus.REJECTED)
                        st.rerun()
                st.divider()

    st.divider()

    # Retain Phase 0.3 button & connectivity verification
    with st.expander("⚡ Phase 0.3: Model Connectivity Check", expanded=False):
        st.markdown(
            "Verifies raw connectivity to both Nemotron Ultra and Nano/Super "
            "model tiers on Nebius Token Factory."
        )
        if st.button("Test Nebius Connectivity", key="test_connectivity_btn", type="primary", use_container_width=True):
            api_key = get_nebius_api_key()

            if not api_key:
                st.error(
                    "Nebius API key not found. Please set `NEBIUS_API_KEY` in `.env` "
                    "or configure `st.secrets` for Streamlit Cloud."
                )
            else:
                with st.spinner("Querying Nemotron Ultra and Nemotron Nano/Super models..."):
                    # Call Nemotron Ultra
                    try:
                        ultra_res = call_nemotron_ultra(api_key=api_key)
                        st.subheader(f"Ultra-tier ({ULTRA_TIER_MODEL})")
                        st.success(
                            f"**Latency:** {ultra_res['latency']:.2f}s\n\n"
                            f"**Response:** {ultra_res['content']}"
                        )
                    except Exception as e:
                        st.error(f"Ultra-tier model failed: {e}")

                    # Call Nemotron Nano/Super
                    try:
                        nano_res = call_nemotron_nano_super(api_key=api_key)
                        st.subheader(f"Nano/Super-tier ({NANO_SUPER_TIER_MODEL})")
                        st.success(
                            f"**Latency:** {nano_res['latency']:.2f}s\n\n"
                            f"**Response:** {nano_res['content']}"
                        )
                    except Exception as e:
                        st.error(f"Nano/Super-tier model failed: {e}")


# ---------------------------------------------------------------------------
# Main Area: Tabs — Chat | Memory Timeline
# ---------------------------------------------------------------------------
st.title("Personal AI")
st.caption(
    "Multi-turn conversational assistant powered by NVIDIA Nemotron Nano/Super via Nebius Token Factory."
)

tab_chat, tab_timeline = st.tabs(["💬 Chat", "🕐 Memory Timeline"])

# ===========================================================================
# TAB 1 — Chat
# ===========================================================================
with tab_chat:
    # Display existing chat history
    for turn in conversation:
        role = turn.get("role", ROLE_USER)
        content = turn.get("content", "")
        with st.chat_message(role):
            st.markdown(content)

    # Chat input bar
    prompt = st.chat_input("Type your message here...")

    if prompt:
        api_key = get_nebius_api_key()

        if not api_key:
            st.error(
                "Nebius API key not found. Please configure `NEBIUS_API_KEY` in `.env` "
                "or `st.secrets` to continue."
            )
        else:
            # 1. Record and render user turn
            turn = add_turn(ROLE_USER, prompt)
            turn_id = session_id  # use session_id as the turn anchor
            with st.chat_message(ROLE_USER):
                st.markdown(prompt)

            # 2. Render thinking indicator and invoke model
            with st.chat_message(ROLE_ASSISTANT):
                with st.spinner("Nemotron is thinking..."):
                    try:
                        response = call_chat_turn(api_key=api_key)
                        assistant_content = response["content"]
                        # 3. Record assistant turn in session history
                        add_turn(ROLE_ASSISTANT, assistant_content)
                        st.markdown(assistant_content)
                    except NebiusAPIError as e:
                        st.error(f"**Nebius API Error ({e.status_code or 'Failure'}):** {e}")
                    except Exception as e:
                        st.error(f"**Error invoking Nemotron Nano/Super:** {str(e)}")

            # 4. Memory extraction: run silently after each user turn.
            #    Failures are intentionally swallowed -- this step must never
            #    disrupt the chat experience.
            try:
                mem_record = extract_and_store_pending(
                    user_message=prompt,
                    source_turn_id=turn_id,
                    api_key=api_key,
                    storage=_store,
                )
                if mem_record:
                    logger.info(
                        "[MemoryExtraction] Stored pending record %s for session %s",
                        mem_record.id,
                        session_id,
                    )
            except Exception as _mem_exc:  # noqa: BLE001
                logger.warning(
                    "[MemoryExtraction] Extraction step failed (non-fatal): %s", _mem_exc
                )

# ===========================================================================
# TAB 2 — Memory Timeline (Subphase 2.3 / BL-06 / FR-003)
# ===========================================================================
with tab_timeline:
    st.subheader("🕐 Memory Timeline")
    st.caption(
        "All approved memories, most recent first. "
        "Use **Edit** to correct a record's content (persists to storage). "
        "Use **Delete** to permanently remove it from storage — not just from this view."
    )

    # Fetch approved records, most recent first
    approved_records = list(
        reversed(_store.list(approval_status=ApprovalStatus.APPROVED))
    )

    if not approved_records:
        st.info(
            "No approved memories yet. Chat with the assistant, then approve "
            "candidates from the **Memory Inbox** in the sidebar."
        )
    else:
        st.caption(f"**{len(approved_records)} approved record(s)**")

        for rec in approved_records:
            short_id = rec.id[:8]

            # Track whether this record is currently in edit mode.
            edit_key = f"editing_{rec.id}"
            if edit_key not in st.session_state:
                st.session_state[edit_key] = False

            with st.container(border=True):
                # Header row: timestamp + id
                st.caption(
                    f"🕐 {rec.timestamp.strftime('%Y-%m-%d %H:%M UTC')}  ·  "
                    f"ID: `{short_id}…`"
                )

                # ---------------------------------------------------------
                # VIEW MODE
                # ---------------------------------------------------------
                if not st.session_state[edit_key]:
                    st.markdown(rec.content)

                    col_edit_btn, col_del_btn = st.columns(2)
                    with col_edit_btn:
                        if st.button(
                            "✏️ Edit",
                            key=f"edit_start_{rec.id}",
                            use_container_width=True,
                        ):
                            st.session_state[edit_key] = True
                            # Seed the draft with the current content
                            st.session_state[f"draft_{rec.id}"] = rec.content
                            st.rerun()

                    with col_del_btn:
                        # Two-step delete: first press arms the confirm prompt,
                        # second press executes the hard delete from storage.
                        confirm_key = f"confirm_delete_{rec.id}"
                        if confirm_key not in st.session_state:
                            st.session_state[confirm_key] = False

                        if not st.session_state[confirm_key]:
                            if st.button(
                                "🗑️ Delete",
                                key=f"del_{rec.id}",
                                use_container_width=True,
                            ):
                                st.session_state[confirm_key] = True
                                st.rerun()
                        else:
                            # Armed state — show confirm/cancel
                            st.warning("Permanently delete this record from storage?")
                            col_yes, col_no = st.columns(2)
                            with col_yes:
                                if st.button(
                                    "✅ Confirm Delete",
                                    key=f"del_confirm_{rec.id}",
                                    use_container_width=True,
                                    type="primary",
                                ):
                                    deleted = _store.delete(rec.id)
                                    if deleted:
                                        st.success(
                                            f"Record `{short_id}…` permanently deleted from storage."
                                        )
                                        logger.info(
                                            "[Timeline] Hard-deleted record %s from storage.",
                                            rec.id,
                                        )
                                    else:
                                        st.error(
                                            f"Delete failed: record `{short_id}…` not found in storage."
                                        )
                                    # Clean up confirm state and refresh
                                    del st.session_state[confirm_key]
                                    st.rerun()
                            with col_no:
                                if st.button(
                                    "↩️ Cancel",
                                    key=f"del_cancel_{rec.id}",
                                    use_container_width=True,
                                ):
                                    st.session_state[confirm_key] = False
                                    st.rerun()

                # ---------------------------------------------------------
                # EDIT MODE
                # ---------------------------------------------------------
                else:
                    draft_key = f"draft_{rec.id}"
                    new_content = st.text_area(
                        "Edit memory content",
                        value=st.session_state.get(draft_key, rec.content),
                        key=f"textarea_{rec.id}",
                        height=100,
                        label_visibility="collapsed",
                    )
                    # Keep draft in sync
                    st.session_state[draft_key] = new_content

                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button(
                            "💾 Save",
                            key=f"save_{rec.id}",
                            use_container_width=True,
                            type="primary",
                        ):
                            stripped = new_content.strip()
                            if not stripped:
                                st.error("Content cannot be empty.")
                            else:
                                updated = _store.update(rec.id, content=stripped)
                                if updated:
                                    st.success("Memory updated in storage.")
                                    logger.info(
                                        "[Timeline] Updated record %s content in storage.",
                                        rec.id,
                                    )
                                else:
                                    st.error(
                                        f"Update failed: record `{short_id}…` not found in storage."
                                    )
                                # Exit edit mode and refresh
                                st.session_state[edit_key] = False
                                if draft_key in st.session_state:
                                    del st.session_state[draft_key]
                                st.rerun()

                    with col_cancel:
                        if st.button(
                            "↩️ Cancel",
                            key=f"cancel_{rec.id}",
                            use_container_width=True,
                        ):
                            st.session_state[edit_key] = False
                            if draft_key in st.session_state:
                                del st.session_state[draft_key]
                            st.rerun()