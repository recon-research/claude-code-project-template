# AGENT_GUIDE.md — The Build Loop For &lt;PROJECT_NAME&gt;

For an LLM agent (Claude Code) pointed at this library and asked to *build*, not just answer questions. [CLAUDE.md](CLAUDE.md) gives the rules for *consulting* the library; this file gives the *loop* for turning it into shipped work.

---

## 0. Load order — what to read, and when

Do **not** read whole books; your context is finite. Load artifacts in this order and stop as soon as the current task is covered:

> **Finding the library.** The downstream project's own `CLAUDE.md` carries a one-line pointer to this library (here it's vendored at `textbooks/`). If you can't locate `MANIFEST.json`, ask — don't guess.

1. **[MANIFEST.json](MANIFEST.json)** — the machine index. `topic_to_books` / `rag_hints` route a topic to the right book(s); `coverage_gaps` says what's *not* covered. Load once; keep it resident.
2. **[SECTIONS.json](SECTIONS.json)** — every heading (`id`, `title`, `line`). Resolve and **verify** any `Book NN §X` without opening the book. It's large — **grep it; don't load it whole.**
3. **[reference/STARTER_KIT.md](reference/STARTER_KIT.md)** — milestone order and exit criteria: what to build next, and when a milestone is done.
4. **[reference/DECISION_TREES.md](reference/DECISION_TREES.md)** — for any architectural fork. Many choices are settled here with trade-offs; don't re-litigate from scratch.
5. **The specific book section(s)** — only what SECTIONS.json says is relevant. Read narrowly.
6. **[../.claude/skills/](../.claude/skills/)** — the atomic operations (§3). **[reference/WORKFLOWS.md](reference/WORKFLOWS.md)** — multi-book recipes.
7. **[reference/ANTI_PATTERNS.md](reference/ANTI_PATTERNS.md)** + **[reference/SYMPTOMS.md](reference/SYMPTOMS.md)** — the relevant entries *before* coding, and again when something breaks.

---

## 1. The build loop (per feature or subsystem)

Run this for each unit of work. Steps b–d are cheap; don't skip them to "save time" — they prevent the expensive rework.

```
a. CLASSIFY   → What kind of task is this? (CLAUDE.md task→doc table)
b. ROUTE      → MANIFEST topic_to_books / rag_hints → book(s); SECTIONS.json → exact §sections
c. PRE-MORTEM → Read the matching ANTI_PATTERNS + SYMPTOMS entries for this area FIRST
d. DECIDE     → Any architectural fork? Resolve via DECISION_TREES; if it's the human's call, surface it (CLAUDE.md §3)
e. IMPLEMENT  → Follow the book's architecture; adapt APIs to the project's actual stack (§4)
f. ATOMIZE    → Use the matching skill for the mechanical part (the add_*/ project skills)
g. VERIFY     → build_and_test; add_test; definition_of_done for the full gate
h. PROFILE    → Optimize only against data (profile_subsystem). Never on a hunch (§5)
i. RECORD     → Note any new decision, gap, or deviation in the project's docs / decision log
```

The loop isn't strictly linear — `g` failing sends you back to `c`/`e`. But never let code reach `g` without having done `c`.

### 1.5 A worked example *(replace this with a real trace once the first book exists)*

A concrete end-to-end trace anchors the loop far better than abstract description. After onboarding, replace the schematic below with a real one — a small feature, each step naming a **verifiable** `Book NN §X`:

- **a. Classify** → what kind of work is `<feature>` (a fork? a mechanical add? a perf task?).
- **b. Route** → MANIFEST `topic_to_books`: `<topic>` → `Book NN`; `grep SECTIONS.json` for `§<x>`; read only those.
- **c. Pre-mortem** → the `ANTI_PATTERNS`/`SYMPTOMS` entries for `<area>` (note the guards before coding).
- **d. Decide** → resolve the fork via `DECISION_TREES Dn`, or surface it to the human with a recommended default.
- **e–f. Implement + atomize** → follow `Book NN §X`'s architecture; use `<add_*>` for the mechanical part.
- **g. Verify** → `add_test` for `<the invariants>`; then `definition_of_done` runs the gate.
- **h. Profile** → only if it shows up hot; no perf claim without a capture.
- **i. Record** → log the new decision/component in the project's docs.

