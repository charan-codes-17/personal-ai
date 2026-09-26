"""Test script for Phase 1.1 Chat Loop.

Simulates a 3+ turn conversation using chat.py and verifies:
1. Context continuity across turns (referencing prior statements).
2. Proper turn structure: {role, content, timestamp}.
3. Debug logging confirming real Nemotron Nano/Super API calls.
"""

import os
import sys
from datetime import datetime

# Configure UTF-8 output encoding for Windows terminals
if sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import streamlit as st

# Ensure .env is loaded
from nebius_smoke_test import load_env_file, NANO_SUPER_TIER_MODEL
load_env_file()

from chat import (
    init_chat_session,
    add_turn,
    get_conversation_history,
    call_chat_turn,
    ROLE_USER,
    ROLE_ASSISTANT,
)


def run_chat_test():
    api_key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not api_key:
        print("[ERROR] NEBIUS_API_KEY not found in environment.")
        sys.exit(1)

    print("=" * 70)
    print("PHASE 1.1 CHAT LOOP MULTI-TURN VERIFICATION TEST")
    print(f"Target Model: {NANO_SUPER_TIER_MODEL}")
    print("=" * 70)

    # Initialize chat session
    init_chat_session()

    test_turns = [
        # Turn 1: Introduce a specific fact
        "Hello! My favorite programming language is Rust, and my project codename is Project-Falcon.",
        # Turn 2: General question
        "Give me a short one-sentence quote about software engineering.",
        # Turn 3: Context-dependent question referencing Turn 1
        "What is my project codename and favorite programming language that I told you earlier?",
    ]

    for idx, user_text in enumerate(test_turns, start=1):
        print(f"\n--- Turn {idx} [User] ---")
        user_turn = add_turn(ROLE_USER, user_text)
        print(f"User: {user_turn['content']}")
        print(f"Timestamp: {user_turn['timestamp']}")

        # Verify turn structure
        assert "role" in user_turn and user_turn["role"] == ROLE_USER
        assert "content" in user_turn and user_turn["content"] == user_text
        assert "timestamp" in user_turn

        print(f"\n--- Turn {idx} [Calling Nemotron Nano/Super] ---")
        res = call_chat_turn(api_key=api_key)
        assistant_text = res["content"]
        assistant_turn = add_turn(ROLE_ASSISTANT, assistant_text)

        print(f"Assistant: {assistant_turn['content']}")
        print(f"Latency: {res['latency']:.2f}s | Timestamp: {assistant_turn['timestamp']}")

    # Check context retention on Turn 3
    final_response = st.session_state.messages[-1]["content"].lower()
    print("\n" + "=" * 70)
    print("EVALUATING MULTI-TURN CONTEXT RETENTION")
    print("=" * 70)
    print(f"Final turn response: \"{st.session_state.messages[-1]['content']}\"")

    has_falcon = "falcon" in final_response
    has_rust = "rust" in final_response

    print(f"Mentions 'Falcon': {has_falcon}")
    print(f"Mentions 'Rust':   {has_rust}")

    if has_falcon and has_rust:
        print("\n[SUCCESS] Context retention verified! Model recalled facts from 2 turns ago.")
    else:
        print("\n[WARNING] Model response did not contain expected keywords. Please inspect output.")
        sys.exit(1)

    history = get_conversation_history()
    print(f"Total turns in history: {len(history)} (expected: 6)")
    assert len(history) == 6, f"Expected 6 turns, got {len(history)}"

    print("\nAll Phase 1.1 multi-turn chat checks passed successfully!")


if __name__ == "__main__":
    run_chat_test()
