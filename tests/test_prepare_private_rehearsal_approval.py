import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_private_rehearsal_approval
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
PEER_PLAN = REPO_ROOT / "fixtures" / "valid" / "configured-peer-rehearsal-plan.synthetic.json"
CONTRACT_INTAKE_REQUEST = REPO_ROOT / "fixtures" / "valid" / "manifold-contract-intake-request.synthetic.json"
EXPECTED_REQUEST = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-approval-request.synthetic.json"


class PreparePrivateRehearsalApprovalTests(unittest.TestCase):
    def test_generator_matches_expected_request(self) -> None:
        generated = prepare_private_rehearsal_approval.build_request(
            PEER_PLAN,
            CONTRACT_INTAKE_REQUEST,
            REPO_ROOT,
            "2026-06-04T22:56:00Z",
        )
        expected = json.loads(EXPECTED_REQUEST.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "private-rehearsal-approval-request.json"
            code = prepare_private_rehearsal_approval.main(
                [
                    "--peer-plan",
                    str(PEER_PLAN),
                    "--contract-intake-request",
                    str(CONTRACT_INTAKE_REQUEST),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T22:56:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_REQUEST.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_request_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_REQUEST)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