---

## 2. Definition of done (the verification gate)

A unit of work is **not done** until these hold — self-audit before telling the human a subsystem is complete (orchestrated by the [`definition_of_done`](../.claude/skills/definition_of_done.md) skill):

- [ ] Builds clean and `build_and_test` passes (no new warnings the project treats as errors).
- [ ] Has tests appropriate to its kind (`add_test`: unit / integration / property / golden).
- [ ] If it owns persistent/simulation state → `snapshot_restore_test` round-trips (for anything that must reset, replay, or roll back).
- [ ] If it touches the run loop → `validate_headless_mode` still passes (no new hard dependency on a window / device / human).
- [ ] Known failure modes from `ANTI_PATTERNS` for this area are explicitly avoided or guarded.
- [ ] Any performance claim is backed by a profile, not a guess.
- [ ] Determinism preserved where the library requires it.
- [ ] The milestone's `STARTER_KIT` / `ROADMAP` exit criterion is met (if this closes a milestone).

---

## 3. The skills map (atomic operation → skill)

These live in the project's `.claude/skills/` and read project paths/commands from `PROJECT_CONVENTIONS.md`, so the same skills work unmodified on any project.

| You are… | Skill |
|---|---|
| **Onboarding / resuming** a session | `onboard` |
| **Checkpointing** before context runs out | `prepare_compaction` |
| **Building / extending** this library | `build_library` |
| **Setting up** the skills in a project | `configure_project` |
| **Planning / designing** a feature | `plan_work` |
| **Reviewing / auditing** a design or diff vs the library | `review_against_library` |
| **Adversarial multi-lens review** (before merge) | `adversarial_review` |
| **Verifying "is it done"** | `definition_of_done` |
| Building + testing | `build_and_test` |
| Adding a test | `add_test` |
| Profiling | `profile_subsystem` |
| Optimizing a hot path | `optimize_loop` |
| Generating content with an LLM | `generate_content` |
| Adding telemetry | `add_telemetry_event` |
| Exposing an action to an agent (MCP tool) | `add_agent_tool` |
| State round-trip test | `snapshot_restore_test` |
| Headless / CI operability gate | `validate_headless_mode` |
| Keeping deferred work in the tracker | `track_followups` |
| *(domain-specific `add_*` / `debug_*` skills)* | *derived during onboarding* |

---

## 4. Respect the project's actual stack

The library is opinionated and assumes `<EXAMPLE_SYSTEM>`'s defaults. When the project differs: the **architectural patterns transfer; the specific APIs do not** — port the idea, not the signature. Call out the mismatch once, then proceed in the project's idiom. Code in the books is **illustrative, not necessarily compileable** — never paste it verbatim and claim it builds.

## 5. When to stop and ask the human (honest leverage)

Your multiplier is **not** uniform. Drive boilerplate / refactor / tests / docs (high leverage) and standard work-from-spec (verify hard). For **architectural design**, **performance tuning without profile data**, **subtle concurrency**, and **integration debugging** you are ~1× and sometimes harmful — propose options from `DECISION_TREES`, get a profile first, slow down, surface findings. Set a realistic blended expectation. Before fabricating an answer you can't locate, check `coverage_gaps` and say so.

## 6. Keep the library honest (maintenance)

If you edit the library (add a book, renumber, change headings), run from the library root:
- `python tools/_gen_sections.py` — regenerate `SECTIONS.json`.
- `python tools/_audit_refs.py` — confirm every `Book NN §X` resolves (target: **0 misses**).
- `python tools/_audit_routing.py` — confirm representative queries still route right; add a `ROUTING_EVAL.json` case for any new topic.
- `python tools/_audit_links.py` — confirm every relative markdown link resolves (target: **0 broken**).
- Update counts in `README.md` / `CLAUDE.md` / `MANIFEST.json`; update `topic_to_books` / `rag_hints`; add a `CHANGELOG.md` entry. **Counts drift — verify, don't trust.**

---

*Consult to learn. Route to find. Verify before you assert. Build the thing.*
