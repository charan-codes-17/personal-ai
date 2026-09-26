# A Personal AI — Product Requirements Document

**Status:** Implementation-ready draft, transformed from `Personal-AI-Unified-Master-Plan.md` (the merged Claude/ChatGPT/Gemini/Perplexity blueprint, "the Master Plan") for the **Nebius x NVIDIA Global AI Hackathon — Personal AI Track**.
**Author:** Solo builder (college student), competing individually.
**Traceability convention:** every requirement below carries an inline tag — **[SOURCE]** (explicitly present in the Master Plan, with a `§` section reference), **[DECISION]** (a locked, already-made project decision, sourced from prior planning), **[PROPOSAL]** (a suggested implementation approach not mandated by any source), or **[TBD]** (insufficient information to decide yet). Nothing in this document silently overrides a locked decision or invents a Master-Plan requirement.

> **Reading note on scope.** The Master Plan is a *unification of four independent full-product visions* — it deliberately preserves everything, including long-term, multi-year, non-hackathon-feasible ideas (Rust daemons, Neo4j clusters, federated inter-agent negotiation). This PRD preserves that full vision (Sections 1–21, 26) exactly as instructed, but Section 22 ("Hackathon MVP") is **not** a generic re-derivation of the Master Plan's own reconciled MVP — it is the actual, already-locked scope for this specific solo, ~5–10 hrs/week, Oct 30, 2026 submission. Where the two disagree, Section 22 wins for what gets built now, and the rest of the document remains the map of where the product can grow.

---

## 1. Product Overview

**Product name:** Not yet finalized. The Master Plan preserves eight-plus candidate names from its four source plans without resolving to one (Continuum, Threadline, Second Ledger, Anchor, Loopback, Nomi, Orbit, Kin, AXIS OS, Aether AI, Kratos, Sovereign, Keepsake, Steward, Axiom) **[SOURCE §27.1]**. For the hackathon submission, the working demo currently runs under a generic persona ("Riya") rather than a finalized brand **[DECISION]**. Naming is an open decision — see §30.

