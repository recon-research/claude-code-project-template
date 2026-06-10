# &lt;DOMAIN&gt; — Knowledge Library

A structured, self-validating RAG knowledge library for **&lt;DOMAIN&gt;**, with the example system named **&lt;EXAMPLE_SYSTEM&gt;**. It is the reference the project's Claude Code agent consults and cites while building. *(Currently a blank template — only the book template exists. Build it with [`build_library`](../.claude/skills/build_library/SKILL.md), driven by [LIBRARY_SEED.md](LIBRARY_SEED.md).)*

## What's here

| Path | What it is |
|------|------------|
| [LIBRARY_SEED.md](LIBRARY_SEED.md) | The complete instruction set for **building** this library from scratch in any domain. Start here. |
| [CLAUDE.md](CLAUDE.md) | Rules for **consulting** the library (routing table, citation discipline). |
| [AGENT_GUIDE.md](AGENT_GUIDE.md) | The **build loop** that turns the library into shipped work. |
| `MANIFEST.json` | Machine index: `topic_to_books`, `rag_hints`, per-book metadata, `coverage_gaps`. |
| `SECTIONS.json` | Generated index of every heading (for resolving/verifying `Book NN §X`). |
| `ROUTING_EVAL.json` | Routing smoke-tests (query → expected target). |
| [books/](books/) | The curriculum, numbered and grouped into volumes. (`00_TEMPLATE.md` is the template.) |
| [reference/](reference/) | Lookup docs: INDEX, GLOSSARY, ANTI_PATTERNS, DECISION_TREES, SYMPTOMS, PATTERNS, WORKFLOWS, STARTER_KIT. |
| [vision/](vision/) | Inspirational docs: PROLOGUE, FUTURES, MOONSHOTS. |
| [tools/](tools/) | The four maintenance scripts that keep the library honest. |

## Reading paths

- **To learn the domain (human):** start at the lowest-numbered book and read in order, or jump via [reference/INDEX.md](reference/INDEX.md).
- **To build something (agent):** follow [AGENT_GUIDE.md](AGENT_GUIDE.md) — route via `MANIFEST.json`, resolve sections via `SECTIONS.json`, pre-mortem via [reference/ANTI_PATTERNS.md](reference/ANTI_PATTERNS.md).

## Stats

- **Books:** 1 (the template) · **Volumes:** 1 · **Reference docs:** 8 · **Status:** template — not yet populated.
  *(Counts drift; trust the scripts, not this line. Update after any structural change.)*

## Keeping it honest

Run from this directory after any change to books or headings:

```
python tools/_gen_sections.py     # regenerate SECTIONS.json
python tools/_audit_refs.py        # 0 unresolved Book NN §X references
python tools/_audit_routing.py     # all ROUTING_EVAL cases pass
python tools/_audit_links.py       # 0 broken markdown links
```

A library that passes all four is internally consistent. The scripts **exit non-zero on failure**, so CI enforces them as a real merge gate (see [`../.github/workflows/ci.yml`](../.github/workflows/ci.yml)). See [LIBRARY_SEED.md](LIBRARY_SEED.md) §4 and §8.
