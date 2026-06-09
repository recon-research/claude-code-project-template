---
name: onboard
description: Start or resume a working session. Use when the user says "welcome back", "let's onboard", "onboard and continue", "let's continue", or opens a fresh session. Branches between first-time onboarding (read the _intake/ brief and set up the project docs + textbook outline) and resuming an in-flight project (read Status + ROADMAP + open issues and pick up the resume point).
---

# Onboard / Resume

The session entry point. First decide which mode you're in, then run it.

## Procedure

**Mode A — First-time onboarding** (the `CLAUDE.md` Status block still has `<placeholders>`, or `_intake/` has new planning docs):
1. Read everything in [`_intake/`](../../_intake/) — the brief, architecture notes, roadmap sketch, domain notes.
2. Fill [`CLAUDE.md`](../../CLAUDE.md): the project name, one-liner, and the **Status** block. Remove the "new project" blockquote.
3. Draft [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) (shape, invariants, the initial `D-NN` decision log) and [`docs/ROADMAP.md`](../../docs/ROADMAP.md) (milestones `M0..`) from the brief. Surface any unresolved fork as a `D-NN` decision with a recommended (ambitious) default + its grounding.
4. Propose the **textbook/RAG library outline** (volumes → books) per [`textbooks/LIBRARY_SEED.md`](../../textbooks/LIBRARY_SEED.md) §1 and get explicit approval. Then hand off to [`build_library`](build_library.md).
5. Run [`configure_project`](configure_project.md) to fill [`PROJECT_CONVENTIONS.md`](../../PROJECT_CONVENTIONS.md) once code/tooling exists.

**Mode B — Resume an in-flight project** (the default day-to-day):
1. Read the **Status** block at the top of [`CLAUDE.md`](../../CLAUDE.md) — done / in-progress / next / open decisions / **resume point**.
2. Read [`docs/ROADMAP.md`](../../docs/ROADMAP.md): the current milestone and its next slices.
3. Check the live backlog: `gh issue list` (open issues are the source of truth, not chat history).
4. Re-read [`PROJECT_CONVENTIONS.md`](../../PROJECT_CONVENTIONS.md) for build/test/run commands.
5. Pick up the **resume point**. Run the [`textbooks/AGENT_GUIDE.md`](../../textbooks/AGENT_GUIDE.md) build loop on the next slice: classify → route → pre-mortem → decide → implement → atomize → verify → record.
6. If a real fork appears, surface it as a decision (recommended ambitious default + `Book NN §X` / `DECISION_TREES Dn`) rather than guessing. Otherwise keep going on autopilot.

## Verification

- You can state, in one or two sentences: the current milestone, the resume point, and the exact next action.
- Any open decision the human owns has been surfaced (not silently resolved).
- Build/test commands for this project are loaded from `PROJECT_CONVENTIONS.md`, not guessed.

## Don't

- Don't start coding before reading Status + ROADMAP + open issues — you'll redo work or miss a decision.
- Don't re-litigate decisions already recorded in the `D-NN` log.
- Don't guess at a fork to keep momentum; a wrong architectural guess is expensive. Surface it.
- Don't re-run a full onboarding if the project is already loaded in context — just confirm the resume point.