**One-line description:** A private, persistent-memory personal AI that remembers what a user is learning, building, and working on across sessions, proactively reconnects new context to past sessions, and — within permissions the user explicitly grants — turns recurring workflows into reusable, tool-using skills. **[SOURCE §1, synthesized from the four plans' one-sentence definitions]**

**Product vision:** Shift the category from *stateless conversational chatbot* to *persistent, proactive, executive personal AI operating system* — a system that is stateful (structured, user-owned memory), proactive (surfaces what needs attention before being asked), and executive (can act, not just describe), operating strictly under explicit, revocable, user-set permissions. **[SOURCE §1, §2.1, §2.2]**

**Product mission (synthesized, all four plans converge on this framing):** Eliminate the "context tax" of re-explaining oneself to memoryless tools, and the manual labor of reconstructing context a computer already has, by giving each user a private AI that accumulates their context over time and compounds in usefulness rather than resetting every session. **[SOURCE §1]**

**What the Personal AI is:** Not a chat window. It is a background system with five interlocking subsystems — a Memory Engine, a Context Engine, a Skill/Agent Runtime, a Permission Firewall, and a Proactive Intelligence Engine — fronted by a command-center UI in which chat is one tab among several. **[SOURCE §2.1, §6, §13.1]**

**What problem it solves:** See §3 (Problem Statement) for the full statement; in one line — conventional AI assistants forget everything between sessions, wait passively to be asked, and cannot act outside the chat window, which forces users to do the integration, memory, and follow-through work themselves. **[SOURCE §1]**

**Why this product should exist:** Every session with a stateless assistant starts from zero; the value of a user's accumulated context — decisions made, preferences stated, projects in flight — is thrown away and has to be manually rebuilt, repeatedly, across every tool the user touches. **[SOURCE §1, §2.1]**

**Core product philosophy (union of all four plans' stated principles — see §5 for the full list):** Ownership, earned autonomy, visible intelligence ("why do you remember this?" / "why did you do this?"), compounding usefulness, reversible automation, non-intrusive proactivity, execution over conversation, and architectural (not policy-level) privacy. **[SOURCE §2.3]**

**What makes it different from conventional AI chatbots/assistants:**

| Dimension | Conventional chatbot | This Personal AI |
|---|---|---|
| State | Resets every session | Persistent, structured, user-owned memory |
| Posture | Waits to be asked | Proactively surfaces what needs attention (with anti-annoyance controls) |
| Scope | Answers inside the chat window | Executes real actions across permitted tools, under a graduated autonomy model |
| Trust model | Implicit, all-or-nothing | Explicit, granular, revocable per app / action-type / data-type / time / context |
| Improvement | Model updates only | Accumulates user-specific procedural knowledge (skills) that compound over time |

**[SOURCE §1, §2.1, §2.4, §13.1, §27.6]**

---

## 2. Hackathon Alignment

*(This section explicitly distinguishes **required implementation** — must be true for the Oct 30, 2026 submission — from **planned implementation** — designed for, partially built — and **optional/future implementation** — described in the Master Plan but out of scope for this submission. See §22 for the authoritative MVP list.)*

### 2.1 Why the project qualifies as Personal AI

The product matches the track's own definition point for point: an always-on assistant, private by architecture, with persistent memory, reusable skills, user-selected tool/information access, and the ability to execute tasks across daily workflows — the same five pillars the Master Plan derives independently from four unrelated source plans (§3.5, §6). **[SOURCE §2.1, §3.5]**

### 2.2 How persistent memory is implemented

- **Required (MVP):** episodic memory with structured storage and simple relevance-based recall, a visible **Memory Timeline/Inspector** the user can scroll and correct, and a staged approval step before anything is committed long-term — the minimum viable slice of the Master Plan's Memory Inbox → Consolidation pipeline (§8.2, §11.1). **[DECISION + SOURCE §8, §11.1]**
- **Planned/partial:** semantic memory (stable facts/preferences) and basic entity linking. **[PROPOSAL, informed by §8.1]**
- **Deferred:** full Personal Knowledge Graph with graph traversal queries, decay/consolidation engine, cryptographic deletion. **[SOURCE §8.3, §8.4 — Phase 2/V2 per §20.5]**

### 2.3 How reusable skills are implemented

- **Required (MVP):** a small, fixed set of pre-built skill templates the assistant can run on trigger (aligned to the Master Plan's named MVP skill list: daily/session briefing, summary/extraction, context-reconnection) rather than the full natural-language Skill Compiler. **[DECISION, scoped from SOURCE §9.2–§9.3, §20.5]**
- **Deferred:** NL-to-skill compilation, skill versioning/chaining, skill marketplace. **[SOURCE §9 — V2/Long-Term per §20.5, §26]**

### 2.4 How tools/information access works

MVP tool surface is intentionally narrow (see §22); every tool call is gated by a permission check even in the narrow MVP, consistent with the Master Plan's non-negotiable principle that no integration is auto-granted (§10.2, FR-4.1). **[SOURCE §10.2, §4/FR-4 — DECISION on which tools are in scope]**

### 2.5 How task execution works

The MVP implements the low end of the five-tier autonomy ladder (§10.2) — Observe and Suggest, with any mutating/consequential action requiring explicit confirmation — rather than the Execute-with-Approval or Autonomous tiers, matching the "functionality over polish, core loop must work live" priority already set for this build. **[DECISION, scoped from SOURCE §10.2]**

### 2.6 Where NVIDIA open-source models fit — **required**

NVIDIA **Nemotron** is the mandatory open model family for this submission, split by task **[DECISION]**:
- **Nemotron Ultra** — reasoning, relevance judgment, and proactive-intervention decisions (the highest-stakes, lowest-frequency calls: "is this worth surfacing to the user right now?").
- **Nemotron Nano/Super** — chat responses and memory extraction/summarization (higher-frequency, lower-latency-sensitive calls).

This mirrors the Master Plan's own model-tiering principle — local/small models for classification, extraction, and context tagging; larger models reserved for complex reasoning (§7.3, §12.2) — adapted here to a Nemotron-only, hosted-inference context rather than the Master Plan's local-inference-first framing (§15.2), since the hackathon environment does not assume the user's own device runs the models. **[DECISION, informed by SOURCE §7.3, §12.2]**

### 2.7 Where Nebius Token Factory or Nebius AI Cloud fits — **required**

Nebius Token Factory/AI Cloud is the mandatory inference host for all Nemotron calls. This satisfies the Master Plan's "cloud model gateway" role (§12.2, §18.3) — the submission does not attempt the Master Plan's local-inference-first architecture (Ollama/llama.cpp/MLX, §7.3, §15.2); that is deferred. **[DECISION]**

### 2.8 How the architecture supports the hackathon requirements

The MVP implements a reduced slice of the Master Plan's unified logical layering (§5.5): Client (Streamlit) → Context assembly → Memory Engine (staged, approved writes) → Reasoning/Planning (Nemotron, task-routed) → a small Tool layer → a minimal Permission gate → an Audit trail. Layers the Master Plan treats as cross-cutting at full scale (Event Bus, Scheduler, Secrets Manager, sandboxed execution) are present only in simplified form or deferred — see §11 and §22. **[DECISION, mapped against SOURCE §5.5, §6]**

### 2.9 What should be demonstrated in the final demo

Per the locked demo scenario: a generic persona ("Riya") works across a learning/building/creating session; the assistant remembers a fact or decision from an earlier session, recognizes its relevance when a related topic resurfaces, and proactively (but non-intrusively) reconnects it — the Master Plan's own "prove one loop reliably: remember → persist → recognize relevance → act" MVP hypothesis (§20.1, Plan 1), independently echoed by Plan 2's MVP hypothesis: *"Does persistent context make an AI substantially more useful over repeated use?"* (§20.2). **[DECISION + SOURCE §20.1, §20.2]** Full demo script in §23.

### 2.10 How the product addresses the four judging criteria

| Judging criterion | How this PRD's scoped product addresses it |
|---|---|
| **Technological Implementation** | Working Nemotron-on-Nebius integration with genuine task-based model routing (not a single model doing everything); a real, live memory-write → retrieval → relevance loop, not a scripted demo. |
| **Design** | Command-center framing (not chat-only) carried through even at MVP scale — a visible Memory Timeline and staged approval UI, not a bare chatbot — consistent with all four source plans' shared rejection of chat-only UX (§13.1). |
| **Potential Impact** | Addresses a concrete, self-experienced problem (a student's own multi-threaded learning/building context lost between sessions) rather than a generic "AI assistant" pitch. |
| **Quality of the Idea** | The persistent-memory-with-approval loop and task-routed Nemotron usage are a non-obvious, defensible core, aligned with the Master Plan's own identified "most defensible capability" theme — the memory/context/permission stack, not the model (§27.7). |

**[DECISION, mapped against SOURCE §27.7]**

---

## 3. Problem Statement

**The target problem [SOURCE §1]:** Users with an ongoing, multi-threaded digital life — students, developers, professionals, researchers, creators — pay a recurring "context tax": re-explaining their situation to tools that remember nothing between sessions, and manually reconstructing context (decisions made, where a project stands, what was already tried) that the computer already touched but never retained.

**Existing limitations of conventional AI assistants [SOURCE §1, §2.1]:**
- Stateless: each session starts from zero.
- Reactive: they wait to be asked and cannot notice something needs attention on their own.
- Chat-bound: they cannot act outside the conversation window.
- Fragmented: context is scattered across email, docs, calendars, notes, browsers, messaging, and devices, with no system reconstructing it.
- Opaque: unclear what is remembered, where it lives, or how it is used.

**User pain points [SOURCE §1, synthesized]:**
- Repeating the same background/context at the start of every new conversation.
- Losing track of decisions, rationale, and half-finished commitments across a busy week.
- No single place that connects "what I'm learning" to "what I'm building" to "what I said I'd do."

**Why current solutions are insufficient [SOURCE §1]:** Chat history is not memory — it is an unstructured log the user has to re-read and re-explain from, not a queryable, structured, evolving model of the user's actual context (Plan 2, §2.2 "Persistent memory" definition).

**Why privacy, ownership, persistent context, memory, autonomy, and extensibility matter [SOURCE §2.3, §15.1]:** A system that remembers a user's life and work is only trustworthy if the user, not the vendor, controls what is remembered, who can see it, and what it is allowed to do — privacy and control are treated as architecture, not policy, across all four source plans.

**The specific opportunity this Personal AI addresses [DECISION, scoped]:** For this submission specifically — a student's own cross-session learning/building/creating context, proactively reconnected without being asked, demonstrated live rather than scripted.


---

## 4. Target Users

*The Master Plan's persona lists (students, developers/engineers, professionals/knowledge workers, researchers, creators, entrepreneurs) are the union across all four source plans [SOURCE §1]. This PRD narrows to the personas actually relevant to the locked solo build, without inventing new ones.*

### 4.1 Primary persona — Student / builder (the demo persona, "Riya")

- **Who they are:** A student juggling coursework, self-directed learning (AI/ML), and personal build projects, across multiple sessions per week. **[DECISION]**
- **Goals:** Keep learning and building threads connected across sessions; avoid re-explaining project context every time; get proactively reminded when new context connects to something from before. **[DECISION, aligned with SOURCE §1]**
- **Problems:** Context loss between sessions; forgetting earlier decisions/rationale; no single place tying "what I'm learning" to "what I'm building." **[SOURCE §1]**
- **How they currently solve this:** Manually re-reading old notes/chat history; re-explaining background at the start of each new AI conversation. **[SOURCE §1, §2.2]**
- **How the Personal AI helps:** Persists memory across sessions, and proactively resurfaces relevant past context without being asked (Context-triggered proactivity, §7.2). **[SOURCE §7.2]**
- **Most important use cases:** Session-to-session continuity on a learning/building thread; recognizing when a new question relates to a past decision; a visible, correctable record of what's been remembered. **[DECISION]**
- **Technical expertise:** High (comfortable with a plain, even unpolished, functional UI; values working core loop over visual polish). **[DECISION]**

### 4.2 Secondary personas (represented in the Master Plan; informative for the broader vision, not required for MVP)

- **Developer/engineer** — repo activity, standup drafts, code-review workflows. **[SOURCE §13.2]**
- **Professional/knowledge worker** — meeting-prep briefings, decision memory across projects. **[SOURCE §8.3, §13.2]**
- **Creator** — content-pipeline dashboards. **[SOURCE §13.2]**

Do not build persona-specific features for 4.2 in the hackathon scope; they inform the product's future breadth (§6, Future Scope) only. **[DECISION]**

---

## 5. Product Principles

*Only principles the Master Plan explicitly and consistently states are listed; no principle is invented.* **[SOURCE §2.3, §27.9]**

1. **Ownership** — the user owns their data, memory, and configuration.
2. **Earned autonomy** — the assistant starts conservative (observe/suggest) and gains execution rights only through explicit, per-domain authorization; never a global switch.
3. **Visible intelligence / transparency** — the user can always ask "why do you remember this?" and "why did you do this?" and get a real, traceable answer.
4. **Compounding usefulness** — every approved memory and skill makes future interactions more useful, not less, as data accumulates.
5. **Reversible automation / human control** — the assistant can act, but the user can pause, inspect, correct, undo, and revoke at any time.
6. **Non-intrusive proactivity** — optimizes for usefulness per interruption, not number of interventions; "do nothing" is a valid default output.
7. **Execution over conversation** — the product competes on continuity, ownership, context, memory, execution, and trust, not "better answers."
8. **Architectural (not policy) privacy** — privacy is engineered into where data lives and how it moves, not promised in a policy document.
9. **Explicit permissions / graceful failure** — nothing is auto-granted; failures degrade gracefully (halt, log, notify, offer retry) rather than crashing or silently retrying forever.

**MVP-scope note [DECISION]:** principles 1, 2, 3, 5, 6, and 9 are directly testable in the hackathon build (staged memory approval, visible timeline, low-autonomy default, undo/correct, non-intrusive surfacing, graceful degradation on model/tool failure). Principle 8's full architectural form (local-first, user-held encryption keys) is deferred — the MVP instead applies data minimization and scoped, revocable API access as its practical privacy floor (see §16).

---

## 6. Product Scope

### 6.1 In Scope — Full Product Vision (from the Master Plan; what "done" eventually looks like)

Everything catalogued in the merged capability set (§3.5 of the Master Plan): multi-layer persistent memory with Memory Inbox and Timeline; Personal Knowledge Graph; reusable Skills/Mini-Agents with versioning and chaining; a granular Permission Firewall; the 5-tier Autonomy Framework; a Proactive Intelligence Engine with anti-annoyance controls; a Context Engine; a Trust & Safety layer (audit log, receipts, undo, panic button, secrets manager, prompt-injection defense); a privacy-first/local-first hybrid architecture; an Automation Engine; self-improving workflow discovery; a command-center UI; multi-modal interaction; a Digital Twin/simulation mode; temporary agents; decision memory; unfinished-commitment detection; cross-app task continuity; sandboxed execution; a Personal API; and (long-term) federated inter-agent negotiation. **[SOURCE §3.5]**

### 6.2 In Scope — Hackathon MVP (the actual, locked build; authoritative list is §22)

A persistent-memory personal AI with: staged memory writes (Memory Inbox pattern, simplified), a visible Memory Timeline/Inspector, context-triggered and deadline-triggered proactive surfacing only, a small fixed skill set, Nemotron (task-routed) on Nebius Token Factory/AI Cloud, a Streamlit frontend, and a working demo URL. **[DECISION]**

### 6.3 Out of Scope (for the hackathon submission specifically)

- Full Personal Knowledge Graph with relational graph queries and entity resolution. **[SOURCE §8.3 — deferred, DECISION]**
- Natural-language Skill Compiler, skill versioning/chaining/marketplace. **[SOURCE §9 — deferred, DECISION]**
- Scheduled and opportunity-based and autonomous-completion proactive triggers (only context + deadline triggers ship). **[DECISION]**
- Local/on-device model inference (Ollama/llama.cpp/MLX); local-first storage architecture. **[SOURCE §7.3, §15.2 — deferred, DECISION]**
- Sandboxed (Wasm/container) execution isolation; a dedicated Secrets Manager/credential vault beyond basic API-key handling. **[SOURCE §10.5, §12.2 — deferred, DECISION]**
- Digital Twin/simulation mode, temporary/ephemeral agents, autonomous research missions. **[SOURCE §9.4 — deferred, DECISION]**
- Multi-modal interaction (voice, vision/OCR, screen understanding). **[SOURCE §7.4 — deferred, DECISION]**
- Multi-user authentication/account system, cross-device sync. **[SOURCE §14 — a gap even in the Master Plan; not attempted, DECISION]**
- Memory Graph *visualization* specifically (explicitly cut, even though basic memory storage is in scope). **[DECISION]**

### 6.4 Future Scope (belongs to the larger vision; explicitly deferred past this submission)

Everything in §6.1 not listed in §6.2, following the Master Plan's own reconciled Phase 2 (V2) and Phase 3 (Long-Term) groupings (§20.5): full Knowledge Graph, Skill Compiler/marketplace, full Automation Engine, multi-modal support, cross-device sync, local/private model options, Digital Twin, federated negotiation, OS-level integration. **[SOURCE §20.5, §26]**

---

## 7. Feature Requirements

*This is the comprehensive feature inventory. Each entry traces to its Master Plan section. Priority uses P0 (critical to this submission) / P1 (high, strengthens the submission if time allows) / P2 (medium, V2) / P3 (future/optional). Every feature from the Master Plan's merged capability set (§3.5) is represented below; none are silently dropped — deferred ones are marked P2/P3 rather than omitted.*

### 7.1 Persistent Memory (Core)

- **Purpose:** Retain user-approved information across sessions and retrieve it when relevant to a later interaction. **[SOURCE FR-1]**
- **User value:** No more re-explaining context every session; compounding usefulness.
- **Description:** Structured memory records (not raw chat logs), each carrying source, timestamp, and approval status at minimum (full metadata set is P2 — see §13). **[SOURCE FR-1.2]**
- **User interaction:** New candidate memories are shown to the user for approval before being committed (simplified Memory Inbox); the user can browse, correct, or delete any stored memory via the Memory Timeline. **[SOURCE FR-1.5, FR-1.6]**
- **Functional behavior:** On each session, the system judges whether new information is worth remembering (LLM judgment step, §11.1 step 4), stages it, and on approval commits it to the store.
- **Inputs:** Conversation turns, explicit user statements.
- **Outputs:** Stored memory records; a "why do you remember this?" explanation on request. **[SOURCE FR-1.3]**
- **Dependencies:** Nemotron (extraction/judgment), storage backend.
- **Permissions/security:** Sensitive categories (health, finance, passwords) excluded from extraction by default. **[SOURCE FR-1.11]** — P1 for MVP; a basic keyword/category filter is P0-adjacent given privacy is a first-class requirement.
- **Failure/edge cases:** Contradictory new memory vs. existing memory must be flagged for user resolution, never silently overwritten. **[SOURCE FR-1.4]**
- **Acceptance criteria:** A fact stated in session 1 is correctly recalled and applied in session 2 without the user restating it; the user can see, correct, and delete it.
- **Priority:** **P0**

### 7.2 Memory Inbox (staged approval)

- **Purpose:** Prevent silent, unreviewed memory writes. **[SOURCE FR-1.5, §8.4]**
- **Description:** Candidate memories are held pending Save/Modify/Ignore/Never-remember action.
- **Priority:** **P0** (simplified single-tier version; full multi-state staging is P1)

### 7.3 Memory Timeline / Inspector

- **Purpose:** Visible, scrollable, correctable record of everything remembered. **[SOURCE FR-1.6]**
- **User interaction:** Scroll, correct, delete individual records; bulk purge is P2 (deferred). **[SOURCE FR-1.6]**
- **Priority:** **P0** — explicitly confirmed as MVP scope, not a stretch goal. **[DECISION]**

### 7.4 Natural-language memory correction ("forget my old address")

- **Purpose:** Let users correct memory conversationally. **[SOURCE FR-1.7]**
- **Priority:** **P2** (deferred — no cascading graph edges to update yet since the Knowledge Graph itself is deferred)

### 7.5 Memory TTL / expiration rules

- **Purpose:** Auto-forget temporary information after a set period. **[SOURCE FR-1.8]**
- **Priority:** **P2**

### 7.6 Cryptographic deletion

- **Purpose:** Irrecoverable deletion via key destruction. **[SOURCE FR-1.9]**
- **Priority:** **P3** (requires the local-first encryption architecture that is out of scope for this submission)

### 7.7 Three explicit memory states (Remember / Temporary / Never Remember) + Private Sessions

- **Purpose:** Give users a simple, explicit control over what persists. **[SOURCE FR-1.10]**
- **Priority:** **P1** — a minimal two-state version (Remember / Never Remember) is achievable at MVP; full three-state plus "Incognito Mode" is P2.

### 7.8 Sensitive Content Filter

- **Purpose:** Exclude health/finance/password-like content from extraction by default. **[SOURCE FR-1.11]**
- **Priority:** **P1**, given privacy is a first-class requirement even at MVP scale (§16).

### 7.9 Personal Knowledge Graph

- **Purpose:** Relational store of People/Projects/Documents/Meetings/Tasks/Decisions/Deadlines with provenance, enabling multi-hop queries ("what's blocking this project?"). **[SOURCE FR-2, §8.3]**
- **Priority:** **P2** (Phase 2/V2 — deferred past this submission per §6.3)

### 7.10 Reusable Skills (NL → structured workflow, full compiler)

- **Purpose:** Turn a natural-language description into a versioned, permission-scoped, triggerable workflow. **[SOURCE FR-3]**
- **Priority:** **P2** for the full compiler. **P0** for a *fixed*, pre-built subset (daily/session briefing, summarization, context-reconnection) run through a simplified version of the same lifecycle (Describe → Approve → Execute), consistent with the Master Plan's own MVP skill list (§9.2, §20.5). **[DECISION]**

### 7.11 Skill versioning, chaining, marketplace

- **Purpose:** Git-like skill history, one skill's output triggering another, community sharing. **[SOURCE FR-3.4, FR-3.5, §26]**
- **Priority:** **P3**

### 7.12 Permission Firewall / Capability-Based Access Control

- **Purpose:** No integration or action is auto-granted; access is scoped per app/action-type/data-type/time/context and revocable. **[SOURCE FR-4, §10.2, §10.3]**
- **Priority:** **P0** for a minimal version (explicit per-tool allow list, confirm-before-execute for anything mutating); **P2** for the full multi-axis granularity (time-limited, location-based, network-based scoping).

### 7.13 5-Tier Autonomy Framework

- **Purpose:** Configurable autonomy per task-type (Observe/Suggest/Prepare-Draft/Execute-with-Approval/Autonomous), never global. **[SOURCE FR-7, §10.2]**
- **Priority:** **P0** for Observe + Suggest tiers only (matches the "functionality over polish" MVP priority and the low-autonomy-by-default principle); **P2** for the full 5-tier ladder including Execute-with-Approval and Autonomous.

### 7.14 Proactive Intelligence Engine

- **Purpose:** Continuously evaluate signals and decide whether to surface something, with "do nothing" as a valid default. **[SOURCE FR-5, §7.2]**
- **Priority:** **P0**, scoped to **context-triggered and deadline-triggered** signals only. **[DECISION]** Scheduled, opportunity-based, and autonomous-completion triggers are **P2** stretch goals. **[DECISION, mapped to SOURCE §7.2's five trigger types]**

### 7.15 Anti-annoyance controls (quiet hours, thresholds, frequency caps, suggestion-vs-interruption)

- **Purpose:** Prevent the proactive engine from becoming a nuisance. **[SOURCE FR-5.3]**
- **Priority:** **P1** — at minimum, a suggestion-only (inbox, never push-interrupt) MVP behavior satisfies the spirit of this requirement without full threshold/quiet-hours tuning, which is **P2**.

### 7.16 Context Engine

- **Purpose:** Fuse available signals (active project/topic, recent conversation, time) into "what does the user probably need right now," treated as evidence, not truth. **[SOURCE FR-6, §7.1]**
- **Priority:** **P0**, scoped to conversation content and explicit session/project labels only (no OS-level window/accessibility-API ingestion, no location, no calendar integration at MVP). **[DECISION]**

### 7.17 Trust & Safety (audit log, action preview, undo, panic button, secrets manager, prompt-injection defense)

- **Purpose:** Make every consequential action previewed, logged, undoable, and haltable; treat all externally fetched content as untrusted data. **[SOURCE FR-8]**
- **Priority:** **P0** for an audit log (every memory write and skill run recorded) and prompt-injection-aware handling of any fetched content; **P1** for a manual "pause" control; **P2** for full one-click undo and a dedicated secrets manager (MVP has minimal external tool/credential surface, lowering this risk).

### 7.18 Automation Engine (triggers, conditions, actions, retries)

- **Purpose:** Scheduled/event/state-driven triggers with conditional branching and error handling. **[SOURCE FR-9, §17.1]**
- **Priority:** **P2** — MVP proactivity (§7.14) is a narrow special case of this, not the general engine.

### 7.19 Multi-modal interaction (voice, vision/OCR, documents, screen)

- **Purpose:** Voice, image/OCR, document parsing, screen understanding. **[SOURCE FR-10, §7.4]**
- **Priority:** **P3**

### 7.20 Command-Center UI (Home/briefing, Chat, Memory Browser, Skills, Automation, Activity, Permissions)

- **Purpose:** Reject chat-only UX in favor of a dashboard with several first-class views. **[SOURCE §13.1, §13.6]**
- **Priority:** **P0** for a reduced set — Home/briefing + Chat + Memory Timeline — implemented as Streamlit tabs/pages. **[DECISION]** Full navigation set (Skills library, Automation dashboard, Permission Center, Knowledge Graph Viewer, Agent Monitor) is **P2/P3**.

### 7.21 Decision Memory ("why am I doing this")

- **Purpose:** Track rationale behind decisions, not just the decision itself. **[SOURCE §3.5, §27.2–§27.4]**
- **Priority:** **P2**

### 7.22 Unfinished-commitment / "forgotten things" detection

- **Purpose:** Surface dropped commitments the user hasn't returned to. **[SOURCE §3.5]**
- **Priority:** **P2** — conceptually close to the deadline-triggered proactivity in scope for MVP (§7.14), but the general-purpose detector is deferred.

### 7.23 Cross-app task continuity

- **Purpose:** Continue a task started in one tool inside another. **[SOURCE §3.5]**
- **Priority:** **P3** (requires the broader Tool/Integration Hub, out of scope)

### 7.24 Sandboxed skill/tool execution (Wasm/container)

- **Purpose:** Contain the blast radius of a compromised integration. **[SOURCE §10.5]**
- **Priority:** **P3** — MVP's minimal tool surface and low autonomy tiers substitute for this at reduced risk.

### 7.25 Personal API (skills-as-API)

- **Purpose:** Expose the user's own skills to external systems. **[SOURCE §18.1]**
- **Priority:** **P3**

### 7.26 Digital Twin / simulation mode

- **Purpose:** Simulate the user's likely response/decision for low-stakes pre-testing. **[SOURCE §9.4]**
- **Priority:** **P3**

### 7.27 Temporary / ephemeral agents

- **Purpose:** Spin up a bounded, single-mission agent with no persistent footprint. **[SOURCE §9.4]**
- **Priority:** **P3**

### 7.28 Federated / inter-agent negotiation

- **Purpose:** Two users' personal AIs coordinate without exposing raw data. **[SOURCE §18.4, §26]**
- **Priority:** **P3** (multi-year, long-term vision item — not remotely in scope)

---

## 8. Core Personal AI Capabilities

*Organized into the domains the Master Plan actually supports; each domain states the required functionality, distinguishing MVP-scope behavior from full-vision behavior.*

**Conversational intelligence** — Nemotron-driven chat, task-routed (Nano/Super for chat, Ultra for reasoning-heavy relevance/intervention calls). **[DECISION + SOURCE §7.3]**

**Persistent memory** — see §7.1–§7.8. MVP: episodic memory with staged approval and a visible timeline. Full vision: episodic + semantic + procedural + preference + project + temporary layers (§8.1). **[SOURCE §8.1]**

**Context management** — MVP: conversation- and session-label-based context only. Full vision: active-window, clipboard, calendar, and location signal fusion into a continuously updated context vector (§7.1). **[SOURCE §7.1]**

**User profile/identity** — Single-user, locally-scoped identity for the demo persona; no login/account system (matches the Master Plan's own acknowledged gap, §14). **[SOURCE §14]**

**Skills** — MVP: fixed pre-built templates. Full vision: NL-to-skill compiler with versioning/chaining (§9). **[SOURCE §9]**

**Agents** — MVP: none (single assistant loop). Full vision: temporary agents, multi-agent orchestration, autonomous research missions (§9.4). **[SOURCE §9.4]**

**Planning** — MVP: single-step reasoning per turn. Full vision: multi-step goal tracking via the Reasoning & Planning Layer (§7.3). **[SOURCE §7.3]**

**Tool use** — MVP: a small, explicit, permissioned tool set. Full vision: a full Tool/Integration Hub with sandboxed adapters (§10). **[SOURCE §10]**

**Workflow execution / automation** — MVP: none beyond proactive surfacing. Full vision: the full Automation Engine (§17.1). **[SOURCE §17.1]**

**Proactive assistance** — MVP: context- and deadline-triggered suggestions only, inbox-style (never push-interrupting). Full vision: five trigger types with anti-annoyance controls (§7.2). **[SOURCE §7.2]**

**Knowledge retrieval** — MVP: simple relevance-based recall over stored memories. Full vision: combined graph traversal + vector/semantic search (§8.3, FR-2.5). **[SOURCE FR-2.5]**

**Personal information management** — MVP: the Memory Timeline functions as a lightweight personal record. Full vision: full Knowledge Graph with entity resolution (§8.3). **[SOURCE §8.3]**

**Integrations** — MVP: minimal, explicit (Nebius/Nemotron only, plus whatever demo-supporting storage is used). Full vision: the full integration surface (§10.1). **[SOURCE §10.1]**

**Notifications** — MVP: in-app suggestion surfacing only, no push notifications. Full vision: suggestion-vs-interruption distinction with configurable thresholds (§7.2). **[SOURCE §7.2]**

**Multimodal capabilities** — Out of scope for MVP; full vision in §7.4. **[SOURCE §7.4]**

**Security and permissions** — MVP: explicit per-tool allow list, confirm-before-mutate. Full vision: multi-axis CBAC (§10.3). **[SOURCE §10.3]**

**Personalization** — MVP: memory-driven personalization (recalled facts/preferences shape responses). Full vision: adds procedural memory of *how* the user works (§8.1). **[SOURCE §8.1]**

**Learning/adaptation** — MVP: none beyond memory accumulation. Full vision: self-improving workflow discovery (Observe→Suggest→Approve→Learn→Automate, §17.2). **[SOURCE §17.2]**

**Observability** — MVP: a basic activity/audit log of memory writes and skill runs. Full vision: full Activity & Audit Stream, System Tray status, Agent Monitor (§25). **[SOURCE §25]**

**Self-management** — MVP: none. Full vision: Memory Retention Decay Engine, dead-link pruning, Consolidation Engine (§8.2, §25). **[SOURCE §8.2, §25]**

---

## 9. User Experience

*MVP-scope UX only, per the Streamlit-frontend decision; full-vision UX (ambient overlay, ambient ummand center) is described in §13 of the Master Plan and referenced here as future direction, not built now.*

- **First-time onboarding [DECISION]:** the demo persona is pre-seeded (no live sign-up flow needed for a hackathon demo); a real product would need an onboarding flow the Master Plan itself does not specify (§14 gap).
- **Initial setup / permissions [DECISION]:** at MVP scale, the "permission" step is implicit in the fixed, narrow tool surface rather than a configurable Permission Center; a one-time acknowledgment that memory will be stored is the practical minimum equivalent to the Master Plan's consent step (§10.2).
- **Connecting tools [P2]:** deferred — no user-facing tool-connection flow at MVP.
- **Creating/configuring the AI [P2]:** deferred — no skill-authoring UI at MVP; skills are pre-built.
- **Normal daily interaction:** chat-first (Streamlit), with a Memory Timeline tab and (if time allows) a simple Home/briefing view — the smallest faithful slice of the Master Plan's command-center principle (§13.1). **[DECISION]**
- **Memory interactions [P0]:** approve/ignore a staged memory; browse/correct/delete via the Timeline (§7.1–§7.3).
- **Skill discovery [P1]:** the fixed skill set is visible and invocable by name, echoing FR-3.12's "invokable by name" requirement even without the full compiler. **[SOURCE FR-3.12]**
- **Task execution / automation [deferred]:** no automation dashboard at MVP.
- **Notifications [P0, minimal]:** in-app suggestion surfacing only.
- **Errors [P0]:** on a model/tool failure, halt gracefully, log it, and show an unobtrusive message — consistent with FR-8/§23.1's graceful-degradation requirement even at reduced scope. **[SOURCE §23.1]**
- **Confirmation flows [P1]:** any mutating action (a memory deletion, a skill run with a side effect) requires an explicit click.
- **Privacy controls [P1]:** a visible "forget this" action per memory record satisfies the minimum viable version of user-controlled deletion (§15.1).
- **Settings [P2]:** deferred beyond the minimum memory controls above.
- **Data management [P1]:** export is **not** committed for MVP (no time-boxed requirement states it must ship) but is flagged as a strong P1/P2 given the Master Plan's "data portability, not platform captivity" principle (§15.2). **[SOURCE §15.2]**
- **Shutdown/reset/deletion behavior [P1]:** a full-store reset/delete-all control is a reasonable minimum privacy control even at MVP scale.

---

## 10. User Journeys

### 10.1 Journey — Context reconnection (the core demo loop) **[DECISION, the primary journey to be demonstrated]**

1. **User goal:** Not have to re-explain a decision or fact from an earlier session.
2. **Trigger:** User opens a new session and raises a topic related to something discussed previously.
3. **User action:** Asks a question or states a new fact in the related topic area.
4. **AI reasoning/action:** Context Engine flags the topic as related to stored memory; Nemotron (Ultra, for the relevance judgment) scores whether the connection is worth surfacing.
5. **Tool/skill execution:** None required — pure memory retrieval + reasoning.
6. **Data/memory interaction:** Retrieves the relevant prior memory record(s); does not silently assume — states the connection and lets the user confirm/correct it (evidence-not-truth principle, FR-6.2). **[SOURCE FR-6.2]**
7. **Result:** The assistant proactively reconnects the new context to the old, in a natural response.
8. **Confirmation/feedback:** User can affirm, correct, or dismiss the connection; any new fact from this exchange goes through the Memory Inbox staging step again.
9. **Failure scenarios:** If confidence is low, the system says nothing (silent default is valid, FR-5.1) rather than guessing.

### 10.2 Journey — Staged memory write

1. **User goal:** Have a stated fact or decision remembered for future sessions.
2. **Trigger:** User states something judged worth remembering during conversation.
3. **User action:** Continues the conversation normally; no special "remember this" command required (though one may exist as a shortcut, P2).
4. **AI reasoning/action:** Extraction/judgment step (Nemotron Nano/Super) proposes a candidate memory.
5. **Tool/skill execution:** None.
6. **Data/memory interaction:** Candidate is staged (Memory Inbox); on approval, committed to the store with source and timestamp.
7. **Result:** A new, retrievable memory record exists.
8. **Confirmation/feedback:** User sees the staged item and can Save/Ignore (Modify and Never-remember are P1/P2 refinements). **[SOURCE FR-1.5]**
9. **Failure scenarios:** If the new fact contradicts an existing one, flag the conflict rather than overwrite. **[SOURCE FR-1.4]**

### 10.3 Journey — Deadline-triggered proactive nudge

1. **User goal:** Be reminded of an approaching, still-incomplete commitment.
2. **Trigger:** A stored memory includes a deadline-bearing item that is approaching and unresolved.
3. **User action:** None — this is proactive.
4. **AI reasoning/action:** Deadline-trigger check (part of the narrow MVP proactivity scope, §7.14) fires; confidence-gated before surfacing.
5. **Tool/skill execution:** None.
6. **Data/memory interaction:** Reads the relevant memory record(s).
7. **Result:** A suggestion (not a push interruption) appears the next time the user is in-session.
8. **Confirmation/feedback:** User can mark it resolved, dismiss, or snooze.
9. **Failure scenarios:** If the deadline data is stale or ambiguous, the nudge is suppressed rather than shown low-confidence.

*(Full-vision journeys — skill creation from a repeated workflow, cross-app task continuity, autonomous research missions, Digital Twin simulation — are preserved in the Master Plan §27.5 and are not built for this submission; they inform §6.4 Future Scope only.)* **[SOURCE §27.5]**

---

## 11. System Architecture

*MVP architecture only. The Master Plan's full unified logical layering (§5.5) — Client/Presentation, Context Engine, Personal Memory System, Reasoning & Planning, Skill & Agent Runtime, Permission/Autonomy Firewall, Tool & Integration Layer, Execution Sandbox, plus cross-cutting Event Bus/Scheduler/Secrets Manager/Encryption/Audit Log/Policy Engine/Observability/Identity — is the map this MVP is a reduced slice of; layers not present at MVP are marked accordingly.*

| Layer | Full vision (Master Plan §5.5) | This submission (MVP) |
|---|---|---|
| Client/interface | Chat UI, ambient overlay, command-center dashboard, spatial canvas, voice, mobile/desktop shells | Streamlit web app — chat + Memory Timeline (+ Home/briefing if time allows) **[DECISION]** |
| AI/model layer | Local + cloud model gateway, model-agnostic | Nemotron only, hosted on Nebius Token Factory/AI Cloud, task-routed (Ultra vs. Nano/Super) **[DECISION]** |
| Agent/orchestration | Skill & Agent Runtime, multi-agent orchestration | Single assistant loop; no agent orchestration **[DECISION]** |
| Memory layer | Working/episodic/semantic/procedural/preference/project/temporary + Consolidation Engine | Episodic memory only, with staged approval; no decay/consolidation engine **[DECISION]** |
| Knowledge/context layer | Personal Knowledge Graph + Context Engine (multi-signal fusion) | No graph; context = conversation + session labels only **[DECISION]** |
| Skills layer | NL-to-skill compiler, versioning, chaining | Fixed, pre-built skill templates **[DECISION]** |
| Tool/integration layer | Full Tool/Integration Hub, sandboxed adapters | Minimal, explicit tool surface **[DECISION]** |
| Execution layer | Wasm/container-sandboxed, transactional undo | Direct execution; no sandbox isolation; manual pause only **[DECISION]** |
| Security/privacy layer | Zero-knowledge local-first, CBAC, secrets vault | Basic access scoping + Sensitive Content Filter; no vault **[DECISION]** |
| Storage layer | Vector DB + Graph + relational DB, encrypted at rest | Simple structured store (P0); encryption at rest is **P1/TBD** pending hosting choice |
| Observability layer | Activity/Audit Stream, Agent Monitor, System Tray | Basic audit log of memory writes and skill runs **[DECISION]** |
| Infrastructure layer | Local daemon (Rust) or generic service + local/cloud hybrid | Hosted web app (Streamlit) + Nebius-hosted inference; deployment target TBD, Hugging Face Spaces recommended **[DECISION]** |

*Note on the Master Plan's flagged architectural conflict (§5.5, §27.9, §28.3.1):* the Master Plan leaves open whether the eventual full-scale system should follow Plan 3's Rust-daemon/Wasm-sandbox stack or Plan 4's generic-service/container-sandbox stack. **This submission does not resolve that conflict** — it sidesteps it entirely by building a hosted web app rather than a local daemon, which is appropriate for a demo but explicitly not a decision about the long-term architecture. **[SOURCE §5.5, §28.3.1 — TBD, out of scope for MVP resolution]**

---

## 12. AI Architecture

**Model responsibilities [DECISION]:**
- **Nemotron Ultra** — relevance scoring for proactive surfacing (§10.3 journey step 4), memory-conflict judgment, any multi-step reasoning the demo requires.
- **Nemotron Nano/Super** — turn-by-turn chat responses, memory-candidate extraction/summarization from conversation.

**Model routing:** task-based, not confidence-based fallback — each call type is routed to a fixed model tier by design, rather than escalating dynamically. **[DECISION]** *(The Master Plan's local-vs-cloud hybrid-routing pattern, §7.3, is not applicable here since both tiers are cloud-hosted on Nebius; the analogous principle — route by task complexity/stakes, not by a single model doing everything — is preserved.)*

**Reasoning & planning:** single-turn reasoning per interaction (Nemotron Ultra for the relevance/intervention decision); no multi-step goal-tracking planner at MVP. **[DECISION, scoped from SOURCE §7.3]**

**Tool calling:** MVP's minimal tool surface means tool-calling is simple and low-frequency; no general-purpose tool-orchestration loop is required.

**Memory operations:** extraction (Nano/Super) → staging → (on approval) commit; retrieval is a straightforward relevance lookup, not graph traversal.

**Context selection:** conversation history + explicit session/project labels, fed to the model as prompt context; no separate context-vector computation service at MVP (contrast with the Master Plan's continuously updated context vector, §7.1). **[SOURCE §7.1 — deferred]**

**Summarization / classification / extraction:** Nemotron Nano/Super, for memory-candidate extraction and any chat-side summarization.

**Generation:** Nemotron Nano/Super for user-facing chat text.

**Agent loops:** none at MVP (single-shot reasoning per turn, no multi-step agent loop).

**Verification:** the staged-approval step (Memory Inbox pattern) functions as the system's verification gate — nothing is committed without it. **[SOURCE FR-1.5]**

**Fallbacks:** on a Nemotron/Nebius call failure, degrade gracefully (return an apologetic, honest message; do not fabricate) — consistent with FR-8's trust-and-safety intent even without the full audit/undo stack. **[SOURCE §23.1]**

---

## 13. Memory Architecture

*Dedicated specification, since persistent memory is the product's central, demo-critical capability. Each item states MVP behavior and the full-vision behavior it's a slice of.*

**What should be remembered [SOURCE §8.1]:** facts, decisions, preferences, and project/learning context the user states or that the system judges worth retaining from conversation. MVP: episodic facts/decisions only. Full vision adds semantic (stable preferences), procedural (how the user works), project, and intent/goal memory layers.

**What should not be remembered [SOURCE FR-1.11, §15.5]:** health, finance, passwords, and other sensitive categories, excluded by default via a Sensitive Content Filter. **[P1 for MVP]**

**Memory creation [SOURCE §11.1 steps 1–6]:** conversation → extraction/judgment (Nemotron Nano/Super) → Memory Inbox staging → user approval → commit.

**Memory retrieval [SOURCE FR-2.5, scoped]:** MVP uses simple relevance-based lookup (not graph traversal + vector search, which is full-vision/P2).

**Memory updating [SOURCE §8.4]:** MVP: user can manually edit a stored record via the Timeline. Full vision: natural-language corrections cascading through graph edges (P2, deferred, since there's no graph yet).

**Memory correction [SOURCE FR-1.7]:** manual edit at MVP; NL correction is P2.

**Memory deletion [SOURCE FR-1.6, FR-1.9]:** per-record delete via the Timeline is **P0**; bulk purge is **P2**; cryptographic deletion is **P3** (requires local-first encryption architecture not in scope).

**Memory prioritization [TBD]:** the Master Plan's importance/confidence scoring (§8.1's per-memory metadata) is not fully implemented at MVP; a simple recency + explicit-relevance heuristic substitutes. **[TBD — exact retrieval-ranking approach is an open implementation decision]**

**Short-term context:** conversation-turn history within a session. **[DECISION]**

**Long-term memory:** the approved, committed episodic store. **[DECISION]**

**User preferences:** captured as episodic facts at MVP rather than a distinct semantic-preference layer (full vision distinguishes them, §8.1). **[DECISION, scoped]**

**Episodic memory [SOURCE §8.1]:** **P0** — the only memory type fully implemented at MVP.

**Semantic memory [SOURCE §8.1]:** **P2** — deferred; the Knowledge Graph that would house it is also deferred (§7.9).

**Memory permissions [SOURCE §8.4]:** a single owning user at MVP; no multi-user memory-sharing controls needed.

**Privacy [SOURCE §15.1–§15.2]:** data minimization is the practical MVP substitute for the full local-first/zero-knowledge architecture; see §16.

**Retention [SOURCE FR-1.8]:** no automatic decay/TTL at MVP (**P2**); records persist until the user deletes them.

**Conflict resolution [SOURCE FR-1.4]:** contradictory new information is flagged for the user to resolve, never silently overwritten — **P0**, since this is core to the "recognize relevance" half of the demo loop.

**Retrieval relevance [TBD]:** see Memory prioritization above.

**User control [SOURCE FR-1.5, FR-1.6]:** approve/reject staging + Timeline browse/edit/delete — **P0**, the two pillars of user control at MVP scale.

---

## 14. Skills & Tool System

*MVP ships a fixed, small skill set rather than the full compiler; this section specifies both.*

**What a skill is [SOURCE §9.1]:** a named, triggerable capability bundling instructions, (optionally) tool calls, memory access, and an output format. MVP skills are hand-authored, not user-authored.

**Skill structure [SOURCE FR-3.2]:** trigger → (optional tool call) → memory read/write → output. MVP skills are simple prompt templates with defined inputs/outputs, not the full compiled trigger→tool-calls→memory-writes→output object graph.

**Skill discovery [SOURCE FR-3.12]:** skills are invokable by name in chat. **[P1]**

**Skill execution [SOURCE §9.2]:** MVP lifecycle is reduced to Describe (pre-written) → Execute, skipping Generate/Review/Approve/Test/Improve, which apply to the full NL-compiler flow. **[DECISION]**

**Skill permissions [SOURCE FR-3.6]:** each MVP skill has an explicit, fixed, minimal permission scope; no independent per-skill permission configuration UI at MVP.

**Skill inputs/outputs:** defined per skill (e.g., a session-briefing skill takes recent memory records as input, outputs a short summary).

**Tool access [SOURCE §10.1]:** MVP's tool surface is limited to what the demo needs (memory read/write, and whatever minimal external calls the chosen skills require); the full named integration surface (email, calendar, GitHub, Slack, Notion, etc., §10.1) is **P3**.

**Tool authentication [TBD]:** exact secrets-handling approach for any external API keys used in the demo is an open implementation decision — see §26 Risks.

**Tool failure [SOURCE §23.1]:** halt, log, notify — **P0**, consistent with the graceful-degradation principle.

**Skill composition / chaining [SOURCE FR-3.5]:** **P3** — not needed for a fixed, small skill set.

**Adding/removing skills [SOURCE FR-3.11]:** code-level only at MVP; no-code skill builder is **P3**.

**User-created skills [SOURCE FR-3.1–FR-3.3]:** **P2/P3** — the full NL-to-skill compiler is explicitly deferred (§6.3).

---

## 15. Agent & Task Execution System

*MVP has no multi-step agent loop; this section documents the full-vision requirement and states the MVP's much simpler substitute.*

**Intent understanding [SOURCE §7.1, FR-6]:** MVP infers intent from the current conversation turn plus session context only.

**Planning [SOURCE §7.3]:** single-step; no multi-step goal tracking.

**Task decomposition [SOURCE §9.1]:** not implemented — MVP tasks (skills) are atomic.

**Tool selection [SOURCE §10]:** deterministic per skill, not dynamically chosen by the model from a large toolset.

**Execution [SOURCE §11.1 steps 8–10]:** direct call, no sandbox isolation.

**State tracking [SOURCE §9.3]:** basic execution log per skill run (what ran, when, outcome) — **P0**, doubling as the audit trail (§17).

**Intermediate results [TBD]:** not surfaced separately at MVP; only final output shown.

**Verification [SOURCE §22 gap-flag in Master Plan]:** no formal test harness; the staged-memory-approval step is the closest MVP equivalent for memory writes (§13).

**Error recovery [SOURCE §23.1]:** halt → log → notify → (manual) retry — **P0**.

**Human confirmation [SOURCE FR-8.1]:** any mutating action requires explicit user action — **P0/P1** depending on which actions the final skill set includes.

**Completion:** result shown in chat / Timeline.

**Long-running / background / scheduled / proactive tasks [SOURCE §17.1, §7.2]:** MVP's only "background" behavior is the context- and deadline-triggered proactive check (§7.14); there is no general scheduler or background daemon. **[DECISION]**

---

## 16. Privacy & Security Requirements

*Privacy is treated as a first-class requirement per the Master Plan's shared philosophy (§15.1), even though the MVP cannot implement the full local-first, zero-knowledge architecture. Each item below states the practical MVP floor and the deferred full-vision mechanism.*

**Data ownership [SOURCE §15.1]:** conceptually the user's; MVP does not yet implement export/portability (P1/P2) or a user-held encryption key (P3, requires local-first architecture).

**Data isolation [SOURCE §16.4]:** MVP is single-user, so identity-vs-context separation is not yet a live concern; documented as a **P2/TBD** design principle for when multi-user support is considered.

**Authentication/authorization [SOURCE §14]:** none at MVP (single pre-seeded demo persona, no login flow) — this mirrors a gap the Master Plan itself acknowledges exists across all four source plans (§14, §28.4). **[TBD if the product needs real end-user auth post-hackathon]**

**Permission scopes [SOURCE §10.2–§10.3]:** MVP: fixed, minimal, per-tool allow list. Full vision: multi-axis CBAC.

**Secrets [SOURCE §12.2]:** any API keys used are stored via standard hosting-platform secret management (not a dedicated in-product vault) — **[TBD pending final deployment target]**.

**Tool permissions / memory permissions:** see §12, §13.

**Sensitive information [SOURCE FR-1.11]:** Sensitive Content Filter — **P1**.

**Encryption [SOURCE §16.3]:** MVP: relies on the hosting platform's standard encryption-in-transit (HTTPS) and at-rest defaults; a dedicated AES-256 encryption layer with user-held keys is **P3**, deferred with the local-first architecture. **[TBD — exact storage encryption posture depends on hosting choice]**

**Audit logs [SOURCE §15.3]:** basic log of memory writes and skill runs — **P0**; immutability guarantees and a full Activity & Audit Stream UI are **P2**.

**User controls [SOURCE §15.1]:** approve/reject memory, delete records — **P0**; full export/deletion/migration tooling — **P1/P2**.

**Data export [SOURCE §15.2]:** **P1/P2**, not committed for the initial submission but strongly recommended given the "data portability, not platform captivity" principle.

**Data deletion [SOURCE FR-1.9]:** per-record delete — **P0**; cryptographic/irrecoverable deletion — **P3**.

**Model/data boundaries [SOURCE §15.2]:** whatever is sent to Nemotron via Nebius is, by necessity of this architecture, leaving the "local" boundary the Master Plan's full vision assumes; this is a **deliberate, disclosed departure** from the local-first principle, justified by the hackathon's hosted-inference requirement. **[DECISION, flagged]**

**Prompt-injection protection [SOURCE FR-8.4]:** any externally fetched content (if the final skill set includes any) is treated as untrusted data, never as instructions — **P0** if such a skill ships, otherwise not applicable.

**Tool abuse prevention / agent safety [SOURCE §10.5]:** MVP's minimal tool surface and low-autonomy defaults are the practical substitute for full sandboxing.

**Human approval mechanisms [SOURCE FR-8.1]:** see §12, §15.

---

## 17. Functional Requirements

*Restated and re-scoped from the Master Plan's FR-1 through FR-10 (§4) into MVP-testable requirements. Master Plan FR numbers are preserved as traceability references; this PRD's own FR-XXX numbering follows.*

**FR-001 — Persistent Memory** *(traces to Master Plan FR-1)*
The system shall retain user-approved information across sessions and retrieve it when relevant to a later interaction.
*Acceptance criteria:* A fact stated in one session is correctly recalled, without restatement, in a later session.

**FR-002 — Staged Memory Approval** *(traces to FR-1.5)*
The system shall stage extracted candidate memories for explicit user approval before committing them to long-term storage.
*Acceptance criteria:* No memory record exists in long-term storage that was not either explicitly approved or auto-committed under a rule the user has explicitly set.

**FR-003 — Memory Timeline** *(traces to FR-1.6)*
The system shall provide a scrollable view of all stored memory records, each editable and deletable.
*Acceptance criteria:* Every stored record is visible, correctable, and deletable from this view.

**FR-004 — Conflict Flagging** *(traces to FR-1.4)*
The system shall never silently overwrite a memory record with contradictory new information; it shall flag the conflict for user resolution.
*Acceptance criteria:* Given two contradictory statements across sessions, the system surfaces both and asks which is current.

**FR-005 — Sensitive Content Exclusion** *(traces to FR-1.11)*
The system shall exclude a defined set of sensitive categories (health, finance, passwords) from automatic memory extraction by default.
*Acceptance criteria:* A test statement in an excluded category is not proposed as a candidate memory.

**FR-006 — Context-Triggered Proactive Surfacing** *(traces to FR-5, §7.2)*
The system shall, on detecting a topic related to existing memory, proactively surface the connection as a suggestion (not an interruption).
*Acceptance criteria:* Given a new-session prompt on a topic with prior stored context, the system references the prior context unprompted, with a visible confidence/evidence framing rather than an unstated assumption.

**FR-007 — Deadline-Triggered Proactive Surfacing** *(traces to FR-5, §7.2)*
The system shall surface a suggestion when a stored, deadline-bearing item is approaching and unresolved.
*Acceptance criteria:* Given a stored item with an approaching deadline and no resolution recorded, a suggestion appears.

**FR-008 — Suggestion, Not Interruption** *(traces to FR-5.2)*
All MVP proactive output shall be delivered as an in-app suggestion, never a push notification or forced interruption.
*Acceptance criteria:* No proactive output blocks or forcibly interrupts the user's current action.

**FR-009 — Minimal Permission Gate** *(traces to FR-4.1)*
No tool call shall execute without passing an explicit, fixed permission check.
*Acceptance criteria:* A disallowed tool call is rejected and logged, not silently executed.

**FR-010 — Confirm-Before-Mutate** *(traces to FR-7.1, §10.2)*
Any action with a side effect outside the chat/memory store shall require explicit user confirmation before executing.
*Acceptance criteria:* No mutating action executes without a preceding user click/confirmation.

**FR-011 — Task-Routed Model Calls** *(DECISION, not a direct Master Plan FR, but implements §7.3's model-tiering principle)*
Relevance/intervention/reasoning calls shall route to Nemotron Ultra; chat/extraction calls shall route to Nemotron Nano/Super.
*Acceptance criteria:* Logs show each call type consistently routed to its designated model tier.

**FR-012 — Graceful Degradation on Model/Tool Failure** *(traces to §23.1)*
On a Nemotron/Nebius call failure, the system shall halt the affected operation, log it, and notify the user honestly rather than fabricating a response.
*Acceptance criteria:* A simulated API failure produces a visible, honest error state, not a hallucinated answer.

**FR-013 — Fixed Skill Invocation by Name** *(traces to FR-3.12)*
Pre-built skills shall be invokable by name in chat.
*Acceptance criteria:* Naming a skill triggers its execution.

**FR-014 — Basic Audit Log** *(traces to FR-8.1, §25)*
Every memory write and skill run shall be recorded with what happened and when.
*Acceptance criteria:* A log entry exists for every memory write and skill execution in a test session.

*(FR-015 and beyond, corresponding to deferred capabilities in §6.3/§7 — full Knowledge Graph queries, skill compilation, the 5-tier autonomy ladder, the full Automation Engine, multi-modal input, sandboxed execution, export/cryptographic deletion — are captured as backlog items in §28 rather than duplicated here as testable MVP requirements, since they are explicitly out of scope for this submission.)*

---

## 18. Non-Functional Requirements

| Category | Requirement | Status |
|---|---|---|
| Performance | Chat responses return within a few seconds under normal Nebius/Nemotron latency | **TBD** — no numeric target given by the Master Plan; propose ≤5s p50 for chat, ≤10s p50 for a proactive-check pass, pending real measurement |
| Latency | Task-routed calls (Ultra vs. Nano/Super) should not make the common case (chat) noticeably slower than a single-model system | **[DECISION]** design intent; not numerically bounded |
| Availability | Demo must be reliably reachable via the required working demo URL for judging | **P0 [DECISION]** |
| Scalability | Not a design target for this submission (single demo persona, solo evaluator load) | **Out of scope, TBD post-hackathon** |
| Security | See §16 | — |
| Privacy | See §16 | — |
| Reliability | Core loop (remember → persist → recognize relevance → act) must work live, not just in a recorded video | **P0 [DECISION]** — explicit project priority |
| Maintainability | Fresh, separate repo; no code dependency back to prior personal projects | **[DECISION]** |
| Extensibility | Architecture should not preclude the Phase 2/3 growth path in §6.4/§29 | **[DECISION, design intent]** |
| Observability | See §7.17, §17 (basic audit log) | **P0 (minimal)** |
| Cost efficiency | Stay within Nebius credit allocation for the hackathon; task-routing to smaller models (Nano/Super) for high-frequency calls is itself a cost-control measure | **[DECISION]** |
| Resource usage | Not separately targeted; follows from hosted-inference architecture | **TBD** |
| Model efficiency | Task-based routing (§12) is the primary efficiency mechanism | **[DECISION]** |
| Deployment | Streamlit app; deployment target TBD, Hugging Face Spaces recommended, following from the frontend choice | **[DECISION + TBD]** |
| Recovery | On failure, degrade gracefully rather than crash (§7.17, FR-012) | **P0** |
| Compatibility | Web-based, no platform-specific requirement | **[DECISION]** |

*(Where the Master Plan gives no numeric target, no number is invented — targets above marked TBD/proposed are flagged as such, per instruction not to fabricate figures.)* **[SOURCE §18's own instruction: "do not invent arbitrary numbers"]**

---

## 19. Data Model

*MVP entities only; full-vision entities (Skill, Tool, Agent, Workflow, Permission, Credential, Knowledge item, Event, Notification, Execution, full Audit record) are listed for completeness but marked deferred where not needed at MVP scale.* **[SOURCE §19]**

| Entity | MVP fields (minimum) | Status |
|---|---|---|
| **User** | single demo persona identifier | **P0 (minimal)** |
| **Memory record** | id, content, source-turn reference, timestamp, approval status | **P0** |
| **Conversation / Message** | session id, turn content, timestamp | **P0** |
| **Skill** | name, fixed prompt/logic, trigger condition | **P0 (fixed set)** |
| **Execution log entry** | what ran (memory write or skill run), timestamp, outcome | **P0** |
| **Proactive suggestion** | triggering memory reference, trigger type (context/deadline), surfaced timestamp, user response | **P0** |
| Tool | *(deferred — no general tool entity, MVP tools are hardcoded)* | **P2/P3** |
| Agent | *(deferred — no agent entity)* | **P3** |
| Task / Workflow | *(deferred — no automation entity)* | **P2/P3** |
| Permission | *(deferred — fixed allow list, not a data-modeled entity)* | **P2** |
| Credential | *(deferred — platform secret management, not modeled)* | **P2/TBD** |
| Knowledge item (graph node/edge) | *(deferred — no graph)* | **P2** |
| Event | *(partially covered by Execution log entry above)* | **P1** |
| Notification | *(covered by Proactive suggestion above)* | **P0** |
| Audit record | *(covered by Execution log entry above, minimal form)* | **P0 (minimal) / P2 (full)** |

*Per the instruction to only include entities relevant to the actual architecture, the deferred rows above are listed for traceability to the Master Plan's full entity set (§19) rather than specified in detail — they have no MVP schema.*

---

## 20. API & Integration Requirements

**Internal services [DECISION]:** a single application service (Streamlit app) calling out to Nebius Token Factory/AI Cloud for Nemotron inference and to the storage backend for memory read/write. No separate internal microservice boundaries at MVP scale.

**Model APIs [DECISION, required]:** Nebius Token Factory/AI Cloud API, calling Nemotron Ultra and Nemotron Nano/Super per the routing in §12.

**Tool APIs [TBD]:** exact external APIs (if any) used by the fixed skill set are not yet finalized — an open implementation decision.

**External integrations [SOURCE §10.1, deferred]:** none of the Master Plan's named integration surface (Gmail, Calendar, Notion, Slack, GitHub, etc.) is required for MVP; any single integration used by a demo skill is a **P1/P2** addition, not a committed requirement.

**Authentication:** platform-level (Nebius API keys), not user-facing auth (§16).

**Webhooks / events / background jobs [SOURCE §17.1, deferred]:** none at MVP — no event bus, no scheduler.

**Data exchange:** simple request/response between the Streamlit app and the Nebius inference endpoint and storage backend; no external Personal API surface (§18.1) — **P3**.

**Error handling:** see FR-012 (§17) and §23.1.

---

## 21. Deployment & Infrastructure

**Nebius Token Factory / Nebius AI Cloud [DECISION, required]:** hosts all Nemotron inference calls; this is the mandatory hackathon deployment requirement.

**NVIDIA open-source models [DECISION, required]:** Nemotron (Ultra + Nano/Super split), the mandatory open model.

**Nemotron applicability:** see §12 for the exact task-to-model-tier mapping.

**Serverless infrastructure:** not specifically targeted; Nebius Token Factory functions as the inference-serving layer regardless of whether it is "serverless" in the strict sense — **[TBD, depends on Nebius's own service model]**.

**Deployment architecture:** Streamlit frontend, deployed to a public URL. **Deployment target: TBD, Hugging Face Spaces recommended**, following directly from the Streamlit choice already locked in. **[DECISION + TBD on final host]**

**Environment configuration:** Nebius API credentials and any storage-backend credentials via the deployment platform's standard secret/environment-variable mechanism. **[TBD — exact mechanism depends on final host]**

**Secrets:** see §16 — no dedicated in-product vault; relies on platform-level secret management.

**Scaling:** not a design target (§18).

**Background processing:** none beyond the narrow context-/deadline-triggered proactive check, which can run as part of normal request handling rather than a separate background worker at this scale. **[DECISION]**

**Monitoring/logging:** basic audit log (§17, §25); no external operational monitoring (crash reporting, uptime dashboards) — this mirrors a gap the Master Plan itself flags as unspecified across all four source plans (§25, §28.4). **[TBD if pursued post-hackathon]**

**Reproducibility requirement (hackathon-mandated, not from the Master Plan):** a public code repository with setup instructions must let a judge run the working demo independently — **P0**.

---

## 22. Hackathon MVP

*This is the authoritative, already-locked scope for the Oct 30, 2026 submission — not a re-derivation of the Master Plan's own generic reconciled MVP (§20.5), though it is a genuine subset of it. Where this section and the Master Plan's own MVP list differ in emphasis, this section is what actually gets built.* **[DECISION]**

**Must work, live, for the demo:**

1. **The core loop:** remember → persist → recognize relevance → act (surface/notify), proven live rather than only shown in a recorded video. **[DECISION — explicit stated priority: functionality over polish]**
2. **Staged memory approval** (simplified Memory Inbox) — nothing commits to long-term storage without going through an approval step.
3. **Memory Timeline/Inspector** — confirmed in scope, not a stretch goal.
4. **Context-triggered proactivity** — the assistant reconnects a new topic to stored context unprompted.
5. **Deadline-triggered proactivity** — the assistant surfaces an approaching, unresolved, deadline-bearing item.
6. **Nemotron on Nebius Token Factory/AI Cloud**, task-routed (Ultra for reasoning/relevance/intervention; Nano/Super for chat/extraction) — the mandatory technology requirement, implemented meaningfully rather than as a token integration.
7. **Streamlit frontend.**
8. **A working, publicly reachable demo URL** (hackathon submission requirement).
9. **A generic demo persona** ("Riya" for now), not the builder's own real data.

**Explicitly NOT required for this submission** (see §6.3 for the full list): Knowledge Graph, NL skill compiler, scheduled/opportunity/autonomous-completion proactive triggers, local/on-device inference, sandboxed execution, multi-modal input, multi-user auth, Memory Graph *visualization*, full 5-tier autonomy ladder (only Observe/Suggest tiers), full Automation Engine.

**Why this is not "a generic chatbot":** the staged-approval memory loop plus context-triggered proactive surfacing is exactly the differentiator the Master Plan identifies as the category's core distinction — *state* + *initiative*, not just better answers (§1, §2.1, §27.6). A plain Q&A bot with no memory persistence or proactive behavior would fail this bar even with a polished UI.

---

## 23. Demo Scenario

**Story arc:** Problem → User → Personal AI → Memory → Reasoning → Action → Result. **[SOURCE §23 template]**

1. **Problem:** Riya (demo persona) is a student juggling a course, a personal AI/ML side project, and general learning threads. In session 1, she mentions a specific decision or preference relevant to her project (e.g., a technical choice she's made, or something she's currently stuck on).
2. **Memory:** The assistant proposes this as a candidate memory; Riya approves it (Memory Inbox staging shown on screen).
3. **Time passes (a new, separate session begins).**
4. **Reasoning:** Riya opens a new session and raises a related topic — not explicitly restating the earlier context.
5. **Action:** The Context Engine (Nemotron Ultra) recognizes the connection with sufficient confidence and proactively reconnects it — e.g., "This connects to [earlier decision] you mentioned — want me to factor that in?" — framed as evidence, not an unstated assumption (FR-6.2).
6. **Result:** Riya confirms; the conversation proceeds with the reconnected context applied, without her having restated it.
7. **Secondary beat (deadline trigger):** Riya has an approaching, unresolved deadline-bearing item stored from an earlier session; the assistant surfaces it unprompted as a suggestion (not a push interruption), demonstrating the second proactive trigger type in scope.
8. **Closing beat:** A quick look at the Memory Timeline shows the full, correctable record of what's been remembered — reinforcing the "user controls memory" principle live, not just asserted.

**What NOT to show (per honesty of scope):** no Knowledge Graph visualization, no skill-authoring flow, no Execute-with-Approval/Autonomous-tier action, no multi-modal input — none of these are built, so the demo does not imply they are.

---

## 24. Hackathon Submission Readiness

*Checklist derived from the hackathon's own stated requirements (per this document's opening context, not the Master Plan) plus the locked project decisions.*

- [ ] **Working application** — reachable, functioning demo (P0, §22)
- [ ] **Nebius deployment** — Token Factory/AI Cloud actually used for inference, not just referenced (P0)
- [ ] **NVIDIA open-source model usage** — Nemotron, task-routed, actually called (P0)
- [ ] **Personal AI Track alignment** — persistent memory + proactive surfacing + (minimal) tool use, demonstrably present (P0)
- [ ] **Working demo URL** — public, reachable at submission time (P0)
- [ ] **Public repository** — fresh, separate repo (per the locked build-strategy decision), no dependency back to prior personal projects **[DECISION]**
- [ ] **Open-source license** — **TBD**, not yet decided
- [ ] **README** — setup instructions sufficient for a judge to run it independently
- [ ] **Model/Nebius documentation** — clear explanation of how Nemotron + Nebius are used, matching §12
- [ ] **Demo video** — ≤3 minutes, following the arc in §23 **[DECISION — deadline and format confirmed]**
- [ ] **Demonstration of functionality** — live, not just video, per the "functionality over polish" priority
- [ ] **Privacy/security explanation** — matching §16's honest, scoped account (not overclaiming the local-first architecture that isn't built)
- [ ] **Existing-project update explanation, if applicable** — not applicable; this is a fresh, separate repo, not an update to SecondSelf or JARVIS
- [ ] **Feedback submission** — per hackathon process, **TBD**
- [ ] **Card-verification / credit-activation status** — flagged as an open operational risk, not a product risk; see §27

**Submission deadline:** Oct 30, 2026, 10:00 AM PT. **[DECISION]**

---

## 25. Testing Strategy

*The Master Plan specifies no formal QA methodology (§22 gap-flag); this section is net-new, informed by the functional requirements in §17 and scoped to what's feasible for a solo, time-boxed build.*

- **Unit testing [P1]:** targeted at the memory-staging and conflict-flagging logic (FR-002, FR-004), since these are the most behaviorally load-bearing pieces.
- **Integration testing [P0]:** end-to-end run of the core loop (FR-001, FR-006, FR-007) against the real Nebius/Nemotron endpoint, not mocked, before the demo — this is the single highest-value test given the "must work live" priority.
- **AI/model testing [P1]:** spot-check that Ultra vs. Nano/Super routing (FR-011) is actually happening as designed, not silently falling back to one model.
- **Agent testing:** not applicable — no agent loop at MVP.
- **Tool testing [P1]:** whatever tool(s) the final fixed skill set uses, tested for the failure path (FR-012) specifically, since graceful degradation is a stated priority.
- **Memory testing [P0]:** verify a fact stated in session 1 is retrievable and correctly applied in session 2 (the acceptance criterion for FR-001).
- **Security testing [P2]:** basic check that the Sensitive Content Filter (FR-005) rejects an obviously sensitive test statement.
- **Permission testing [P1]:** verify a disallowed tool call is actually rejected (FR-009).
- **Failure testing [P0]:** simulate a Nebius/Nemotron API failure and confirm graceful degradation (FR-012), since this directly protects the live demo.
- **End-to-end testing [P0]:** full run-through of the demo scenario (§23) before submission, more than once, on the actual deployed URL.
- **Demo validation [P0]:** the demo video and the live URL must show the same behavior — no divergence between what's recorded and what a judge can independently reproduce.
- **Hackathon environment testing [P0]:** confirm the deployed app is reachable from outside the builder's own network/session before the deadline.

---

## 26. Risks & Mitigations

| Risk | Source | Mitigation |
|---|---|---|
| Nebius credit activation not confirmed (card-verification blocker) | **[DECISION-context]** builder has submitted both credit forms but has not confirmed a visible credit balance; blocked on a $0 card-verification step | Pursue a virtual card (Jupiter/Fi Money/Niyo) as the no-third-party-card route; check the Token Factory dashboard directly rather than relying on confirmation emails |
| Model hallucination in the relevance/reconnection step | **[SOURCE §26 gap-flag pattern]** | Evidence-not-truth framing (FR-6.2) — always state the connection as a suggestion the user can correct, never an assumed fact |
| Tool/API failure during the live demo | §23.1 | Graceful degradation (FR-012); rehearse the failure path, not just the happy path |
| Memory corruption / bad extraction | §8.4 | Staged approval (FR-002) as the safety gate; nothing bad commits without a human in the loop |
| Prompt injection via any fetched external content | FR-8.4 | Treat fetched content as untrusted data; keep the MVP tool surface minimal specifically to reduce this attack surface |
| Latency (Ultra calls on the reasoning path feel slow in a live demo) | §18 (no numeric target given) | Reserve Ultra calls for the specific relevance/intervention moments in the demo script; use Nano/Super for everything else |
| Cost overrun against Nebius credits | §18 | Task-based routing (cheaper models for high-frequency calls) is itself a cost control |
| Scope creep given ~5–10 hrs/week and competing commitments (coursework, SIH 2026, Build-A-Bot, RSNA Kaggle, YouTube, SAI Store) | **[DECISION-context]** | Hold the line on §22's locked MVP list; treat everything in §6.3/§6.4 as explicitly out of scope until after submission |
| Deployment target not finalized (Hugging Face Spaces only "recommended," not committed) | **[DECISION-context, TBD]** | Decide and lock the host early enough to leave buffer time for the reproducibility/demo-URL requirement |
| Integration complexity if any external tool is added to the fixed skill set | §10 | Keep the fixed skill set's tool dependencies to the minimum needed for the demo script in §23 |
| Solo builder — no second reviewer to catch demo-breaking bugs | **[DECISION-context]** | Rehearse the full demo scenario (§23) multiple times, on the deployed URL, before the deadline |

---

## 27. Development Roadmap

*Phased for this specific solo, time-boxed build — not the Master Plan's multi-year Phase 1/2/3 roadmap (§20), which remains the long-term map in §29's Definition of Done and §6.4's Future Scope.*

1. **Foundation** — storage backend for memory records, Streamlit app skeleton, Nebius/Nemotron connectivity smoke test (both Ultra and Nano/Super).
2. **Core AI** — chat loop wired to Nemotron Nano/Super; basic prompt-based memory extraction.
3. **Memory** — staged approval flow (Memory Inbox), commit-to-store, Memory Timeline UI.
4. **Skills/tools** — the fixed, small skill set implemented and invokable by name.
5. **Agent execution** — *not applicable at this scope* (no agent loop).
6. **Security/privacy** — Sensitive Content Filter, confirm-before-mutate gate, basic audit log.
7. **UI/UX** — Home/briefing view (if time allows), chat, Timeline, in-app suggestion surfacing.
8. **Nebius/NVIDIA integration** — finalize task-based routing (FR-011), verify it live.
9. **Testing** — per §25, prioritizing the core-loop integration test and the failure-path test.
10. **Demo preparation** — rehearse the scenario in §23, record the ≤3-minute video.
11. **Submission readiness** — work through §24's checklist.

---

## 28. Engineering Backlog

| Task ID | Task name | Description | Priority | Dependencies | Expected output | Acceptance criteria |
|---|---|---|---|---|---|---|
| BL-01 | Storage backend | Set up structured store for memory records | P0 | None | Working read/write store | A record written can be read back |
| BL-02 | Nebius/Nemotron connectivity | Wire up calls to both Ultra and Nano/Super via Nebius Token Factory | P0 | BL-01 (parallel) | Successful test calls to both tiers | Both tiers return valid responses |
| BL-03 | Chat loop | Basic conversational turn handling via Nano/Super | P0 | BL-02 | Working chat | User can converse; responses generated by Nemotron |
| BL-04 | Memory extraction | Propose candidate memories from conversation via Nano/Super | P0 | BL-03 | Candidate memory objects | A stated fact produces a candidate |
| BL-05 | Memory Inbox (staging) | Approve/ignore UI for candidate memories | P0 | BL-04, BL-01 | Staging UI + commit-on-approve logic | Only approved candidates reach the store |
| BL-06 | Memory Timeline | Browsable, editable, deletable list of stored records | P0 | BL-01 | Timeline UI | Every stored record visible/correctable/deletable |
| BL-07 | Context reconnection (relevance check) | Detect topic relevance to stored memory via Ultra | P0 | BL-01, BL-02 | Working relevance-check call | Correctly reconnects a related topic across sessions |
| BL-08 | Conflict flagging | Detect and surface contradictory memory | P1 | BL-04, BL-01 | Conflict UI prompt | Contradiction is flagged, not silently overwritten |
| BL-09 | Sensitive Content Filter | Exclude sensitive categories from extraction | P1 | BL-04 | Filter logic | Sensitive test statement is excluded |
| BL-10 | Deadline-triggered proactivity | Surface approaching, unresolved deadline items | P0 | BL-01, BL-07's relevance-scoring pattern | Suggestion surfacing | Approaching stored deadline triggers a suggestion |
| BL-11 | Fixed skill set | Implement the small, pre-built skill templates | P0 | BL-03, BL-01 | Invokable-by-name skills | Naming a skill runs it |
| BL-12 | Confirm-before-mutate gate | Explicit confirmation before any side-effecting action | P1 | BL-11 | Confirmation UI | No mutating action fires without a click |
| BL-13 | Basic audit log | Record every memory write and skill run | P0 | BL-05, BL-11 | Log store + minimal view | Every write/run has a corresponding entry |
| BL-14 | Failure handling | Graceful degradation on Nebius/Nemotron failure | P0 | BL-02 | Honest error state | Simulated failure produces no hallucinated output |
| BL-15 | Home/briefing view | Optional lightweight command-center-style landing view | P2 | BL-06, BL-10 | Home view | Shows recent memory + pending suggestions |
| BL-16 | Deployment | Deploy Streamlit app to public URL | P0 | All above | Reachable demo URL | Judge can independently open and use it |
| BL-17 | Demo rehearsal & video | Run the full §23 scenario, record ≤3 min video | P0 | BL-16 | Demo video + verified live run | Video and live app show matching behavior |

---

## 29. Definition of Done

*For this specific submission — not the Master Plan's full-vision "done."*

- **Product functionality:** the core loop (remember → persist → recognize relevance → act) works live on the deployed URL, demonstrated end-to-end without scripting around a failure.
- **AI behavior:** Nemotron Ultra and Nano/Super are both genuinely in use, task-routed as specified in §12, not a single model doing everything with the other referenced only nominally.
- **Memory:** staged approval and the Memory Timeline both function as specified in §13/§17.
- **Skills/tools:** the fixed skill set runs correctly and is invokable by name.
- **Security:** the minimal permission gate, confirm-before-mutate, and Sensitive Content Filter are all functioning (§16).
- **Deployment:** the app is reachable at a public URL, independent of the builder's own machine/session.
- **Testing:** the core-loop integration test and the failure-path test (§25) have both been run successfully against the deployed instance, not just locally.
- **Documentation:** README with setup instructions sufficient for independent reproduction; a clear, honest explanation of how Nebius/Nemotron are used (§12, §24) that does not overclaim capabilities not built (§16's local-first honesty principle carried through).
- **Demo:** a ≤3-minute video following §23's arc, matching what the live app actually does.
- **Hackathon submission readiness:** every applicable item in §24's checklist is either done or explicitly, knowingly left TBD with a stated reason.

---

## 30. Open Questions & Decisions

*Consolidated from the ambiguities and gaps flagged throughout this PRD, plus the Master Plan's own flagged conflicts (§28.3–§28.5) where they still matter at MVP scale.*

1. **Deployment host:** Hugging Face Spaces is recommended but not finalized. **[TBD]**
2. **Exact tool(s) in the fixed MVP skill set:** not yet finalized — affects BL-11, BL-12, and whether §16's "external content as untrusted data" requirement (FR-8.4) is actually triggered. **[TBD]**
3. **Nebius credit/billing status:** card-verification blocker not yet resolved; a virtual-card route is the current leading option but unconfirmed. **[OPEN — see §26]**
4. **Exact memory-ranking/relevance heuristic** for retrieval (§13's "Memory prioritization" line) — no formal scoring model decided yet. **[TBD]**
5. **Product name:** the Master Plan preserves eight-plus candidate names without resolving to one (§27.1); the hackathon submission may ship without committing to a final brand name, using the generic persona framing instead. **[OPEN — a product decision, not urgent for submission]**
6. **License:** not yet decided for the public repository. **[TBD]**
7. **Export/data-portability feature:** flagged as a strong P1/P2 given the Master Plan's stated principle (§15.2, §18) but not committed for this submission — worth a go/no-go call if time allows. **[OPEN]**
8. **Encryption-at-rest posture:** depends on the final deployment/storage choice; not yet specified. **[TBD]**
9. **Whether any P1 items (conflict flagging BL-08, Sensitive Content Filter BL-09, confirm-before-mutate BL-12) make the cut** given the ~5–10 hrs/week budget and competing commitments — these strengthen the submission but are not part of the hard P0 core loop. **[OPEN, a scope call for the builder as time firms up]**
10. **Full-vision architecture conflict inherited from the Master Plan (§5.5, §28.3.1):** Rust-daemon/Wasm-sandbox vs. generic-service/container-sandbox — not resolved and explicitly not this submission's problem to resolve, but relevant if the product continues past the hackathon (§6.4). **[DEFERRED, not urgent]**
11. **Multi-user/authentication design**, if the product is ever extended beyond a single-user demo — the Master Plan itself has no answer here (§14); would need to be designed net-new. **[DEFERRED]**

---

## Master Plan Coverage Summary

- **Total major feature groups identified in the Master Plan's merged capability set (§3.5):** 20 (Sections 3–18 of this PRD collectively map every one of them to either an MVP requirement, a deferred/future-scope item, or an explicit out-of-scope decision — none were silently dropped).
- **Total functional requirements created:** 14 MVP-scoped FRs (§17, FR-001–FR-014), each traceable to a Master Plan FR or section; the Master Plan's remaining FR-1 through FR-10 sub-items not restated as their own PRD-level FR are captured instead as backlog/future-scope items (§6.3, §6.4, §28) rather than omitted.
- **Features mapped to the Hackathon MVP (§22):** persistent episodic memory with staged approval, Memory Timeline, context-triggered proactivity, deadline-triggered proactivity, task-routed Nemotron on Nebius, a fixed pre-built skill set, a minimal permission gate, basic audit logging, Streamlit UI, a working public demo URL.
- **Features deferred to post-hackathon (Phase 2/3 per the Master Plan's own §20.5 grouping):** full Personal Knowledge Graph, NL Skill Compiler/versioning/chaining/marketplace, full 5-tier autonomy ladder, full Automation Engine, multi-modal interaction, local/on-device inference, sandboxed execution, Digital Twin/simulation, temporary agents, federated inter-agent negotiation, cross-device sync, multi-user authentication.
- **Ambiguous items requiring a decision (this submission's own open items, §30):** 11, listed above — deployment host, exact skill-set tooling, Nebius billing status, retrieval-ranking heuristic, product naming, license, export feature go/no-go, encryption posture, which P1 stretch items make the cut, the inherited architecture-stack conflict, and multi-user auth design.
- **Master Plan items that could not be cleanly mapped to this submission at all** (i.e., neither MVP nor a near-term backlog item, only long-term future scope per §6.4/§26): OS-kernel-level integration, secure inter-agent negotiation protocols, federated learning, smart-home/wearable/IoT integration, on-device hardware-acceleration optimization — all explicitly Phase 3/Long-Term in the Master Plan itself (§20.5) and treated identically here.

No feature, requirement, or mechanism named in `Personal-AI-Unified-Master-Plan.md` was silently dropped in producing this PRD: everything not built for the hackathon submission is explicitly named as deferred, out of scope, or future scope, with its own Master Plan section reference, rather than omitted.
