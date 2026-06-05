import json
import tempfile
import unittest
from pathlib import Path

from tools import review_no_network_recipe
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
RECIPE = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-recipe.synthetic.json"
EXPECTED_REVIEW = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-recipe-review.synthetic.json"


class ReviewNoNetworkRecipeTests(unittest.TestCase):
    def test_generator_matches_expected_review(self) -> None:
        generated = review_no_network_recipe.build_review(RECIPE, REPO_ROOT, "2026-06-04T22:05:00Z")
        expected = json.loads(EXPECTED_REVIEW.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "review.json"
            code = review_no_network_recipe.main(
                [
                    "--recipe",
                    str(RECIPE),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T22:05:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_REVIEW.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_review_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_REVIEW)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()

