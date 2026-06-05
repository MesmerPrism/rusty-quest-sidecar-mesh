import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_manifold_public_derivative_schema_slice_response_operator_decision_request
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PACKAGE = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json"
EXPECTED_REQUEST = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json"


class PrepareManifoldPublicDerivativeSchemaSliceResponseOperatorDecisionRequestTests(unittest.TestCase):
    def test_generator_matches_expected_request(self) -> None:
        generated = prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.build_request(
            HANDOFF_PACKAGE,
            REPO_ROOT,
            "2026-06-05T01:04:00Z",
        )
        expected = json.loads(EXPECTED_REQUEST.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-public-derivative-schema-slice-response-operator-decision-request.json"
            code = prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.main(
                [
                    "--handoff-package",
                    str(HANDOFF_PACKAGE),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-05T01:04:00Z",
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
