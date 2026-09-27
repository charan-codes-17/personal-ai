# Personal AI — Master Development & Vibe-Coding Roadmap

---

## 0. How to Use This Document

This is a working playbook, not a document to read once. Find your current checkpoint (Section 13), do the next small unit of work in that subphase (Section 5), verify it against the checkpoint's test, mark it, and move to the next one. Sections 6–18 are reference material you'll dip into as needed — the phase-by-phase plan (Section 5) is where you'll spend most of your time while actually coding.

**A scope note that governs everything below.** Your two source documents are not the same kind of document. The Master Plan is a deliberately non-lossy merge of four independent full-product visions — it _includes_ a Rust daemon, Wasm sandboxing, a Neo4j knowledge graph, federated inter-agent negotiation, and dozens of other multi-year, non-hackathon-feasible ideas, on purpose, because its job was to preserve everything. The PRD then takes that full vision and locks a specific, buildable scope for _this_ submission: a Streamlit app, Nemotron on Nebius, a fixed skill set, episodic memory with staged approval, due **Oct 30, 2026**, built solo at ~5–10 hrs/week. The PRD says explicitly: _"Where the two disagree, Section 22 wins for what gets built now, and the rest of the document remains the map of where the product can grow."_

This roadmap follows that instruction. **Sections 4–5 (the phases you actually build) implement the PRD's locked hackathon MVP** — not a generic 16-phase OS build sequence, and not the Master Plan's Rust-daemon architecture. **Section 7 (Advanced Feature Path)** carries the full Master Plan vision forward as the map for what comes after submission, exactly as the PRD's own §6.3/§6.4/§26/§29 intend, so nothing from either source document is dropped — it's just correctly sequenced as "later," not "now."

If you ever feel tempted to start building the Knowledge Graph, the skill compiler, or a sandboxed execution layer before the hackathon deadline — don't. That's explicitly out of scope per PRD §22, and every hour spent there is an hour not spent on the thing that's actually being judged: a working, live, Nemotron-on-Nebius memory loop.

---

## 1. Source Documents & Scope

|Document|Role|
|---|---|
|`Personal-AI-Unified-Master-Plan.md`|Full-vision source of truth — every feature, architecture idea, and long-term capability across all four source plans. Used here for traceability (Section 16) and the Advanced Feature Path (Section 7).|
|`Personal-AI-Detailled-Unified-Master-Plan.md`|The same four-plan merge in expanded form, with per-plan verbatim detail preserved (full standout-feature tables, the reconciled Phase 1/2/3 backlog in §20.5, the FR-7.1 per-task-type autonomy table, full multimodal/skill-compiler/integration detail). Section 7's post-hackathon sequencing below is built directly from this document's §20.5, §8.3, §9, §10, §7.4, and §27.|
|`Personal-AI-PRD.md`|Locked, implementation-ready scope for the Oct 30, 2026 hackathon submission. §22 (Hackathon MVP), §27 (Development Roadmap), and §28 (Engineering Backlog, BL-01–BL-17) are the direct basis for Sections 4–5 below.|

**What "done" means for this roadmap** is the PRD's own §29 Definition of Done: a live, deployed, Nemotron-on-Nebius memory loop that works without scripting around a failure — not the Master Plan's full-vision "done" (Section 18 restates this precisely).

---

## 2. Project Implementation Philosophy

