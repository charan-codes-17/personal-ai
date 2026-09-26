"""Memory Extraction Module.

Phase 1.2: After each user turn, prompts Nemotron Nano/Super to judge whether
the turn contains a fact, decision, or preference worth remembering.

If worthy, the model returns a structured JSON candidate:
    {"content": "<short factual statement>", "why": "<brief justification>"}

If nothing is worth remembering, the model returns an empty JSON object {} or
the literal string "NOTHING". Both are valid, expected outcomes — not errors.

Worthy candidates are stored as pending MemoryRecords (approval_status='pending')
using the Phase 0 storage module. Nothing is committed to 'approved' status here.
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from typing import Optional

from storage import MemoryStorage, MemoryRecord, ApprovalStatus
from nebius_smoke_test import call_nemotron_nano_super, load_env_file

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt for the extraction judge
# ---------------------------------------------------------------------------

_EXTRACTION_SYSTEM_PROMPT = """\
You are a memory-extraction judge embedded in a personal AI assistant.

Your sole job is to decide whether the user's message contains a fact, decision,
preference, or important personal detail that is worth remembering long-term.

Rules:
1. Only extract genuinely informative, durable facts -- things that would still
   be relevant in a future conversation (e.g. "My name is Alice",
   "I prefer dark mode", "I am allergic to penicillin").
2. Do NOT extract ephemeral chit-chat, acknowledgements, greetings, filler,
   or questions that contain no self-referential information
   (e.g. "ok thanks", "what's the weather?", "sure", "tell me a joke").
3. Output ONLY valid JSON -- no prose, no markdown fences, no explanation.
   - If something IS worth remembering:
       {"content": "<concise factual statement>", "why": "<one-sentence justification>"}
   - If NOTHING is worth remembering:
       {}

Never output anything other than a single JSON object.\
"""

_EXTRACTION_USER_TEMPLATE = """\
User message:
\"\"\"{user_message}\"\"\"

Decide whether this message contains a memory-worthy fact, preference, or decision.\
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_memory_candidate(
    user_message: str,
    api_key: str,
    max_tokens: int = 256,
    temperature: float = 0.2,
) -> Optional[dict]:
    """Call Nemotron Nano/Super to judge a user turn for memory-worthiness.

    Returns a dict {"content": str, "why": str} if a candidate was found,
    or None if the model decided nothing is worth remembering.

    Never raises on model/parse failures -- logs a warning and returns None
    so the calling code never has to worry about this step crashing the chat.
    """
    messages = [
        {"role": "system", "content": _EXTRACTION_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": _EXTRACTION_USER_TEMPLATE.format(user_message=user_message),
        },
    ]

    try:
        response = call_nemotron_nano_super(
            api_key=api_key,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            raise_on_error=True,
        )
    except Exception as exc:
        logger.warning("[MemoryExtraction] Model call failed: %s", exc)
        return None

    raw = (response or {}).get("content", "").strip()
    if not raw:
        logger.debug("[MemoryExtraction] Empty model response -- nothing to extract.")
        return None

    # Strip any accidental markdown fences the model might still emit
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning(
            "[MemoryExtraction] Could not parse model JSON response: %r", raw
        )
        return None

    if not isinstance(parsed, dict) or not parsed.get("content"):
        # Model returned {} (or missing 'content') -> nothing to remember
        logger.debug(
            "[MemoryExtraction] Model returned empty/no-content object -- nothing to extract."
        )
        return None

    candidate = {
        "content": str(parsed["content"]).strip(),
        "why": str(parsed.get("why", "")).strip(),
    }
    logger.info(
        "[MemoryExtraction] Candidate extracted: content=%r  why=%r",
        candidate["content"],
        candidate["why"],
    )
    return candidate


def extract_and_store_pending(
    user_message: str,
    source_turn_id: str,
    api_key: str,
    storage: Optional[MemoryStorage] = None,
) -> Optional[MemoryRecord]:
    """Full pipeline: extract candidate then store as pending if found.

    Args:
        user_message:   Raw text of the user's turn.
        source_turn_id: The turn/session ID to attach to the stored record.
        api_key:        Nebius API key.
        storage:        Optional MemoryStorage instance; creates a default one
                        (memory.db) if not provided.

    Returns:
        The newly created MemoryRecord (approval_status='pending') if a
        candidate was found and stored, otherwise None.
    """
    candidate = extract_memory_candidate(user_message=user_message, api_key=api_key)
    if candidate is None:
        logger.debug(
            "[MemoryExtraction] No candidate for turn '%s' -- nothing stored.",
            source_turn_id,
        )
        return None

    store = storage or MemoryStorage()
    record = store.create(
        content=candidate["content"],
        source_turn_id=source_turn_id,
        approval_status=ApprovalStatus.PENDING,
    )
    logger.info(
        "[MemoryExtraction] Stored pending record id=%s for turn '%s'.",
        record.id,
        source_turn_id,
    )
    return record
