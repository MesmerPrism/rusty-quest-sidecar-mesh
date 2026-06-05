import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_hostess_boundary_descriptor_expectation
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
RESPONSE_HANDOFF = REPO_ROOT / "fixtures" / "valid" / "manifold-response-handoff-package.synthetic.json"
EXPECTED_EXPECTATION = REPO_ROOT / "fixtures" / "valid" / "hostess-boundary-descriptor-expectation.synthetic.json"


class PrepareHostessBoundaryDescriptorExpectationTests(unittest.TestCase):
    def test_generator_matches_expected_expectation(self) -> None:
        generated = prepare_hostess_boundary_descriptor_expectation.build_expectation(
            RESPONSE_HANDOFF,
            REPO_ROOT,
            "2026-06-04T23:44:00Z",
        )
        expected = json.loads(EXPECTED_EXPECTATION.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_expectation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "hostess-boundary-descriptor-expectation.json"
            code = prepare_hostess_boundary_descriptor_expectation.main(
                [
                    "--response-handoff",
                    str(RESPONSE_HANDOFF),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T23:44:00Z",
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
