# ARCHITECTURE — &lt;PROJECT_NAME&gt;

The durable description of the system's shape, its non-negotiable invariants, and the log of every architectural decision. Onboarding drafts this from the `_intake/` brief; it's updated whenever a `D-NN` decision is made. Keep it honest and current — `plan_work` and `review_against_library` both lean on it.

## 1. Shape

&lt;The high-level structure: the layers / components / data flow, and the one-sentence thesis of the design. A diagram (ASCII or linked) helps. Ground the shape in the library — e.g. "see Book NN §X / DECISION_TREES D1".&gt;

## 2. Invariants (the non-negotiables)

The properties that must hold no matter what. Every change is checked against these; `definition_of_done` gates on them. *(Examples — replace with the real ones for &lt;PROJECT_NAME&gt;:)*

- **&lt;Invariant 1&gt;** — &lt;e.g. determinism of the core: same inputs → same outputs; no wall-clock / unordered-map iteration in the core path&gt;.
- **&lt;Invariant 2&gt;** — &lt;e.g. headless operability: no hard dependency on a window, device, or human; CI can run it&gt;.
- **&lt;Invariant 3&gt;** — &lt;e.g. a versioned public interface: schemas never change silently&gt;.

## 3. Subsystems

&lt;One subsection per major component: its responsibility, its boundary, the key types, and the book section(s) behind it. Fill as the system grows.&gt;

## 4. Risks

&lt;Optional: the known risks `R1..` with a mitigation each. Surface the scary ones early.&gt;

| # | Risk | Mitigation |
|---|------|------------|
| R1 | &lt;what could go wrong&gt; | &lt;how it's contained&gt; |

---

## Appendix A — Decision Log

Every architectural decision, recorded once and referred to thereafter. When a fork is resolved (see [CLAUDE.md](../CLAUDE.md) § *How we work* #3), add a row here — the **Choice** (not just the question) and its **Grounding** (the library section / decision tree behind it). The Status block and ROADMAP reference these by number. Decisions lean to the most ambitious, complete option unless the trade-off says otherwise.

| # | Decision | Choice | Grounding |
|---|----------|--------|-----------|
| D-01 | &lt;the fork, e.g. "core architecture"&gt; | &lt;what was chosen&gt; | &lt;Book NN §X; DECISION_TREES D1&gt; <!-- EXAMPLE — replace --> |
| D-02 | &lt;the fork, e.g. "primary stack"&gt; | &lt;what was chosen&gt; | &lt;Book MM §Y; DECISION_TREES D2&gt; <!-- EXAMPLE — replace --> |

> **Adding a decision:** append the next `D-NN`; cite the grounding (verify the `Book NN §X` against `textbooks/SECTIONS.json` first); reflect it in `docs/ROADMAP.md` and the `CLAUDE.md` Status block. Don't re-litigate a logged decision — supersede it with a new row that references the old one if it genuinely changes.
