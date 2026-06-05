import json
import tempfile
import unittest
from pathlib import Path

from tools import package_manifold_response_handoff
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = REPO_ROOT / "fixtures" / "valid" / "manifold-response-implementation-preflight.synthetic.json"
EXPECTED_PACKAGE = REPO_ROOT / "fixtures" / "valid" / "manifold-response-handoff-package.synthetic.json"


class PackageManifoldResponseHandoffTests(unittest.TestCase):
    def test_generator_matches_expected_package(self) -> None:
        generated = package_manifold_response_handoff.build_package(
            PREFLIGHT,
            REPO_ROOT,
            "2026-06-04T23:36:00Z",
        )
        expected = json.loads(EXPECTED_PACKAGE.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-response-handoff-package.json"
            code = package_manifold_response_handoff.main(
                [
                    "--preflight",
                    str(PREFLIGHT),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T23:36:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_PACKAGE.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_package_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_PACKAGE)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
