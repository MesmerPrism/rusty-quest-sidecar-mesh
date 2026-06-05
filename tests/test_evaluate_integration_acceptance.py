import json
import tempfile
import unittest
from pathlib import Path

from tools import evaluate_integration_acceptance
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SCORECARD = REPO_ROOT / "fixtures" / "valid" / "integration-acceptance-scorecard.synthetic.json"


class EvaluateIntegrationAcceptanceTests(unittest.TestCase):
    def test_generator_matches_expected_scorecard(self) -> None:
        generated = evaluate_integration_acceptance.build_scorecard(REPO_ROOT, "2026-06-04T21:46:00Z")
        expected = json.loads(EXPECTED_SCORECARD.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_scorecard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "scorecard.json"
            code = evaluate_integration_acceptance.main(
                [
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T21:46:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_SCORECARD.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_scorecard_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_SCORECARD)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()

