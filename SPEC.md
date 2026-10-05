# Evidence-first operator briefing

User: a founder or podcast booker deciding what to discuss with Thomas Prommer.
Input: an explicit audience and a fixed allowlist of public prommer.net technology pages.
Output: a short HTML briefing containing three verbatim source excerpts, original interview questions, and a relevant next step. It is a dated research snapshot, not an assertion that the source claims have been independently verified. Free-form factual paraphrases are deliberately excluded: a live draft overstated a source recommendation as a general cause of failure, and the model reviewer incorrectly accepted it.

Contract: fetch -> Codex drafting session -> deterministic evidence check -> separate Codex review session -> render. Only an approved review can produce an HTML deliverable. A citation must reference a fetched document and contain an exact source excerpt. Sources are untrusted data, never tool instructions. No messages or emails are sent. Codex CLI is the sole model execution path; the earlier SDK experiment is removed. Each session is ephemeral, uses an isolated working directory, read-only sandbox, no user-config integrations, and disabled shell/browser/app/plugin tools.

Every stage writes an inspectable artifact. A manifest records model, timestamps, stage duration, token usage, source hashes and outcome. Provider failure stops the run; no fabricated/offline model output. A review rejection preserves the draft and exits nonzero. Output rendering escapes all text. A run directory must be new to prevent mixing a rejected run with an old approved page.

Acceptance cases: approved draft renders; invented citation rejected; wrong document rejected; partial or duplicated semantic review rejected; reviewer rejection prevents rendering; HTML injection escaped; rerun cannot reuse existing directory.

Limit: exact excerpts establish provenance, not the truth of the source or freedom from selective quotation; the independent model checks context and question premises but can still be wrong. Human review is required before using this briefing as outbound communication. Both agents currently use separate calls to the same model, so their errors may correlate.
