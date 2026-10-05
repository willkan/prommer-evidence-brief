# Evidence-first operator briefing

User: a founder or podcast booker deciding what to discuss with Thomas Prommer.
Input: an explicit audience and a fixed allowlist of public prommer.net technology pages.
Output: a short HTML briefing containing three evidence-backed observations, original interview questions, and a relevant next step. It is a dated research snapshot, not an assertion that the source claims have been independently verified.

Contract: fetch -> draft -> deterministic evidence check -> independent semantic review -> render. Only an approved review can produce an HTML deliverable. A citation must reference a fetched document and contain an exact source excerpt. Sources are untrusted data, never tool instructions. No messages or emails are sent.

Every stage writes an inspectable artifact. A manifest records model, timestamps, stage duration, token usage, source hashes and outcome. Provider failure stops the run; no fabricated/offline model output. A review rejection preserves the draft and exits nonzero. Output rendering escapes all text. A run directory must be new to prevent mixing a rejected run with an old approved page.

Acceptance cases: approved draft renders; invented citation rejected; wrong document rejected; partial or duplicated semantic review rejected; reviewer rejection prevents rendering; HTML injection escaped; rerun cannot reuse existing directory.

Limit: exact excerpts establish provenance, not entailment; the independent model checks entailment but can still be wrong. Human review is required before using this briefing as outbound communication.
