"""Typed handoffs and deterministic publication boundary."""
from html import escape
from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Source(StrictModel):
    id: str
    url: str
    title: str
    text: str
    sha256: str
    fetched_at: str


class Angle(StrictModel):
    id: int
    observation: str = Field(min_length=10, max_length=350)
    source_id: str
    quote: str = Field(min_length=15, max_length=180)
    question: str = Field(min_length=10, max_length=350)


class Brief(StrictModel):
    angles: list[Angle] = Field(min_length=3, max_length=3)


class Verdict(StrictModel):
    angle_id: int
    supported: bool
    question_has_false_premise: bool
    reason: str


class Review(StrictModel):
    verdicts: list[Verdict]


def validate_evidence(brief: Brief, sources: list[Source]) -> None:
    by_id = {s.id: s for s in sources}
    if len({a.id for a in brief.angles}) != len(brief.angles):
        raise ValueError("duplicate angle ID")
    used_words: dict[str, int] = {}
    for angle in brief.angles:
        if angle.source_id not in by_id:
            raise ValueError(f"unknown source: {angle.source_id}")
        if angle.quote not in by_id[angle.source_id].text:
            raise ValueError(f"angle {angle.id}: quote not found verbatim in source")
        used_words[angle.source_id] = used_words.get(angle.source_id, 0) + len(angle.quote.split())
        if used_words[angle.source_id] > 25:
            raise ValueError("source quotation budget exceeded: 25 words")


def validate_review(brief: Brief, review: Review) -> None:
    expected = {a.id for a in brief.angles}
    actual = [v.angle_id for v in review.verdicts]
    if len(actual) != len(expected) or set(actual) != expected:
        raise ValueError("review must cover every angle exactly once")
    rejected = [v for v in review.verdicts if not v.supported or v.question_has_false_premise]
    if rejected:
        raise ValueError("semantic review rejected: " + "; ".join(v.reason for v in rejected))


def render(brief: Brief, review: Review, sources: list[Source], audience: str) -> str:
    validate_evidence(brief, sources)
    validate_review(brief, review)
    by_id = {s.id: s for s in sources}
    cards = []
    for angle in brief.angles:
        source = by_id[angle.source_id]
        cards.append(f'''<article><span class="number">0{angle.id}</span>
        <h2>{escape(angle.observation)}</h2>
        <p class="label">ASK THIS</p><p class="question">{escape(angle.question)}</p>
        <details><summary>Check the evidence</summary><blockquote>{escape(angle.quote)}</blockquote>
        <a href="{escape(source.url, quote=True)}" rel="noopener noreferrer">{escape(source.title)}</a>
        <p class="meta">Fetched {escape(source.fetched_at)} · SHA-256 {source.sha256[:12]}</p></details></article>''')
    return '''<!doctype html><html lang="en"><meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Three conversations worth having | Thomas Prommer</title>
    <style>body{margin:0;background:#f3f0e8;color:#182b2b;font:17px/1.65 system-ui,sans-serif}
    main{max-width:850px;margin:auto;padding:60px 24px}header{border-bottom:2px solid #182b2b;padding-bottom:30px}
    h1{font-size:clamp(36px,6vw,66px);line-height:1.05;letter-spacing:-2px;max-width:700px}
    h2{font-size:23px;line-height:1.4}a{color:#176659}article{padding:32px 0;border-bottom:1px solid #b9c5bb}
    .label,.number{font-size:12px;letter-spacing:2px;font-weight:700;color:#176659}.question{font-size:20px}
    summary{cursor:pointer;color:#176659}blockquote{border-left:3px solid #b59957;padding-left:18px;margin-left:0}
    .meta,footer{font-size:13px;color:#596b66}.badge{background:#dce9dd;padding:7px 12px;border-radius:30px;font-size:12px}
    footer{padding-top:30px}details{background:#e8e9df;padding:14px 20px;border-radius:8px}</style><main><header>
    <p class="label">PROMMER.NET / CONVERSATION INTELLIGENCE</p>
    <h1>Three conversations worth having.</h1>
    <p>A source-backed briefing for ''' + escape(audience) + '''.</p>
    <span class="badge">Evidence checked · AI reviewed · Human review required</span></header>''' + "".join(cards) + '''
    <footer>This independent research prototype uses claims from prommer.net, not independently verified biography.
    Questions are proposed discussion angles. Source capture time is not publication time.
    <p><a href="https://prommer.net/en/tech/">Explore Thomas's technology work →</a></p>
    Generated through fetch → draft → evidence check → independent review → render.</footer></main></html>'''