1. **The core loop is the product.** Remember → persist → recognize relevance → act. Everything in Phases 0–3 exists to make this loop real; everything after exists to make it safe, visible, and demo-ready. If a task doesn't serve one of those two goals, it's Section 7 material, not now.
2. **Staged approval is the safety net, not a formality.** Because there's no sandboxing, no full permission ladder, and no undo system at this scope, the Memory Inbox (approve/reject before commit) and confirm-before-mutate are doing the trust-and-safety work that the full vision spreads across many more subsystems. Don't skip or stub them out.
3. **Task-route the models on purpose, from the start.** Nemotron Ultra for relevance/reasoning, Nano/Super for chat/extraction — this is both a cost control and a demo-credibility point (judges can see it's not one model doing everything). Wire this in Phase 1, not as a later refactor.
4. **Build the failure path as deliberately as the happy path.** The single biggest live-demo risk is an API failure producing a hallucinated answer instead of an honest error. Phase 6 and Phase 7 exist because of this.
5. **Small, sequential, testable units.** Each subphase below ends in something you can run and see work. Don't start the next one until the current checkpoint passes.

---

## 3. Dependency Map

```
Storage backend (memory record store)
   ↓
Nebius/Nemotron connectivity (both tiers)
   ↓
Chat loop (Nano/Super)
   ↓
Memory extraction (Nano/Super) ──────────────┐
   ↓                                          │
Memory Inbox (staged approval)                │
   ↓                                          │
Memory Timeline (browse/edit/delete)          │
   ↓                                          │
Context-relevance check (Ultra) ◄─────────────┘
   ↓
Proactive surfacing (context-triggered, deadline-triggered)
   ↓
Fixed skill set (invokable by name)
   ↓
Security gates (permission allow-list, confirm-before-mutate, sensitive-content filter)
   ↓
Audit log
   ↓
UI assembly (Home/briefing + Chat + Timeline as Streamlit tabs)
   ↓
Testing (integration + failure-path, against the deployed instance)
   ↓
Deployment
   ↓
Demo rehearsal & video
   ↓
Submission
```

**Hard dependencies:** storage before anything persists; Nebius connectivity before any model behavior; the chat loop before extraction has anything to extract from; staged approval before anything commits to memory; memory before context-relevance or deadline checks have data to work with.

**Soft dependencies:** the Sensitive Content Filter and conflict flagging strengthen memory extraction but don't block it from working end-to-end first. The Home/briefing view depends on the Timeline and proactive surfacing existing, but is itself optional (P2).

**Parallelizable work:** storage backend setup and Nebius connectivity smoke-testing (BL-01, BL-02) can happen side by side — neither blocks the other. UI shell scaffolding can start as soon as the chat loop exists, in parallel with memory-extraction work. Writing the demo script (Section 5, Phase 8) can start early and be refined throughout, rather than left to the end.

---

## 4. Overall Development Phases

This is the PRD's own §27 Development Roadmap, expanded into vibe-coding-sized phases with subphases and checkpoints. Phase numbers below map directly to backlog items (BL-XX) from PRD §28.

|#|Phase|Objective|
|---|---|---|
|0|Foundation|Storage backend, Streamlit skeleton, Nebius/Nemotron connectivity proven for both tiers|
|1|Core AI — Chat Loop|Working conversational turn handling via Nemotron Nano/Super|
|2|Memory System|Extraction → staged approval → commit → Timeline, plus conflict flagging|
|3|Proactive Intelligence|Context-triggered and deadline-triggered surfacing via Nemotron Ultra|
|4|Skills & Tools|The fixed, small skill set, invokable by name|
|5|Security & Privacy|Sensitive Content Filter, permission allow-list, confirm-before-mutate, audit log|
|6|UI Assembly|Streamlit tabs: Chat, Memory Timeline, (optional) Home/briefing|
|7|Testing & Reliability|Integration test of the core loop; failure-path test; routing verification|
|8|Deployment|Public, reachable demo URL|
|9|Demo Preparation|Rehearse the §23 scenario; record the ≤3-minute video|
|10|Submission Readiness|Work the PRD §24 checklist to completion|
|**F**|**(Future) Advanced Feature Path**|Everything in Master Plan Phase 2/V2 and Phase 3/Long-Term that this submission explicitly defers — see Section 7|

Do **not** build Phase F now. It's here so nothing from the Master Plan is silently lost — see Section 7 and Section 16 for exactly where each deferred capability re-enters the roadmap later.

---

## 5. Detailed Phase-by-Phase Plan

Status markers to use as you go: ⬜ Not Started · 🟡 In Progress · ✅ Completed · 🔴 Blocked · ⚠️ Needs Review

### Phase 0 — Foundation

**Objective:** Everything else attaches to this. A place for memory to live, and proven, working calls to both Nemotron tiers via Nebius. **Why now:** Nothing else in the roadmap can be tested without both of these existing. **Prerequisites:** Nebius account access with Token Factory/AI Cloud credits confirmed as usable (see Section 17, item 3 — this is the single biggest non-technical risk to resolve first). **Deliverables:** A working read/write store for memory records; a Streamlit app that boots; confirmed successful calls to both Nemotron Ultra and Nano/Super.

#### 0.1 — Storage Backend (BL-01)

- **Objective:** Stand up a structured store for memory records that survives a process restart.
- **Tasks:** Choose a storage approach appropriate to the deployment target (e.g., SQLite file, or a hosted lightweight DB if the deployment platform doesn't persist local files — resolve this jointly with the deployment-target decision in Section 17, item 1). Define the minimal Memory record schema from PRD §19: id, content, source-turn reference, timestamp, approval status. Implement basic create/read/update/delete functions.
- **Dependencies:** None — can start immediately, in parallel with 0.2.
- **Expected behavior:** A record written by a test script can be read back after the process restarts.
- **Validation:** Write a record, kill and restart the app process, read the record back — content matches.
- **Checkpoint 0.1:** ✅ when a record written in one process run is still readable in the next. Files/components: a storage module with `create_record`, `get_records`, `update_record`, `delete_record`. Safe to move forward once this round-trips reliably.
- **Failure condition:** Data doesn't survive a restart, or writes silently fail. Don't proceed to 0.2's dependent work until this is solid — everything downstream assumes durable storage.
- **AI coding prompt:** _"Nothing exists yet. Build a minimal persistent storage module in Python for a chat app's memory records. Schema: id (str), content (str), source_turn_id (str), timestamp (datetime), approval_status (enum: pending/approved/rejected). Provide create, list, update, and delete functions. Use [SQLite / chosen backend] so data survives a process restart. Include a simple test script that writes a record, simulates a restart by reopening the connection, and confirms the record is still readable. Do not add any UI or model-calling code yet — storage only."_

#### 0.2 — Nebius/Nemotron Connectivity (BL-02)

- **Objective:** Prove both Nemotron Ultra and Nano/Super are callable via Nebius Token Factory/AI Cloud before building anything that depends on them.
- **Tasks:** Obtain and securely store the Nebius API key (per the platform's standard secret-management approach — see PRD §16). Write a minimal test script that calls Nemotron Ultra with a trivial prompt and Nemotron Nano/Super with a trivial prompt, and prints both responses.
- **Dependencies:** Nebius credits/access confirmed (Section 17, item 3).
- **Expected behavior:** Both calls return valid, non-error responses.
- **Validation:** Run the script twice; confirm consistent success and note actual latency for each tier (informs the TBD performance targets in PRD §18).
- **Checkpoint 0.2:** ✅ when both tiers return valid responses in a standalone script, with API key never hardcoded into source (use environment variables / platform secrets). Safe to move forward once both calls succeed reliably.
- **Failure condition:** Auth errors, quota errors, or inconsistent failures. Resolve before writing any application code that depends on these calls — a shaky connectivity layer will make every later phase harder to debug.
- **Regression protection:** None yet — this is the first working piece.
- **AI coding prompt:** _"Write a standalone Python script that calls the Nebius Token Factory API twice: once against Nemotron Ultra, once against Nemotron Nano (or Super, whichever is the configured chat-tier model), each with a simple one-line prompt like 'Say hello in one sentence.' Read the API key from an environment variable, never hardcode it. Print each response and the response latency. Do not wire this into an app yet — this is a connectivity smoke test only. Include basic error handling that prints a clear message on auth failure vs. a quota/rate-limit failure vs. a network failure, so failures are distinguishable."_

**Verified model IDs (confirmed live against `GET /v1/models` on this account, 0.2 checkpoint) — reuse these exact strings in Phases 1, 2, and 3, don't re-derive or guess them again:**

- Ultra tier (relevance/reasoning calls — Phase 3): `nvidia/Nemotron-3-Ultra-550b-a55b`
- Super tier (chat/extraction calls — Phases 1, 2): `nvidia/nemotron-3-super-120b-a12b`
- Nano tier (alternative lighter option, also confirmed working): `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`
- Base URL: `https://api.tokenfactory.nebius.com/v1`
- No `nebius/` prefix on the model field when calling the API directly — that prefix is a third-party-router convention, not part of Nebius's own model IDs.
- Key is loaded from a local `.env` file (via `python-dotenv`), confirmed `.gitignore`'d — never hardcoded or committed.

#### 0.3 — Streamlit App Skeleton

- **Objective:** A bare Streamlit app that boots and can import both the storage module and the Nebius connectivity module.
- **Tasks:** Scaffold `app.py` with a single placeholder page. Confirm the storage module and Nebius module both import cleanly inside the Streamlit process (not just in a standalone script — Streamlit's execution model can surface import/env issues a plain script won't). Note: `.env`-based key loading works locally, but once deployed (Phase 8), Streamlit Community Cloud needs the key set via `st.secrets` instead — plan for the code to check `st.secrets` first and fall back to `.env`/`os.environ` for local dev, so the same code works in both places without edits.
- **Dependencies:** 0.1, 0.2.
- **Checkpoint 0.3:** ✅ when `streamlit run app.py` boots locally, shows a placeholder page, and a button click triggers one successful call to each Nemotron tier without error. This is your true Phase 0 exit checkpoint — do not start Phase 1 until this passes.
- **Failure condition:** Import errors, environment-variable issues inside Streamlit's process, or the app crashing on load.
- **Do-not-break rule going forward:** From this checkpoint on, the app must boot cleanly at the start of every future phase's work session before you touch anything else. If it doesn't, fix that first.

---

### Phase 1 — Core AI: Chat Loop (BL-03)

**Objective:** A user can hold a real conversation, with every response actually generated by Nemotron Nano/Super — no canned or mocked responses. **Prerequisites:** Phase 0 complete. **Deliverables:** A working chat interface in Streamlit; conversation-turn history maintained within a session.

#### 1.1 — Turn Handling & Session History

- **Tasks:** Implement a conversation-turn data structure (session id, turn content, timestamp — PRD §19). Wire the Streamlit chat input to call Nemotron Nano/Super with the running conversation history as context. Display responses in a scrolling chat UI.
- **Components:** `chat.py` (turn handling), extends `app.py`.
- **Expected behavior:** Multi-turn conversation feels coherent — the model references what was said two turns ago within the same session.
- **Acceptance criteria:** A user can ask a follow-up question that depends on earlier context in the same session and get a coherent answer.
- **Checkpoint 1.1:** ✅ when a 3+ turn conversation stays coherent and every response is confirmed (via a debug print or log line) to come from a real Nano/Super call, not a placeholder.
- **Testing:** Manual conversation test; confirm via logs that each turn triggers a real API call.
- **Failure condition:** Responses ignore prior turns, or the model call silently fails and the UI shows nothing/hangs.
- **Regression protection:** Phase 0's connectivity and storage checkpoints must still pass.
- **AI coding prompt:** _"Building on the existing Streamlit skeleton (app.py) and the Nebius connectivity module from Phase 0, implement a chat interface. Maintain conversation history in Streamlit session state as a list of {role, content, timestamp} turns. On each user message, call Nemotron Nano/Super with the full running history as context and display the response in a chat-style UI (st.chat_message or equivalent). Do not add memory extraction yet — this phase is turn handling only. Include a visible indicator while the model call is in flight, and a clear error message (not a silent hang) if the call fails."_

---

### Phase 2 — Memory System (BL-04, BL-05, BL-06, BL-08)

**Objective:** The heart of the product. A fact stated in one session is correctly recalled in a later one, only after the user has approved it, and the user can always see, correct, or delete what's remembered. This phase directly implements FR-001 through FR-004. **Prerequisites:** Phase 1 complete (there must be conversation turns to extract from). **Deliverables:** Memory extraction, a staged-approval Memory Inbox, a browsable/editable/deletable Memory Timeline, and conflict flagging.

#### 2.1 — Memory Extraction (BL-04)

- **Objective:** Propose candidate memories from conversation via Nemotron Nano/Super.
- **Tasks:** After each conversation turn (or on a periodic/end-of-topic basis — your call, document the choice), send the turn to Nano/Super with a judgment prompt: "is anything here worth remembering, and as what?" Parse the response into candidate memory objects (not yet committed).
- **Dependencies:** 1.1.
- **Expected behavior:** A stated fact ("I'm using PyTorch for this project") produces a candidate memory object; small talk produces none.
- **Acceptance criteria (traces FR-002 precondition):** A stated fact reliably produces a candidate; "do nothing" is a valid, common outcome — don't force a candidate out of every turn.
- **Checkpoint 2.1:** ✅ when a clearly fact-bearing test message produces exactly one sensible candidate object, and a clearly non-fact-bearing message ("thanks!") produces none.
- **Failure condition:** Every message produces a candidate (over-extraction, will flood the Inbox) or facts are consistently missed.
- **AI coding prompt:** _"Add a memory-extraction step that runs after each user turn, using Nemotron Nano/Super. Prompt the model to judge whether the turn contains a fact, decision, or preference worth remembering, and if so, to return it as a short structured candidate (content string + a short 'why remember this' justification). If nothing is worth remembering, it should return nothing — this is a valid, expected, and common outcome, not an error. Store candidates as pending records (approval_status='pending') using the Phase 0 storage module — do not commit them to approved status yet. Test with an obvious fact statement and an obvious non-fact statement (like 'ok thanks') and confirm the extraction behaves correctly for both."_

#### 2.2 — Memory Inbox / Staged Approval (BL-05)

- **Objective:** Nothing reaches long-term, usable memory without the user approving it (FR-002).
- **Tasks:** Build a UI section listing pending candidates with Approve/Ignore actions (Modify and Never-remember are P1 refinements — add if time allows). On Approve, flip `approval_status` to `approved`. On Ignore, either delete or mark `rejected`.
- **Dependencies:** 2.1.
- **Expected behavior:** A candidate sits visibly pending until the user acts; nothing auto-commits.
- **Acceptance criteria (FR-002):** No record exists as `approved` that the user didn't explicitly approve.
- **Checkpoint 2.2:** ✅ when you can generate a candidate, see it in the Inbox, approve it, and confirm (by inspecting storage directly) that only the approved record's status changed — nothing else was silently committed.
- **Failure condition:** Candidates auto-commit, or the Approve action affects the wrong record.
- **AI coding prompt:** _"Add a 'Memory Inbox' section to the Streamlit app showing all pending-status memory records from storage, each with Approve and Ignore buttons. Approve sets approval_status to 'approved'; Ignore sets it to 'rejected' (or deletes it — your choice, document which). Nothing should change status except through these explicit user actions. Add a quick manual test: create two pending candidates, approve one and ignore the other, then verify via the storage module that only the approved one shows approval_status='approved'."_

#### 2.3 — Memory Timeline (BL-06)

- **Objective:** A browsable, correctable, deletable record of everything approved (FR-003).
- **Tasks:** Build a Timeline view listing approved memory records (most recent first is a reasonable default), each with inline edit and delete controls.
- **Dependencies:** 2.2.
- **Acceptance criteria (FR-003):** Every stored approved record is visible, editable, and deletable from this view — verify all three actions work, not just display.
- **Checkpoint 2.3:** ✅ when you can edit a record's content and see the change persist, and delete a record and confirm it's gone from storage, not just hidden in the UI.
- **Failure condition:** Edits don't persist, or delete only hides the record from view without removing it from storage (this matters for the privacy principle in PRD §16 — deletion needs to be real).
- **AI coding prompt:** _"Add a Memory Timeline tab to the Streamlit app, listing all approval_status='approved' records, most recent first, each showing content and timestamp with Edit and Delete controls. Edit should update the record in storage; Delete should remove it from storage entirely, not just from the displayed list. Test: edit a record's text and confirm the change is in storage after a page refresh; delete a record and confirm a direct storage query no longer returns it."_

#### 2.4 — Conflict Flagging (BL-08)

- **Objective:** Never silently overwrite a memory with contradictory new information (FR-004).
- **Tasks:** When extraction (2.1) proposes a candidate, check it against existing approved memories for topical overlap (a simple approach: ask Nemotron whether the new candidate contradicts any of a short list of topically-similar existing memories — exact retrieval-ranking approach is a PRD-flagged open decision, §13; keep it simple for now, e.g. keyword or embedding similarity on a small memory set). If a contradiction is detected, surface both statements to the user and ask which is current, instead of auto-approving.
- **Dependencies:** 2.1, 2.2.
- **Acceptance criteria (FR-004):** Given two contradictory statements across sessions, the system surfaces both and asks which is current — it never picks one silently.
- **Checkpoint 2.4:** ✅ when a deliberately contradictory test pair ("I'm using React" then later "I switched to Vue") triggers a conflict prompt instead of silently creating two approved facts or overwriting the first.
- **Failure condition:** Contradictions are missed (both facts sit approved with no flag) or one silently overwrites the other.
- **Testing:** Behavioral test with a scripted contradiction; this is the single most demo-relevant behavior after the core recall loop, so test it deliberately, not incidentally.
- **AI coding prompt:** _"Extend the memory-extraction step from Phase 2.1: before a candidate reaches the Inbox, check it against existing approved memories for the user for topical contradiction (simple approach: compare against the 5 most similar existing approved memories using [your chosen similarity method], and ask Nemotron Ultra whether the new candidate contradicts any of them). If a contradiction is found, mark the candidate as 'conflict' status instead of 'pending', and show it in the Inbox with both the new statement and the conflicting old one, letting the user pick which is current (updating the old record or keeping both, your call — document it). Test explicitly with a contradictory pair of statements in two separate sessions."_

**Phase 2 exit checkpoint:** the full loop — state a fact, approve it, close the session, open a new session, ask a related question, get it recalled correctly (a basic version of FR-001's acceptance criterion, ahead of full relevance-scoring in Phase 3) — works end to end. This is the single most important checkpoint in the whole roadmap. Don't move to Phase 3 until it's rock solid.

---

### Phase 3 — Proactive Intelligence (BL-07, BL-10)

**Objective:** The assistant proactively reconnects new context to old, without being asked — the core demo differentiator (PRD §10.1's primary journey). Implements FR-006 and FR-007. **Prerequisites:** Phase 2 complete (there must be approved memories to be relevant to).

#### 3.1 — Context-Triggered Relevance Check (BL-07)

- **Objective:** Detect when a new conversation topic relates to stored memory, using Nemotron Ultra.
- **Tasks:** On each new user turn, retrieve a small set of topically-similar approved memories (same retrieval approach as 2.4). Send the current turn plus these candidates to Nemotron Ultra with a relevance-judgment prompt: is this worth surfacing right now? If yes and confidence is reasonably high, weave the reconnection into the chat response _as a stated, correctable connection_ — never an unstated assumption (FR-6.2's evidence-not-truth principle). If confidence is low, say nothing (FR-5.1: "do nothing" is a valid default).
- **Dependencies:** Phase 2 complete; this is the first place Nemotron Ultra is used in the live loop (Phase 0.2 was just a smoke test).
- **Expected behavior:** A new-session question on a previously-discussed topic gets a response that references the prior context, framed as "it looks like this connects to X you mentioned before — is that right?" rather than a flat assumption.
- **Acceptance criteria (FR-006):** Given a new-session prompt on a topic with prior stored context, the system references the prior context unprompted, with visible confidence/evidence framing.
- **Checkpoint 3.1:** ✅ when a scripted two-session test (state a fact in session 1, ask a related question in a fresh session 2) reliably produces a correctly-framed reconnection, and an unrelated question produces no forced reconnection.
- **Failure condition:** The model reconnects to irrelevant memories (over-triggering), states connections as flat fact instead of a checkable suggestion, or misses an obviously related topic.
- **Testing:** This is your primary demo scenario — test it more than any other single behavior, across several fact/question pairs, not just one.
- **AI coding prompt:** _"Implement context-triggered proactive surfacing using Nemotron Ultra. On each new user turn, retrieve the small set of topically-similar approved memories (reuse the similarity approach from Phase 2.4). Send the current turn and these candidate memories to Nemotron Ultra, asking it to judge whether any candidate is genuinely relevant enough to surface right now, and if so, phrase the connection as a checkable suggestion ('It looks like this relates to X you mentioned — is that still accurate?'), never as a flat assumption. If no candidate clears a reasonable relevance bar, the model should say nothing about past context and just answer normally — this is the expected, common case, not a failure. Test with: (a) a fact stated in one session, a clearly related question in a new session — expect a correct, well-framed reconnection; (b) a fact stated in one session, an unrelated question in a new session — expect no forced reconnection."_

#### 3.2 — Deadline-Triggered Surfacing (BL-10)

- **Objective:** Surface a suggestion when a stored, deadline-bearing item is approaching and unresolved.
- **Tasks:** When extraction (2.1) detects a deadline-bearing statement, tag the memory record accordingly (a simple field is enough — no need for a full date-parsing library unless one's already at hand). On app load / session start, check tagged records for approaching, unresolved deadlines and surface a suggestion (not a push interruption — FR-008).
- **Dependencies:** 3.1's relevance-scoring pattern (reused, per PRD §10.3's own note).
- **Acceptance criteria (FR-007):** Given a stored item with an approaching deadline and no resolution recorded, a suggestion appears; given stale/ambiguous deadline data, the nudge is suppressed rather than shown at low confidence.
- **Checkpoint 3.2:** ✅ when a test memory tagged with a near-future deadline produces a suggestion on the next session start, and a stale/already-past or ambiguous one does not.
- **Failure condition:** Deadline nudges fire for irrelevant or stale items, or never fire at all.
- **AI coding prompt:** _"Add deadline-triggered proactive surfacing. Extend the Phase 2.1 extraction step to flag when a candidate memory contains a deadline-like statement (a due date, an approaching commitment), tagging the record with a simple deadline field. On app/session start, check approved memories with a deadline field for items that are approaching (within a reasonable window, your call) and not marked resolved, and surface them as an in-app suggestion, never a forced popup or push notification. If the deadline is ambiguous or already past, suppress the nudge rather than showing it. Test with a near-future deadline memory (expect a suggestion) and a stale/past one (expect suppression)."_

#### 3.3 — Suggestion-Not-Interruption Discipline (FR-008)

- **Objective:** Confirm all proactive output across 3.1 and 3.2 is delivered as an in-app suggestion, never a blocking interruption.
- **Checkpoint 3.3:** ✅ — audit both 3.1 and 3.2's UI surfacing code paths and confirm neither uses a blocking modal, forced popup, or anything that halts the user's current action. This is a review checkpoint, not new code.

---

### Phase 4 — Skills & Tools (BL-11, BL-12)

**Objective:** The fixed, small, pre-built skill set runs correctly and is invokable by name (FR-013). **Prerequisites:** Phase 2 (skills will likely read/write memory). **Note:** The exact tools in this fixed set are still an open decision per PRD §30 item 2 — resolve that first (see Section 17 below), then run this phase.

#### 4.1 — Fixed Skill Set (BL-11)

- **Tasks:** Implement each chosen skill (e.g., session briefing, summarization, context-reconnection-on-demand) as a simple, hand-authored prompt template with defined inputs (typically: recent approved memories) and outputs (a short generated response). Make each invokable by name in chat (e.g., typing "run session briefing" triggers it).
- **Acceptance criteria (FR-013):** Naming a skill in chat triggers its execution and produces the expected kind of output.
- **Checkpoint 4.1:** ✅ when each skill in the fixed set can be triggered by name and produces a sensible output using real memory data, not placeholder text.
- **AI coding prompt:** _"Implement the fixed skill set as simple, hand-authored functions, each taking the user's approved memories (and conversation context where relevant) as input and calling Nemotron Nano/Super to produce a defined output — for example, a 'session briefing' skill that summarizes recent approved memories into a short catch-up paragraph. Wire skill invocation by name: if the user's message matches a skill's name/trigger phrase, run that skill instead of falling through to normal chat. Test each skill individually with real stored memory data."_

#### 4.2 — Confirm-Before-Mutate Gate (BL-12)

- **Objective:** No action with a side effect outside the chat/memory store executes without explicit confirmation (FR-010).
- **Tasks:** Identify which (if any) of your fixed skills have a mutating side effect (e.g., calling an external tool/API). For each, require an explicit confirmation click before executing, not just before the skill starts.
- **Checkpoint 4.2:** ✅ when a mutating skill (if any exist in your final set) visibly pauses for confirmation and does not execute on a single message alone. If your final skill set has no external side effects, document that explicitly and mark this checkpoint N/A rather than skipping it silently.
- **Failure condition:** A mutating action fires without a click.
- **Regression protection:** Phase 2 and Phase 3 checkpoints still pass — skill invocation shouldn't interfere with normal chat or proactive surfacing.

---

### Phase 5 — Security & Privacy (BL-09, BL-13)

**Objective:** The minimal but real trust-and-safety floor: sensitive content excluded from extraction, tool calls gated, every write logged. **Prerequisites:** Phase 2 (extraction and storage must exist to filter/log).

#### 5.1 — Sensitive Content Filter (BL-09)

- **Objective:** Exclude health, finance, and password-like content from automatic memory extraction by default (FR-005).
- **Tasks:** Add a filter step before a candidate reaches the Inbox — either a keyword/category check or a Nemotron-based classification pass — that drops or blocks candidates in excluded categories.
- **Acceptance criteria (FR-005):** A test statement in an excluded category (e.g., a made-up health detail) is not proposed as a candidate memory.
- **Checkpoint 5.1:** ✅ when a deliberately sensitive test statement produces no candidate, while an ordinary fact still does.
- **AI coding prompt:** _"Add a Sensitive Content Filter step in the memory-extraction pipeline (Phase 2.1), running before a candidate is stored as pending. Classify candidates against a small set of excluded categories (health, finance, passwords/credentials) — either keyword-based or a quick Nemotron classification call — and drop any candidate that falls into an excluded category, never surfacing it in the Inbox at all. Test with an obviously sensitive test statement (expect no candidate) and an ordinary fact (expect normal candidate creation, unaffected)."_

#### 5.2 — Minimal Permission Gate (FR-009)

- **Tasks:** Maintain an explicit, fixed allow-list of tool calls the app is permitted to make. Any call not on the list is rejected and logged, not silently skipped.
- **Checkpoint 5.2:** ✅ when a deliberately disallowed test call is rejected and produces a log entry.

#### 5.3 — Basic Audit Log (BL-13)

- **Objective:** Record every memory write and skill run (FR-014).
- **Tasks:** Add a lightweight log entry on every memory commit (Phase 2.2's Approve action) and every skill execution (Phase 4.1), recording what happened and when.
- **Checkpoint 5.3:** ✅ when a test session's log shows one entry per approved memory and one entry per skill run, matching what actually happened.
- **AI coding prompt:** _"Add a basic audit log: a simple append-only record (reuse the storage module's pattern) that logs one entry whenever a memory record's status changes to 'approved' and whenever a skill executes, each entry recording what happened and a timestamp. Add a minimal view (even a simple list) to inspect the log. Test by running a session with two memory approvals and one skill invocation, then confirm the log has exactly three matching entries."_

---

### Phase 6 — UI Assembly

**Objective:** Assemble the pieces built so far into the PRD's reduced command-center slice: Chat + Memory Timeline, plus an optional Home/briefing view if time allows (PRD §7.20, §9). **Prerequisites:** Phases 1–5 functionally complete (this phase is largely integration, not new logic).

#### 6.1 — Tab/Page Structure

- **Tasks:** Organize the Streamlit app into clear sections/tabs: Chat (Phase 1+3+4), Memory Timeline (Phase 2.3, with the Inbox from 2.2 visible here or as its own tab), and optionally Home/briefing (a landing view showing recent memory + pending suggestions, per PRD §7.20 — this is P2, build it only if the P0/P1 phases above are solid and stable first).
- **Checkpoint 6.1:** ✅ when a user can navigate among all implemented sections without losing session state, and every previously-passed checkpoint from Phases 1–5 still passes inside the assembled app (not just in isolation).
- **Failure condition:** Navigating between tabs resets chat history or loses in-flight state.

---

### Phase 7 — Testing & Reliability (per PRD §25)

**Objective:** Prove the core loop and the failure path both work against the real, deployed system — not mocked, not just locally. **Prerequisites:** Phases 0–6 complete.

#### 7.1 — Core-Loop Integration Test

- **Tasks:** Script and run the full loop end-to-end: state a fact → approve it → close session → open new session → ask related question → confirm correct, well-framed recall (FR-001, FR-006). Run this against the real Nebius/Nemotron endpoint.
- **Checkpoint 7.1:** ✅ when this passes at least twice in a row, cleanly.

#### 7.2 — Model-Routing Verification (FR-011)

- **Tasks:** Add logging (if not already present from earlier phases) confirming which model tier handled each call type, and spot-check a session's logs to confirm Ultra is only used for relevance/reasoning calls and Nano/Super for chat/extraction, per the routing rule.
- **Checkpoint 7.2:** ✅ when a session's logs show consistent, correct routing with no silent fallback to a single model.

#### 7.3 — Failure-Path Test (FR-012)

- **Tasks:** Simulate a Nebius/Nemotron API failure (e.g., temporarily point at a bad endpoint or invalid key) and confirm the app degrades gracefully — an honest error message, not a hallucinated answer or a crash.
- **Checkpoint 7.3:** ✅ when a simulated failure produces a visible, honest error state every time it's tried.
- **Why this matters more than it looks like it does:** this is the test that protects you specifically during the live demo, per PRD's own risk table (§26).

#### 7.4 — Security/Permission Spot-Checks

- **Tasks:** Re-run 5.1's and 5.2's tests against the assembled, deployed app (not just the isolated modules).
- **Checkpoint 7.4:** ✅ when both still pass post-integration.

---

### Phase 8 — Deployment (BL-16)

**Objective:** A reachable, public demo URL, independent of your own machine/session. **Prerequisites:** Phase 7 passing locally first — don't debug the core loop for the first time in production.

#### 8.1 — Deploy & Verify

- **Tasks:** Deploy to **Streamlit Community Cloud** (locked, revised from the PRD's original Hugging Face Spaces suggestion — HF now requires a paid plan for any Space that runs a live Python backend, Streamlit included; only their Static Spaces, which can't run Streamlit, remain free — see Section 17). Confirm secrets (Nebius API key) are configured via Streamlit Community Cloud's "Secrets" settings, not committed to the repo. Note: the free tier sleeps after ~12 hours idle and a redeploy resets any local-disk storage, so Phase 0.1's storage backend should not assume the local file survives indefinitely — resolve alongside item 1 in Section 17.
- **Checkpoint 8.1:** ✅ when the app is reachable from a device/network other than your own, and Phase 7's checkpoints all still pass against the deployed instance specifically (not just locally).
- **Regression protection:** Re-run 7.1 and 7.3 against the deployed URL before considering this phase done — deployment environments surface issues local runs don't.

---

### Phase 9 — Demo Preparation (BL-17)

**Objective:** A ≤3-minute video and a rehearsed live run that match each other exactly, following the PRD §23 scenario. **Prerequisites:** Phase 8 complete.

#### 9.1 — Rehearse the Scenario

- **Tasks:** Run the full PRD §23 demo arc (session 1: state something; session 2: related topic surfaces proactively; close on the Memory Timeline showing the correctable record) live, on the deployed URL, more than once.
- **Checkpoint 9.1:** ✅ after at least two clean, successful full run-throughs on the deployed instance.

#### 9.2 — Record the Video

- **Tasks:** Record a ≤3-minute video following the same arc, showing exactly what the live app does — no scripting around behavior that doesn't actually happen live.
- **Checkpoint 9.2:** ✅ when the video and a subsequent live run are behaviorally identical.

---

### Phase 10 — Submission Readiness

**Objective:** Every item in PRD §24's checklist is either done or explicitly, knowingly left TBD with a stated reason. **Tasks:** Work through the checklist directly (reproduced in Section 15 below as your Full System Completion Checklist for this submission). **Checkpoint 10.1:** ✅ when Section 15's checklist is fully worked through before Oct 30, 2026, 10:00 AM PT.

---

## 6. MVP Path

The MVP path _is_ Phases 0–10 above, in order. There is no separate, smaller MVP inside the hackathon MVP — PRD §22 already represents the minimum viable slice of the full Master Plan vision. Don't further cut scope from this list without updating the PRD's own P0 designations first; do treat the P1/P2 items called out within each phase (Modify/Never-remember in the Inbox, bulk purge, quiet-hours tuning, Home/briefing view, export) as genuinely optional — build them only after every P0 checkpoint above is solid.

---

## 7. Advanced Feature Path (Post-Hackathon)

This is where the rest of the Master Plan lives. Nothing here is built during Phases 0–10; it's sequenced for _after_ submission. Section 7.0 below is your **specific, chosen feature set** (the ten features you selected, minus WhatsApp and autonomous ticket booking), sequenced by real dependency, not just priority. Section 7.1/7.2 retain the _full_ Master Plan Phase 2/3 lists underneath it, so anything you didn't pick is still documented with a landing spot — nothing from either source document disappears. Traceability to specific sections of both Master Plan documents is in Section 16.

### 7.0 Your Selected Feature Set — Sequenced Build Order (post-hackathon)

Four waves, in order. Don't start a wave until the previous wave's checkpoint-equivalent (a working, demoable version of each item in it) is solid — the same discipline as Phases 0–10.

**Wave A — Extends existing infrastructure, no new external integrations** _(Builds directly on the memory store, Timeline, and skill infra you already have from the hackathon. Lowest risk, start here.)_

|#|Feature|What it is|Depends on|Source|
|---|---|---|---|---|
|A1|People / Projects / Decisions|Personal Knowledge Graph — extends your flat memory records with typed entities (Person, Project, Decision) and relationships between them, plus provenance (why/when a fact was captured)|Phase 2's memory store (already built)|Detailed Plan §8.3, §20.5 Phase 2|
|A2|Daily Life Tracker|A reporting layer over the existing Memory Timeline — trends, activity over time, a "Life Timeline" view|A1 (richer if entities exist, but works on flat memory too)|Detailed Plan §27.4 ("Life Timeline")|
|A3|Daily Priority Digest|The Master Plan's own named feature "Daily Operating Plan" — a generated, prioritized "here's your top items today" view combining memory, deadlines, and (once it exists) calendar/mail|A1, your existing Phase 3 deadline-surfacing engine|Detailed Plan §27.3/§27.4 ("Automated Daily Operating Plan" / "Daily Operating Plan")|
|A4|Study + Exam Assistant|A specialized skill: tracks study topics/progress as memory + graph entities, surfaces weak areas, plans revision sessions|A1 (needs entities to track "topics" and "progress" against), your existing skill-invocation pattern from Phase 4|Detailed Plan §27.5 student journey, §13.2|

**Wave B — Interaction layer, self-contained** _(Doesn't require new integrations or the autonomy ladder — can run in parallel with Wave A once Wave A's basics exist.)_

|#|Feature|What it is|Depends on|Source|
|---|---|---|---|---|
|B1|Voice / Image Input|Speech-to-text for input, OCR/vision for screenshots and documents, feeding into your existing chat loop|Phase 1 chat loop only|Detailed Plan §7.4|
|B2|Natural-Language Skill Creation|The Skill Compiler — user describes a workflow in plain language, it's turned into a structured, permission-scoped, versioned skill definition|Your existing fixed-skill infrastructure from Phase 4 (the compiler _generates_ what Phase 4 already knows how to run)|Detailed Plan §9.2, §9.3, §20.5 Phase 2|

**Wave C — Infrastructure prerequisites** _(Nothing user-facing on its own — this is the plumbing that Wave D needs. This is the wave you flagged as a build-order concern, and you were right to.)_

|#|Feature|What it is|Depends on|Source|
|---|---|---|---|---|
|C1|Multi-App Integration Hub|A generalized OAuth-connection pattern (auth flow, token storage, permission scope per app) that each specific integration plugs into — build the _pattern_ once, then add apps one at a time|Phase 5's permission-gate concept, generalized|Detailed Plan §10.1, §10.5|
|C2|Mail Check (read)|The first concrete integration built on C1 — Gmail/Outlook OAuth, read-only scope|C1|Detailed Plan §10.1 (named integration), FR-3.9 (email-summary skill template)|
|C3|Per-Task-Type Autonomy Ladder|Expands your hackathon's single confirm-before-mutate gate (Phase 4.2) into the full model: autonomy configured _per task type_, never globally — e.g. Email: Draft-only; Calendar: Execute-with-approval; Research: Autonomous; Purchases: Always ask; File deletion: never, full stop|Phase 5's permission gate|Detailed Plan §4 FR-7.1 (verbatim table), §10.2|

**Wave D — Built on top of Wave C's infrastructure** _(This is exactly the wave that would need rebuilding if you skipped Wave C — sequencing it last is deliberate, not arbitrary.)_

|#|Feature|What it is|Depends on|Source|
|---|---|---|---|---|
|D1|Autonomous Task Execution|The general execution engine that actually _acts_ using C3's per-task-type permissions — not a standalone feature, it's what C3 enables|C1, C3|Detailed Plan §10.2, §9.4|
|D2|Put Mails For Me|Drafts (and, only once you're confident, sends) email on your behalf — per C3's own table, Email defaults to **Draft-only**: it prepares the message, you approve the send. This is not optional caution — every one of your four source plans independently landed on the same rule for anything that leaves your outbox|C2 (read access first), C3 (Draft-only tier), D1|Detailed Plan §4 FR-7.1, §10.2 permission table|
|D3|Work Assistant (track + research + analyze + problem-solve)|Combines Autonomous Research Missions (a background agent that runs multi-step research independently, e.g. "research these 5 options, compare, save results") with Decision Memory (a record of _why_ past decisions were made, so the assistant can reason from your own history)|D1 (research missions need real autonomous execution to be more than a single chat reply), A1 (decisions as graph entities)|Detailed Plan §9.4 ("Autonomous Research Missions"), §3.5 (Decision Memory)|

**Cross-device sync** is deliberately _not_ in the four waves above — it's its own large, mostly-independent infrastructure project (encrypted multi-device state sync), not something that composes on top of the others. Build an initial version whenever convenient after Wave B, in parallel with Wave C/D rather than blocking on them; the Detailed Plan (§20.5 Phase 2) scopes an "initial version" there, with full E2EE explicitly pushed to Phase 3/Long-Term (§18.4, §16.3) — don't attempt full E2EE alongside the initial version, that's a materially larger job on its own.

**What's still deliberately excluded**, per your own call and the risk flagged earlier: WhatsApp integration (no legitimate personal-inbox API exists) and autonomous ticket booking (every source plan puts purchases at "Always ask" — booking prep is fine once D1/D3 exist, but the actual purchase click stays yours).

### 7.1 Phase 2 / V2 (full Master Plan list, Detailed Plan §20.5, PRD §6.3)

Everything in Wave A–D above is drawn from this list; the remainder not yet covered by your selections:

- Full Proactive Intelligence Engine: all five trigger types (scheduled, context, deadline, opportunity, autonomous-completion), full anti-annoyance controls (quiet hours, frequency caps, per-topic mute), pattern-to-skill-prompt detection (§7.2, §17.2).
- Full Automation Engine: triggers, conditions, retries with backoff, human-approval nodes (§17.1).
- Expanded integrations beyond Mail: Notion, Slack, GitHub, Zotero, and others (§10.1) — add one at a time on top of Wave C1's hub, same pattern as Mail.
- Memory Inbox multi-state refinement (Modify, Never-remember), TTL-based expiration, selective/bulk forgetting (§8.4).
- Data export / portability (§15.2 — flagged as a strong candidate to pull forward if time allows even pre-hackathon, per PRD §30 item 7).
- Local/private model options; hybrid local+cloud inference (§7.3, §15.2) — a genuine architectural shift from this submission's Nebius-hosted-only approach.
- Goal tracking, richer/contextual-scoped permission system (§20.5).

### 7.2 Phase 3 / Long-Term (full Master Plan list, Detailed Plan §20.5)

- Full personal AI OS with local daemon / system-level hooks (Master Plan §5.5's flagged, unresolved Rust-daemon-vs-generic-service conflict must be decided here, not before).
- Sandboxed skill/tool execution (Wasm or containers) (§10.5).
- Skill marketplace with signed packages and provenance metadata (§9.3).
- Multi-hour autonomous research missions at full scale, temporary/ephemeral agents, multi-agent orchestration (§9.4) — Wave D3 above is the _initial_ version of this; this is its long-term maturation.
- Digital Twin / simulation mode for low-stakes decisions (§9.4).
- Personal API (skills-as-API) (§18.1).
- Cross-device sync matured to full E2EE (§16.3, §18.4).
- Federated inter-agent negotiation, federated learning, smart-home/wearable/IoT integration, on-device hardware-acceleration optimization (§18.4, §20.5) — explicitly multi-year items in the Master Plan itself.

**Vertical-slice guidance for when this resumes:** don't rebuild the whole memory layer before adding the Knowledge Graph — extend the existing episodic store with graph edges incrementally, the same way Phase 2 of this roadmap extended Phase 0's flat storage. The smallest useful next vertical slice after submission is Wave A above (Knowledge Graph → Daily Tracker → Daily Digest → Study Assistant) — all four compose on infrastructure you'll already have, with zero new integrations, before you touch Wave C's OAuth/autonomy plumbing.

---

## 8. Parallel Development Opportunities

- **Phase 0.1 (storage) and 0.2 (Nebius connectivity)** — no dependency between them, do both at once if you have two coding sessions available in the same week.
- **Demo script drafting (Phase 9 content)** — can start as soon as Phase 3 is checkpointed, refined in parallel with Phases 4–8 rather than written cold at the end.
- **UI shell scaffolding (Phase 6.1's tab structure)** — can be stubbed out as soon as Phase 1's chat loop exists, then filled in as Phases 2–5 land, rather than left as one big integration task at the end.
- **Section 17's open decisions (deployment host, exact skill-set tools, billing resolution)** — resolve these early and in parallel with Phase 0, since several later phases (4, 8) are blocked on them.

---

## 9. Testing Strategy

Restated from PRD §25, mapped to the phases above:

|Testing type|Where it happens|Priority|
|---|---|---|
|Unit — memory staging & conflict logic|Phase 2.2, 2.4|P1|
|Integration — full core loop, real endpoint|Phase 7.1|**P0**|
|AI/model — routing verification|Phase 7.2|P1|
|Tool — failure path for any skill using external calls|Phase 4, 7.3|P1|
|Memory — cross-session recall correctness|Phase 2 exit checkpoint, Phase 7.1|**P0**|
|Security — sensitive-content rejection|Phase 5.1, 7.4|P2|
|Permission — disallowed call rejection|Phase 5.2, 7.4|P1|
|Failure — simulated API failure|Phase 7.3|**P0**|
|End-to-end — full demo scenario|Phase 9.1|**P0**|
|Demo validation — video matches live app|Phase 9.2|**P0**|
|Environment — deployed reachability|Phase 8.1|**P0**|

No formal test-harness framework is mandated by either source document — manual, scripted rehearsal against the real deployed instance is the appropriate level of rigor for this scope (PRD §25's own framing).

---

## 10. Security & Privacy Checkpoints

Threaded through the phases, not deferred to the end:

- **Phase 0.2:** API key never hardcoded; environment-variable/platform-secret handling from the very first connectivity script.
- **Phase 2.2:** staged approval as the write-time consent gate — the single most important privacy control at this scope.
- **Phase 2.3:** real deletion (not soft-hide) from the Timeline.
- **Phase 3.1:** evidence-not-truth framing — proactive surfacing never states an assumption as fact.
- **Phase 5.1:** Sensitive Content Filter, before extraction ever reaches the Inbox.
- **Phase 5.2:** fixed allow-list for any tool calls; disallowed calls rejected and logged, not silently dropped.
- **Phase 5.3:** audit log covering every memory write and skill run.
- **Phase 7.4 / 8.1:** re-verify all of the above against the deployed instance, not just local dev.
- **Phase 9.2:** the demo explicitly does not claim capabilities not built (no Knowledge Graph visualization, no sandboxed execution implied) — an honesty-of-scope check, not a code check, but a real checkpoint.

Deferred, documented, not built now: full multi-axis CBAC, dedicated secrets vault, AES-256 with user-held keys, cryptographic deletion, prompt-injection isolation layer (only relevant if the final skill set fetches external content — see Section 17 item 2).

---

## 11. Observability & Debugging Strategy

Given the flat, unlayered architecture at this scope, most debugging is "which of the six pipeline stages produced the wrong output":

```
User message
   → Chat loop (Phase 1) — is the message reaching the model at all?
   → Extraction (Phase 2.1) — did a candidate get proposed correctly?
   → Inbox/staging (Phase 2.2) — did approval status change correctly?
   → Relevance check (Phase 3.1) — did the right memories get retrieved and judged?
   → Skill invocation (Phase 4) — did the right skill fire, with the right inputs?
   → Audit log (Phase 5.3) — is there a log entry matching what actually happened?
```

Practical debugging aids to build as you go (not a separate phase — fold into the relevant phase's tasks):

- Log every model call with: which tier (Ultra vs. Nano/Super), the call's purpose (chat / extraction / relevance / skill), and success/failure. This single log is your Phase 7.2 routing-verification tool, your Phase 7.3 failure-detection tool, and your day-to-day debugging tool.
- A simple way to inspect storage contents directly (even a debug page or a one-off script) — don't rely solely on the Timeline UI to verify what's actually in the store, since a UI bug could mask a storage bug or vice versa.
- When a checkpoint fails: identify which pipeline stage above produced the bad output (check the call log first), re-run that stage in isolation if possible, fix, then re-run the full checkpoint test — not just the isolated piece.

---

## 12. Master Build-Order Table

|Order|Phase|Subphase|Objective|Depends On|Priority|Checkpoint|
|---|---|---|---|---|---|---|
|1|0|0.1|Storage backend|—|P0|0.1|
|2|0|0.2|Nebius/Nemotron connectivity|—|P0|0.2|
|3|0|0.3|Streamlit skeleton|0.1, 0.2|P0|0.3|
|4|1|1.1|Chat loop|0.3|P0|1.1|
|5|2|2.1|Memory extraction|1.1|P0|2.1|
|6|2|2.2|Memory Inbox (staged approval)|2.1|P0|2.2|
|7|2|2.3|Memory Timeline|2.2|P0|2.3|
|8|2|2.4|Conflict flagging|2.1, 2.2|P1|2.4|
|9|3|3.1|Context-triggered surfacing|Phase 2|P0|3.1|
|10|3|3.2|Deadline-triggered surfacing|3.1|P0|3.2|
|11|3|3.3|Suggestion-not-interruption audit|3.1, 3.2|P0|3.3|
|12|4|4.1|Fixed skill set|Phase 2|P0|4.1|
|13|4|4.2|Confirm-before-mutate|4.1|P1|4.2|
|14|5|5.1|Sensitive Content Filter|Phase 2|P1|5.1|
|15|5|5.2|Minimal permission gate|Phase 4|P0|5.2|
|16|5|5.3|Basic audit log|Phases 2, 4|P0|5.3|
|17|6|6.1|UI assembly|Phases 1–5|P0|6.1|
|18|7|7.1|Core-loop integration test|Phase 6|P0|7.1|
|19|7|7.2|Routing verification|7.1|P1|7.2|
|20|7|7.3|Failure-path test|7.1|P0|7.3|
|21|7|7.4|Security spot-checks|7.1|P1|7.4|
|22|8|8.1|Deploy & verify|Phase 7|P0|8.1|
|23|9|9.1|Rehearse scenario|Phase 8|P0|9.1|
|24|9|9.2|Record video|9.1|P0|9.2|
|25|10|10.1|Submission checklist|Phase 9|P0|10.1|

---

## 13. Development Checkpoint Tracker

Copy this into your own notes and update as you go.

```
PERSONAL AI — HACKATHON MVP — DEVELOPMENT CHECKPOINTS

Phase 0 — Foundation
[x] 0.1 Storage backend
[x] 0.2 Nebius/Nemotron connectivity
[x] 0.3 Streamlit skeleton

Phase 1 — Core AI
[x] 1.1 Chat loop

Phase 2 — Memory System
[x] 2.1 Memory extraction
[x] 2.2 Memory Inbox
[x] 2.3 Memory Timeline
[ ] 2.4 Conflict flagging
[ ] Phase 2 exit: full cross-session recall loop

Phase 3 — Proactive Intelligence
[ ] 3.1 Context-triggered surfacing
[ ] 3.2 Deadline-triggered surfacing
[ ] 3.3 Suggestion-not-interruption audit

Phase 4 — Skills & Tools
[ ] 4.1 Fixed skill set
[ ] 4.2 Confirm-before-mutate

Phase 5 — Security & Privacy
[ ] 5.1 Sensitive Content Filter
[ ] 5.2 Minimal permission gate
[ ] 5.3 Basic audit log

Phase 6 — UI Assembly
[ ] 6.1 Tab/page structure

Phase 7 — Testing & Reliability
[ ] 7.1 Core-loop integration test
[ ] 7.2 Routing verification
[ ] 7.3 Failure-path test
[ ] 7.4 Security spot-checks

Phase 8 — Deployment
[ ] 8.1 Deploy & verify

Phase 9 — Demo Preparation
[ ] 9.1 Rehearse scenario
[ ] 9.2 Record video

Phase 10 — Submission Readiness
[ ] 10.1 Full checklist (Section 15)
```

For each checkpoint, when you mark it, note: date, what was completed, tests passed, known issues, next step. Keep this brief — a line or two per checkpoint is enough.

---

## 14. Current State → Next Action Workflow

**If you are starting today:** open Section 13's tracker, find the first unchecked box (should be 0.1 if this is truly day one), read that subphase in Section 5, use its AI coding prompt as your starting point with your coding agent, and don't move to the next box until its checkpoint test passes.

**After each checkpoint:** update the tracker, then re-read the _next_ subphase's "Dependencies" line in Section 5 to confirm you actually have what it needs before starting.

**If something fails:**

```
Checkpoint failed
      ↓
Identify failing layer (use Section 11's pipeline diagram)
      ↓
Check the call log (which model tier, which purpose, success/failure)
      ↓
Check what changed since the last passing checkpoint
      ↓
Fix the root cause in that specific stage
      ↓
Re-run that stage in isolation if possible
      ↓
Re-run the full checkpoint test
      ↓
Only then continue to the next subphase
```

**What NOT to touch yet:** anything in Section 7 (Advanced Feature Path). If you find yourself wanting to add Knowledge Graph queries or a skill compiler mid-build, that's scope creep — note it in Section 7 for later and return to your current checkpoint.

---

## 15. Full System Completion Checklist (Hackathon Submission)

This is PRD §24, reproduced as your final-phase working checklist:

- [ ]  Working application — reachable, functioning demo
- [ ]  Nebius deployment actually used for inference (not just referenced)
- [ ]  NVIDIA Nemotron actually called, task-routed (Ultra vs. Nano/Super)
- [ ]  Personal AI Track alignment demonstrably present (persistent memory + proactive surfacing + minimal tool use)
- [ ]  Working demo URL, public, reachable at submission time
- [ ]  Public repository, fresh and separate, no dependency on prior personal projects
- [ ]  Open-source license chosen (currently TBD — resolve in Section 17)
- [ ]  README with setup instructions sufficient for independent reproduction
- [ ]  Model/Nebius documentation explaining how Nemotron + Nebius are used
- [ ]  Demo video, ≤3 minutes, following the PRD §23 arc
- [ ]  Live functionality demonstration, not just the video
- [ ]  Privacy/security explanation matching the actual, honest, scoped implementation (no overclaiming local-first architecture that wasn't built)
- [ ]  Feedback submission per hackathon process (TBD)
- [ ]  Card-verification / credit-activation status resolved (Section 17, item 3)

**Submission deadline: Oct 30, 2026, 10:00 AM PT.**

---

## 16. Requirement Traceability Matrix

|Requirement / Feature|Source|Phase|Subphase|Status|Validation|
|---|---|---|---|---|---|
|Persistent memory (FR-001)|PRD §17 / Master Plan FR-1|2|2.1–2.3|⬜|Cross-session recall test|
|Staged memory approval (FR-002)|PRD §17 / Master Plan FR-1.5|2|2.2|⬜|Only-approved-commits test|
|Memory Timeline (FR-003)|PRD §17 / Master Plan FR-1.6|2|2.3|⬜|Edit/delete round-trip|
|Conflict flagging (FR-004)|PRD §17 / Master Plan FR-1.4|2|2.4|⬜|Scripted contradiction test|
|Sensitive Content Exclusion (FR-005)|PRD §17 / Master Plan FR-1.11|5|5.1|⬜|Sensitive test statement|
|Context-Triggered Surfacing (FR-006)|PRD §17 / Master Plan FR-5, §7.2|3|3.1|⬜|Two-session reconnection test|
|Deadline-Triggered Surfacing (FR-007)|PRD §17 / Master Plan FR-5, §7.2|3|3.2|⬜|Approaching-deadline test|
|Suggestion Not Interruption (FR-008)|PRD §17 / Master Plan FR-5.2|3|3.3|⬜|Code audit|
|Minimal Permission Gate (FR-009)|PRD §17 / Master Plan FR-4.1|5|5.2|⬜|Disallowed-call rejection test|
|Confirm-Before-Mutate (FR-010)|PRD §17 / Master Plan FR-7.1|4|4.2|⬜|Mutating-action click test|
|Task-Routed Model Calls (FR-011)|PRD §17 (decision)|7|7.2|⬜|Log audit|
|Graceful Degradation (FR-012)|PRD §17 / Master Plan §23.1|7|7.3|⬜|Simulated API failure|
|Fixed Skill Invocation (FR-013)|PRD §17 / Master Plan FR-3.12|4|4.1|⬜|Name-invocation test|
|Basic Audit Log (FR-014)|PRD §17 / Master Plan FR-8.1|5|5.3|⬜|Log-entry-count test|
|**Selected features (Section 7.0 — your ten confirmed additions), in build order:**||||||

|Requirement / Feature|Source|Phase|Subphase|Status|Validation|
|---|---|---|---|---|---|
|People / Projects / Decisions (Knowledge Graph)|Detailed Plan §8.3, §20.5|**F — Wave A1**|—|Deferred|Entity + relationship query test|
|Daily Life Tracker|Detailed Plan §27.4|**F — Wave A2**|—|Deferred|Timeline-derived trend report test|
|Daily Priority Digest|Detailed Plan §27.3/§27.4|**F — Wave A3**|—|Deferred|Morning digest contains correct top items|
|Study + Exam Assistant|Detailed Plan §27.5, §13.2|**F — Wave A4**|—|Deferred|Weak-topic detection + revision-plan test|
|Voice / Image Input|Detailed Plan §7.4|**F — Wave B1**|—|Deferred|Voice command + screenshot OCR test|
|NL Skill Creation (Skill Compiler)|Detailed Plan §9.2, §9.3|**F — Wave B2**|—|Deferred|Described workflow compiles + runs correctly|
|Multi-App Integration Hub|Detailed Plan §10.1, §10.5|**F — Wave C1**|—|Deferred|Second app onboards without hub rework|
|Mail Check (read)|Detailed Plan §10.1, FR-3.9|**F — Wave C2**|—|Deferred|Inbox summary matches real inbox|
|Per-Task-Type Autonomy Ladder|Detailed Plan FR-7.1, §10.2|**F — Wave C3**|—|Deferred|Each task type enforces its configured tier|
|Autonomous Task Execution|Detailed Plan §10.2, §9.4|**F — Wave D1**|—|Deferred|Execute-with-approval action completes correctly|
|Put Mails For Me (draft/send)|Detailed Plan FR-7.1, §10.2|**F — Wave D2**|—|Deferred|Draft created; send requires explicit click|
|Work Assistant (research/analyze/track/solve)|Detailed Plan §9.4, §3.5 (Decision Memory)|**F — Wave D3**|—|Deferred|Multi-step research task completes unattended, cites Decision Memory|
|Cross-device sync (initial)|Detailed Plan §20.5 Phase 2, §18.4|**F — Parallel to Waves C/D**|—|Deferred|Change on device A visible on device B|

**Remaining Master Plan capabilities not yet selected** (still documented, still traceable, not currently on your build list):

|Requirement / Feature|Source|Phase|Subphase|Status|Validation|
|---|---|---|---|---|---|
|Full Proactive Intelligence Engine (all 5 trigger types)|Detailed Plan §7.2, §17.2|**F (Advanced, §7.1)**|—|Deferred|—|
|Full Automation Engine|Detailed Plan §17.1|**F (Advanced, §7.1)**|—|Deferred|—|
|Expanded integrations (Notion, Slack, GitHub, Zotero)|Detailed Plan §10.1|**F (Advanced, §7.1)**|—|Deferred|—|
|Memory Inbox multi-state refinement, TTL forgetting|Detailed Plan §8.4|**F (Advanced, §7.1)**|—|Deferred|—|
|Local/private model options|Detailed Plan §7.3, §15.2|**F (Advanced, §7.1)**|—|Deferred|—|
|Sandboxed execution|Detailed Plan §10.5|**F (Long-Term, §7.2)**|—|Deferred|—|
|Skill marketplace|Detailed Plan §9.3|**F (Long-Term, §7.2)**|—|Deferred|—|
|Digital Twin / simulation mode|Detailed Plan §9.4|**F (Long-Term, §7.2)**|—|Deferred|—|
|Personal API (skills-as-API)|Detailed Plan §18.1|**F (Long-Term, §7.2)**|—|Deferred|—|
|Full E2EE cross-device sync|Detailed Plan §16.3, §18.4|**F (Long-Term, §7.2)**|—|Deferred|—|
|Federated negotiation, smart-home/IoT, on-device acceleration|Detailed Plan §18.4, §20.5|**F (Long-Term, §7.2)**|—|Deferred|—|
|Export / data portability|Master Plan §15.2 / PRD §30 item 7|**F (Advanced, stretch: pre-submission if time allows)**|—|Deferred / Open|—|
|WhatsApp integration|—|**Explicitly excluded**|—|No legitimate personal-inbox API — see prior discussion|—|
|Autonomous ticket booking|Detailed Plan FR-7.1 ("Purchases: Always ask")|**Explicitly excluded** (booking _prep_ is Wave D3-adjacent; the purchase click stays manual)|—|—|—|

Every feature in the Master Plan's merged capability set (§3.5) traces to either an MVP row above, a sequenced Wave A–D row, or a documented remaining-capabilities row — none were silently dropped, matching both source documents' own stated completeness principle (Master Plan §28.6, Detailed Plan §28.6, PRD's closing coverage summary).

---

## 17. Open Decisions / Technical Unknowns

Carried directly from PRD §30, since these block or shape specific phases above:

1. **Deployment host** — ~~Hugging Face Spaces~~ **corrected to Streamlit Community Cloud** (as of Sep 2026, Hugging Face requires a paid plan to create any Space that runs a live Python backend — Gradio and Docker are both paywalled for free accounts, with only a 2-Space ZeroGPU exception that doesn't fit a Streamlit app; Static Spaces remain free but can't run server-side Python at all). Streamlit Community Cloud is genuinely free for public apps (GitHub-connected, ~1GB RAM, sleeps after ~12 hours idle). **Blocks Phase 8.** This also means local-disk storage (Phase 0.1) won't reliably survive a redeploy or a sleep/wake cycle on the free tier — decide whether that's acceptable for demo purposes or whether Phase 0.1 should target an external persistent store (e.g. a free-tier hosted Postgres such as Supabase) instead of a local SQLite file.
2. **Exact tool(s) in the fixed MVP skill set** — not finalized. **Blocks Phase 4.** Resolve before starting 4.1; also determines whether FR-8.4's untrusted-external-content handling is actually triggered.
3. ~~**Nebius credit/billing status** — card-verification blocker unresolved~~ **RESOLVED (confirmed):** $29.50 real account balance confirmed live in the Token Factory dashboard, plus $1.00 trial credit (23 days remaining). Genuinely usable, not just the default trial. **Phase 0.2 is unblocked.**
4. **Exact memory-ranking/relevance heuristic** — no formal scoring model decided. **Affects Phases 2.4 and 3.1.** A simple similarity/recency heuristic is an acceptable placeholder; don't over-engineer this before the core loop works.
5. **Product name** — may ship without one, using the generic persona framing. Doesn't block any phase.
6. **License** — not yet decided. **Blocks Phase 10 checklist item.**
7. **Export/data-portability feature** — a strong P1/P2 candidate; worth a go/no-go call once Phases 0–7 are solid and there's spare time before the deadline.
8. **Encryption-at-rest posture** — depends on the final deployment/storage choice (item 1). Resolve together.
9. **Whether P1 stretch items (conflict flagging, Sensitive Content Filter, confirm-before-mutate) make the final cut** — given the ~5–10 hrs/week budget. Recommendation: keep all three, since each is a single, small subphase (2.4, 5.1, 4.2) that meaningfully strengthens the demo's credibility relative to its build cost.
10. **Rust-daemon vs. generic-service architecture conflict** — inherited from the Master Plan, explicitly deferred, not this submission's problem. Relevant only when Section 7's Phase 3/Long-Term work resumes.
11. **Multi-user/authentication design** — deferred; no source document specifies this. Relevant only well into the Advanced Feature Path.
12. ~~**Official hackathon tooling requirement (NemoClaw/OpenShell/Hermes Agent/Nebius Serverless)** — unclear whether mandatory~~ **RESOLVED (verified against the live Devpost rules, nebiusglobalaihackathon.devpost.com/rules):** the Personal AI Track description lists NemoClaw, OpenShell, Hermes Agent, and Nebius Serverless as "**tools such as**" — suggested, not mandatory. The actual hard requirement (rules §4, "What to Create") is only: runs on Nebius Token Factory or Nebius AI Cloud + uses at least one NVIDIA open source model. Confirmed against the Judging Criteria too (rules §6, "Technological Implementation") — scored on effective use of Nebius Token Factory/AI Cloud + Nemotron, with no separate scoring for NemoClaw/OpenShell/Hermes. **This roadmap's Streamlit + Nemotron-via-Token-Factory plan is fully compliant as-is.** NemoClaw/OpenShell remain a strong, on-brand candidate specifically for Wave D1 (Autonomous Task Execution, Section 7.0) if the project is extended post-hackathon — their kernel-level agent sandboxing is a natural fit for that wave's actual execution engine, just not required to reach this submission's Definition of Done (Section 18).

**Also confirmed from the live rules while verifying the above (not previously in this roadmap):** Judging Period is Dec 1–15, 2026, with winners announced ~Jan 11, 2027 (after the Oct 30 submission deadline — no action needed now, just for awareness). There's also an unrelated $3,000 "Best Use of Tavily" bonus prize for any submission that makes a functional runtime call to the Tavily API — not part of this roadmap's scope, but worth knowing exists if a natural fit ever comes up (e.g. real web search inside Wave D3's Work Assistant, post-hackathon).

---

## 18. Final Definition of Done

For this specific submission — restated from PRD §29 as your single source of truth for "are we actually finished":

- **Product functionality:** the core loop (remember → persist → recognize relevance → act) works live on the deployed URL, end-to-end, without scripting around a failure.
- **AI behavior:** Nemotron Ultra and Nano/Super are both genuinely in use, task-routed as specified, not one model doing everything with the other referenced only nominally.
- **Memory:** staged approval and the Memory Timeline both function as specified.
- **Skills/tools:** the fixed skill set runs correctly and is invokable by name.
- **Security:** the minimal permission gate, confirm-before-mutate, and Sensitive Content Filter are all functioning.
- **Deployment:** the app is reachable at a public URL, independent of your own machine/session.
- **Testing:** the core-loop integration test and the failure-path test have both been run successfully against the _deployed_ instance, not just locally.
- **Documentation:** a README sufficient for independent reproduction, and an honest explanation of how Nebius/Nemotron are used that doesn't overclaim capabilities not built.
- **Demo:** a ≤3-minute video following the §23 arc, matching what the live app actually does.
- **Submission readiness:** every applicable item in Section 15's checklist is either done or explicitly, knowingly left TBD with a stated reason.

Nothing beyond this list is required for "done." Everything in Section 7 is deliberately, correctly, not part of this definition.