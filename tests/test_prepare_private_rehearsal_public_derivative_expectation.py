import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_private_rehearsal_public_derivative_expectation
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_EXPECTATION = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-evidence-expectation.synthetic.json"
EXPECTED_EXPECTATION = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-public-derivative-expectation.synthetic.json"


class PreparePrivateRehearsalPublicDerivativeExpectationTests(unittest.TestCase):
    def test_generator_matches_expected_expectation(self) -> None:
        generated = prepare_private_rehearsal_public_derivative_expectation.build_expectation(
            EVIDENCE_EXPECTATION,
            REPO_ROOT,
            "2026-06-05T00:00:00Z",
        )
        expected = json.loads(EXPECTED_EXPECTATION.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "private-rehearsal-public-derivative-expectation.json"
            code = prepare_private_rehearsal_public_derivative_expectation.main(
                [
                    "--evidence-expectation",
                    str(EVIDENCE_EXPECTATION),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-05T00:00:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_EXPECTATION.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_expectation_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_EXPECTATION)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
