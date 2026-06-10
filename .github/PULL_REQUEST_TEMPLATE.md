<!-- PR title convention: M<n> <slice>: <imperative summary> (closes #<issue>) -->

## What & why

<one short paragraph. Closes #NN.>

## Definition-of-done evidence

<output, not assertion — paste the relevant summaries>

- **Build / tests / lint:** <result>
- **Domain gates** (state round-trip · headless · determinism — as applicable): <PASS / N/A + evidence>
- **Performance claims:** <profile reference, or "none claimed">
- **Library:** citations verified against SECTIONS.json; frontier claims cite research/ notes (sourced + tiered); audits green if textbooks/ or research/ changed

## Tracker hygiene

- [ ] No naked TODO/FIXME introduced — `TODO(#NN)` only (CI hygiene job enforces)
- [ ] Deferred work filed as issues: <#… / none>
- [ ] Decisions touched: <D-NN recorded in ARCHITECTURE Appendix A / none>
- [ ] Merge-time checkpoint done: Status line + ROADMAP state reflect this merge
