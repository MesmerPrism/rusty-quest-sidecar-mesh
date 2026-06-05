import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_private_rehearsal_evidence_expectation
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
APPROVAL_REQUEST = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-approval-request.synthetic.json"
HOSTESS_EXPECTATION = REPO_ROOT / "fixtures" / "valid" / "hostess-boundary-descriptor-expectation.synthetic.json"
EXPECTED_EXPECTATION = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-evidence-expectation.synthetic.json"


class PreparePrivateRehearsalEvidenceExpectationTests(unittest.TestCase):
    def test_generator_matches_expected_expectation(self) -> None:
        generated = prepare_private_rehearsal_evidence_expectation.build_expectation(
            APPROVAL_REQUEST,
            HOSTESS_EXPECTATION,
            REPO_ROOT,
            "2026-06-04T23:52:00Z",
        )
        expected = json.loads(EXPECTED_EXPECTATION.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "private-rehearsal-evidence-expectation.json"
            code = prepare_private_rehearsal_evidence_expectation.main(
                [
                    "--approval-request",
                    str(APPROVAL_REQUEST),
                    "--hostess-expectation",
                    str(HOSTESS_EXPECTATION),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T23:52:00Z",
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
