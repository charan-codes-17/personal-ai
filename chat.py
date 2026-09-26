"""Personal AI - Conversation Turn Handling & Chat Management.

Phase 1.1: Core AI Chat Loop.
Maintains session state conversation turns {role, content, timestamp},
formats running context, and invokes Nemotron Nano/Super on Nebius Token Factory.
"""

from datetime import datetime, timezone
import logging
import uuid
from typing import Any, Dict, List, Optional
import streamlit as st

from nebius_smoke_test import (
    NANO_SUPER_TIER_MODEL,
    call_nemotron_nano_super,
    NebiusAPIError,
)

logger = logging.getLogger(__name__)

# Standard roles
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"


def get_or_create_session_id() -> str:
    """Retrieve the current session identifier or initialize a new one."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session-{uuid.uuid4().hex[:8]}"
    return st.session_state.session_id


def init_chat_session() -> None:
    """Initialize conversation history and session attributes in st.session_state."""
    get_or_create_session_id()
    if "messages" not in st.session_state:
        st.session_state.messages = []


def add_turn(role: str, content: str) -> Dict[str, str]:
    """Append a turn {role, content, timestamp} to session history.

    Timestamp is formatted as UTC ISO-8601 string.
    """
    turn = {
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    st.session_state.messages.append(turn)
    return turn


def clear_chat_history() -> None:
    """Reset conversational history and create a new session id."""
    st.session_state.messages = []
    st.session_state.session_id = f"session-{uuid.uuid4().hex[:8]}"


def get_conversation_history() -> List[Dict[str, str]]:
    """Return all conversation turns from session state."""
    return st.session_state.get("messages", [])


def format_messages_for_api(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Format stored session turns into the API payload schema [{'role': ..., 'content': ...}]."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in messages
        if m.get("role") in (ROLE_USER, ROLE_ASSISTANT, ROLE_SYSTEM)
    ]


def call_chat_turn(
    api_key: str,
    messages: Optional[List[Dict[str, Any]]] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    """Invoke Nemotron Nano/Super model with the full running history as context.

    Emits prominent debug logs confirming a real API call (not a placeholder).
    Raises NebiusAPIError or Exception on failure.
    """
    if messages is None:
        messages = get_conversation_history()

    api_messages = format_messages_for_api(messages)
    session_id = st.session_state.get("session_id", "unknown-session")
    turn_count = len(api_messages)

    # Required debug confirmation: real Nano/Super API call
    debug_banner = (
        f"[REAL API CALL] Invoking Nemotron Nano/Super (Model: '{NANO_SUPER_TIER_MODEL}') | "
        f"Session: '{session_id}' | Turns in Context: {turn_count}"
    )
    print(debug_banner)
    logger.info(debug_banner)

    response = call_nemotron_nano_super(
        api_key=api_key,
        messages=api_messages,
        max_tokens=max_tokens,
        temperature=temperature,
        raise_on_error=True,
    )

    if not response or not response.get("content"):
        raise NebiusAPIError("Nemotron Nano/Super returned an empty response.")

    log_success = (
        f"[REAL API RESPONSE] Received from '{response.get('model')}' in {response.get('latency', 0):.2f}s | "
        f"Completion Tokens: {response.get('usage', {}).get('completion_tokens', 'N/A')}"
    )
    print(log_success)
    logger.info(log_success)

    return response
