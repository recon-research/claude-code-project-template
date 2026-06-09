# ROADMAP — &lt;PROJECT_NAME&gt;

The live plan. Mirrors the milestone order in [`textbooks/reference/STARTER_KIT.md`](../textbooks/reference/STARTER_KIT.md) and adds per-milestone status. Onboarding drafts it; every session updates the status of the slice it touched. The `CLAUDE.md` Status block is the 10-line summary of this file.

**Status legend:** ☐ todo · ◐ in progress · ☑ done · ⊘ blocked · ✂ cut

## Milestones

Each milestone has a **goal**, **slices** (each → a GitHub issue/PR), a verifiable **exit criterion**, a **leverage** note (where the agent is high-leverage vs ~1× human judgment), and **status**.

### M0 — &lt;Foundation: the smallest runnable skeleton&gt;
- **Goal:** &lt;one line&gt;
- **Slices:** ☐ &lt;slice a (#)&gt; · ☐ &lt;slice b (#)&gt;
- **Exit criterion:** &lt;verifiable, ideally CI-gated — e.g. "the skeleton builds, tests pass, and the headless smoke runs N steps"&gt;
- **Leverage:** &lt;e.g. high — boilerplate/scaffolding&gt;
- **Status:** ◐ &lt;what's done / next&gt;

### M1 — &lt;the next vertical slice&gt;
- **Goal:** &lt;one line&gt;
- **Slices:** ☐ &lt;…&gt;
- **Exit criterion:** &lt;…&gt;
- **Leverage:** &lt;…&gt;
- **Status:** ☐ not started

### M2.. — &lt;to be filled during onboarding&gt;
&lt;Continue the milestone list from the approved STARTER_KIT. Keep each exit criterion verifiable.&gt;

## Open decisions

Forks not yet resolved, each with a **recommended (ambitious) default** and how/when it gets decided. These surface to the human per `CLAUDE.md` §3; once chosen they become `D-NN` in [ARCHITECTURE.md](ARCHITECTURE.md) Appendix A.

- &lt;Open decision 1&gt; — recommended: &lt;default&gt;; decided at: &lt;milestone / when&gt;.
- &lt;Open decision 2&gt; — recommended: &lt;default&gt;; decided at: &lt;…&gt;.

## Cut order

If time runs short, the order things get cut (last-to-first) — so scope-trimming is a decision made in advance, not a panic. Never cut the foundation milestones (M0–&lt;Mk&gt;).

1. ✂ &lt;the first thing to drop&gt;
2. ✂ &lt;next&gt;
