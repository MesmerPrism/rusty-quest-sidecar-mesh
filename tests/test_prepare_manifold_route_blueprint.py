import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_manifold_route_blueprint
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_INTAKE_REQUEST = REPO_ROOT / "fixtures" / "valid" / "manifold-contract-intake-request.synthetic.json"
PRIVATE_APPROVAL_REQUEST = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-approval-request.synthetic.json"
EXPECTED_BLUEPRINT = REPO_ROOT / "fixtures" / "valid" / "manifold-route-blueprint.synthetic.json"


class PrepareManifoldRouteBlueprintTests(unittest.TestCase):
    def test_generator_matches_expected_blueprint(self) -> None:
        generated = prepare_manifold_route_blueprint.build_blueprint(
            CONTRACT_INTAKE_REQUEST,
            PRIVATE_APPROVAL_REQUEST,
            REPO_ROOT,
            "2026-06-04T23:04:00Z",
        )
        expected = json.loads(EXPECTED_BLUEPRINT.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_blueprint(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-route-blueprint.json"
            code = prepare_manifold_route_blueprint.main(
                [
                    "--contract-intake-request",
                    str(CONTRACT_INTAKE_REQUEST),
                    "--private-approval-request",
                    str(PRIVATE_APPROVAL_REQUEST),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T23:04:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_BLUEPRINT.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_blueprint_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_BLUEPRINT)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
