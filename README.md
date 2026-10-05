# Three conversations worth having

A small, working research pipeline for founders and podcast bookers exploring Thomas Prommer's technology work. It turns three public prommer.net pages into a briefing of exact source excerpts and proposed interview questions.

## Read the output

- [Generated briefing](index.html) — download and open in a browser, or use the repository's GitHub Pages deployment.
- [Draft handoff](draft.json), [review handoff](review.json), and [run manifest](manifest.json).
- [Output contract](SPEC.md) and [contract tests](test_pipeline.py).

The manifest records capture times, source hashes, execution times and actual Codex token usage. It is evidence of a particular run, not a benchmark or a claim of continuous operation.

## Run it

Prerequisites: Python 3.11+, an installed Codex CLI with existing login (`codex login`), and network access to prommer.net and the Codex service.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest -v
python pipeline.py --out runs/first
```

Use a new output directory each time. `--audience 'podcast bookers'` changes the editorial audience; `--model MODEL` explicitly selects a Codex model. Without it, the CLI chooses its default. No API credential is embedded in this repository.

## What actually runs

1. Fetch three allowlisted technology, press and venture pages. Extract their main content and hash the exact normalized text.
2. Run a fresh Codex CLI session with a JSON output schema to select excerpts and propose questions.
3. Reject unknown source references, fabricated excerpts and excessive quotation.
4. Run a separate Codex session against the sources and draft. It checks context and unsupported premises in questions.
5. Require exactly one accepting verdict per angle before generating escaped HTML.

The CLI runs in an isolated directory, with a read-only sandbox and shell/browser/app/plugin integrations disabled. Inputs, schema, events and outputs are saved locally for diagnosis. The public sample includes only short excerpts, verdicts and metadata, not complete source pages.

## The failure that changed the design

An initial SDK experiment hit a schema-transport error, then model availability errors. More significantly, an eventual live draft-and-review run passed while overstating a source recommendation as a general cause of enterprise failure. Human inspection caught that semantic error.

The final contract removes the free-form factual observation field. Models select exact excerpts and propose questions; deterministic checks enforce excerpt provenance. Codex CLI is now the only execution path; the SDK branch was removed rather than retained as fallback.

## Limits

Exact text membership does not prove a source is true or that a quotation is representative. The reviewer uses a separate context but may share the writer's model and blind spots. Human editorial review remains necessary. This prototype does not send emails, schedule jobs or claim third-party verification of the site's biography. Nine deterministic tests protect the publication boundary; they are not an evaluation of general model accuracy.

Built with AI assistance. No reuse licence is granted by this repository.
