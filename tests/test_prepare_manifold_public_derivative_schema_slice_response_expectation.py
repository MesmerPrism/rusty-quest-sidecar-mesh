import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_manifold_public_derivative_schema_slice_response_expectation
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PACKAGE = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-handoff-package.synthetic.json"
EXPECTED_EXPECTATION = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-expectation.synthetic.json"


class PrepareManifoldPublicDerivativeSchemaSliceResponseExpectationTests(unittest.TestCase):
    def test_generator_matches_expected_expectation(self) -> None:
        generated = prepare_manifold_public_derivative_schema_slice_response_expectation.build_expectation(
            HANDOFF_PACKAGE,
            REPO_ROOT,
            "2026-06-05T00:40:00Z",
        )
        expected = json.loads(EXPECTED_EXPECTATION.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-public-derivative-schema-slice-response-expectation.json"
            code = prepare_manifold_public_derivative_schema_slice_response_expectation.main(
                [
                    "--handoff-package",
                    str(HANDOFF_PACKAGE),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-05T00:40:00Z",
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
