import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from contracts import Source, Angle, Brief, Verdict, Review, validate_evidence, validate_review, render
from pipeline import run

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.sources = [Source(id=f"s{i}", url=f"https://prommer.net/en/page-{i}/",
            title=f"Source {i}", text=f"The site describes engineering tradeoffs in case {i}.",
            sha256="a" * 64, fetched_at="2026-10-05T00:00:00Z") for i in range(1, 4)]
        self.brief = Brief(angles=[Angle(id=i, source_id=f"s{i}",
            quote=self.sources[i-1].text,
            question="Which tradeoff would you measure first?") for i in range(1, 4)])
        self.review = Review(verdicts=[Verdict(angle_id=i, supported=True,
            question_has_false_premise=False, reason="Supported by the cited text.") for i in range(1,4)])

    def test_approved_draft_renders(self):
        html = render(self.brief, self.review, self.sources, "founders")
        self.assertEqual(html.count("<article>"), 3)
        self.assertIn("https://prommer.net/en/page-1/", html)

    def test_invented_citation_rejected(self):
        self.brief.angles[0].quote = "An invented quote claiming ten million dollars."
        with self.assertRaisesRegex(ValueError, "not found verbatim"):
            validate_evidence(self.brief, self.sources)

    def test_wrong_document_rejected(self):
        self.brief.angles[0].source_id = "external-source"
        with self.assertRaisesRegex(ValueError, "unknown source"):
            validate_evidence(self.brief, self.sources)

    def test_partial_or_duplicate_review_rejected(self):
        for verdicts in [self.review.verdicts[:2], [self.review.verdicts[0]] * 3]:
            with self.subTest(verdicts=verdicts):
                with self.assertRaisesRegex(ValueError, "every angle exactly once"):
                    validate_review(self.brief, Review(verdicts=verdicts))

    def test_reviewer_rejection_blocks_rendering(self):
        self.review.verdicts[0].supported = False
        with self.assertRaisesRegex(ValueError, "semantic review rejected"):
            render(self.brief, self.review, self.sources, "founders")

    def test_html_is_escaped(self):
        self.brief.angles[0].question = '<script>alert("x")</script>'
        html = render(self.brief, self.review, self.sources, "<img src=x onerror=alert(1)>")
        self.assertNotIn("<script>", html)
        self.assertNotIn("<img", html)
        self.assertIn("&lt;script&gt;", html)

    def test_existing_run_directory_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("pipeline.fetch_sources") as fetch:
                with self.assertRaises(FileExistsError):
                    run(Path(directory), "founders", "unused")
                fetch.assert_not_called()

    def test_failed_fetch_persists_failure_without_html(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "new"
            with patch("pipeline.fetch_sources", side_effect=TimeoutError("source timed out")):
                with self.assertRaises(TimeoutError):
                    run(output, "founders", "unused")
            self.assertFalse((output / "index.html").exists())
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["status"], "failed")
            self.assertEqual(manifest["stage"], "fetch")

    def test_real_quote_does_not_override_semantic_rejection(self):
        self.brief.angles[0].question = "How did this engineering approach guarantee a million dollars?"
        validate_evidence(self.brief, self.sources)
        self.review.verdicts[0].supported = False
        self.review.verdicts[0].reason = "The source does not establish a revenue outcome."
        with self.assertRaisesRegex(ValueError, "revenue outcome"):
            render(self.brief, self.review, self.sources, "founders")


if __name__ == "__main__":
    unittest.main()
