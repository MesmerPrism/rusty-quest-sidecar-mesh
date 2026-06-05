import json
import tempfile
import unittest
from pathlib import Path

from tools import review_public_lab_artifact_drift
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
QUEST_TERMUX_LAB = REPO_ROOT.parent / "quest-termux-lab"
MANIFEST = REPO_ROOT / "fixtures" / "valid" / "public-lab-artifact-intake-manifest.synthetic.json"
REPORT = REPO_ROOT / "fixtures" / "valid" / "public-lab-artifact-intake-report.synthetic.json"
EXPECTED_REVIEW = REPO_ROOT / "fixtures" / "valid" / "public-lab-artifact-drift-review.synthetic.json"


class ReviewPublicLabArtifactDriftTests(unittest.TestCase):
    def test_generator_matches_expected_review(self) -> None:
        generated = review_public_lab_artifact_drift.build_review(
            MANIFEST,
            REPORT,
            QUEST_TERMUX_LAB,
            REPO_ROOT,
            "2026-06-04T21:43:00Z",
        )
        expected = json.loads(EXPECTED_REVIEW.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "public-lab-artifact-drift-review.json"
            code = review_public_lab_artifact_drift.main(
                [
                    "--manifest",
                    str(MANIFEST),
                    "--report",
                    str(REPORT),
                    "--source-root",
                    str(QUEST_TERMUX_LAB),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T21:43:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_REVIEW.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_review_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_REVIEW)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
