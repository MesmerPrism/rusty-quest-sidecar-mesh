import json
import tempfile
import unittest
from pathlib import Path

from tools import review_manifold_adapter_contract
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
PEER_PLAN = REPO_ROOT / "fixtures" / "valid" / "configured-peer-rehearsal-plan.synthetic.json"
EXPECTED_REVIEW = REPO_ROOT / "fixtures" / "valid" / "manifold-adapter-contract-review.synthetic.json"


class ReviewManifoldAdapterContractTests(unittest.TestCase):
    def test_generator_matches_expected_review(self) -> None:
        generated = review_manifold_adapter_contract.build_review(PEER_PLAN, REPO_ROOT, "2026-06-04T22:32:00Z")
        expected = json.loads(EXPECTED_REVIEW.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "manifold-adapter-contract-review.json"
            code = review_manifold_adapter_contract.main(
                [
                    "--peer-plan",
                    str(PEER_PLAN),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T22:32:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_REVIEW.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_contract_review_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_REVIEW)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
