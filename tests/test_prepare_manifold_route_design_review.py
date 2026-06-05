import json
import tempfile
import unittest
from pathlib import Path

from tools import prepare_manifold_route_design_review
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
ROUTE_BLUEPRINT = REPO_ROOT / "fixtures" / "valid" / "manifold-route-blueprint.synthetic.json"
EXPECTED_REQUEST = REPO_ROOT / "fixtures" / "valid" / "manifold-route-design-review-request.synthetic.json"


class PrepareManifoldRouteDesignReviewTests(unittest.TestCase):
    def test_generator_matches_expected_request(self) -> None:
        generated = prepare_manifold_route_design_review.build_request(
            ROUTE_BLUEPRINT,
            REPO_ROOT,
            "2026-06-04T23:12:00Z",
        )
        expected = json.loads(EXPECTED_REQUEST.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-route-design-review-request.json"
            code = prepare_manifold_route_design_review.main(
                [
                    "--route-blueprint",
                    str(ROUTE_BLUEPRINT),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T23:12:00Z",
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
