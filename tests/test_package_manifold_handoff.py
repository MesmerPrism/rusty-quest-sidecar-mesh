import json
import tempfile
import unittest
from pathlib import Path

from tools import package_manifold_handoff
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_REVIEW = REPO_ROOT / "fixtures" / "valid" / "manifold-adapter-contract-review.synthetic.json"
EXPECTED_PACKAGE = REPO_ROOT / "fixtures" / "valid" / "manifold-handoff-package.synthetic.json"


class PackageManifoldHandoffTests(unittest.TestCase):
    def test_generator_matches_expected_package(self) -> None:
        generated = package_manifold_handoff.build_package(CONTRACT_REVIEW, REPO_ROOT, "2026-06-04T22:40:00Z")
        expected = json.loads(EXPECTED_PACKAGE.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_package(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-handoff-package.json"
            code = package_manifold_handoff.main(
                [
                    "--contract-review",
                    str(CONTRACT_REVIEW),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T22:40:00Z",
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
