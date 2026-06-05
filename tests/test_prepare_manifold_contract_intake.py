import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_manifold_contract_intake
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PACKAGE = REPO_ROOT / "fixtures" / "valid" / "manifold-handoff-package.synthetic.json"
EXPECTED_REQUEST = REPO_ROOT / "fixtures" / "valid" / "manifold-contract-intake-request.synthetic.json"


class PrepareManifoldContractIntakeTests(unittest.TestCase):
    def test_generator_matches_expected_request(self) -> None:
        generated = prepare_manifold_contract_intake.build_request(HANDOFF_PACKAGE, REPO_ROOT, "2026-06-04T22:48:00Z")
        expected = json.loads(EXPECTED_REQUEST.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-contract-intake-request.json"
            code = prepare_manifold_contract_intake.main(
                [
                    "--handoff-package",
                    str(HANDOFF_PACKAGE),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T22:48:00Z",
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
