import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_manifold_response_implementation_preflight
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
RESPONSE_EXPECTATION = REPO_ROOT / "fixtures" / "valid" / "manifold-route-design-response-expectation.synthetic.json"
EXPECTED_PREFLIGHT = REPO_ROOT / "fixtures" / "valid" / "manifold-response-implementation-preflight.synthetic.json"


class PrepareManifoldResponseImplementationPreflightTests(unittest.TestCase):
    def test_generator_matches_expected_preflight(self) -> None:
        generated = prepare_manifold_response_implementation_preflight.build_preflight(
            RESPONSE_EXPECTATION,
            REPO_ROOT,
            "2026-06-04T23:28:00Z",
        )
        expected = json.loads(EXPECTED_PREFLIGHT.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-response-implementation-preflight.json"
            code = prepare_manifold_response_implementation_preflight.main(
                [
                    "--response-expectation",
                    str(RESPONSE_EXPECTATION),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T23:28:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_PREFLIGHT.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_preflight_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_PREFLIGHT)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
