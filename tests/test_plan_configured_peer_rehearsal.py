import json
import tempfile
import unittest
from pathlib import Path

from tools import plan_configured_peer_rehearsal
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_REVIEW = REPO_ROOT / "fixtures" / "valid" / "no-network-prototype-handoff-review.synthetic.json"
EXPECTED_PLAN = REPO_ROOT / "fixtures" / "valid" / "configured-peer-rehearsal-plan.synthetic.json"


class PlanConfiguredPeerRehearsalTests(unittest.TestCase):
    def test_generator_matches_expected_plan(self) -> None:
        generated = plan_configured_peer_rehearsal.build_plan(HANDOFF_REVIEW, REPO_ROOT, "2026-06-04T22:25:00Z")
        expected = json.loads(EXPECTED_PLAN.read_text(encoding="utf-8"))
        self.assertEqual(expected, generated)

    def test_cli_writes_plan(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "configured-peer-rehearsal-plan.json"
            code = plan_configured_peer_rehearsal.main(
                [
                    "--handoff-review",
                    str(HANDOFF_REVIEW),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T22:25:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_PLAN.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_plan_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_PLAN)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
