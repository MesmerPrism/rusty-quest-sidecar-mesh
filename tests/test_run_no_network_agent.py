import json
import tempfile
import unittest
from pathlib import Path

from tools import run_no_network_agent
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
RECIPE = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-recipe.synthetic.json"
REVIEW = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-recipe-review.synthetic.json"
EXPECTED_OBSERVATION = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-observation.synthetic.json"
EXPECTED_REPORT = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-run.synthetic.json"


class RunNoNetworkAgentTests(unittest.TestCase):
    def test_generator_matches_expected_outputs(self) -> None:
        observation, report = run_no_network_agent.build_outputs(
            RECIPE,
            REVIEW,
            EXPECTED_OBSERVATION,
            REPO_ROOT,
            "2026-06-04T22:12:00Z",
            2,
            "agent.quest_sidecar.synthetic_alpha",
        )
        self.assertEqual(json.loads(EXPECTED_OBSERVATION.read_text(encoding="utf-8")), observation)
        self.assertEqual(json.loads(EXPECTED_REPORT.read_text(encoding="utf-8")), report)

    def test_cli_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            observation_output = Path(temp_dir) / "observation.json"
            report_output = Path(temp_dir) / "run.json"
            code = run_no_network_agent.main(
                [
                    "--recipe",
                    str(RECIPE),
                    "--review",
                    str(REVIEW),
                    "--repo-root",
                    str(REPO_ROOT),
                    "--now",
                    "2026-06-04T22:12:00Z",
                    "--sequence",
                    "2",
                    "--observation-output",
                    str(observation_output),
                    "--report-output",
                    str(report_output),
                ]
            )
            self.assertEqual(0, code)
            observation = json.loads(observation_output.read_text(encoding="utf-8"))
            report = json.loads(report_output.read_text(encoding="utf-8"))
            self.assertEqual("rusty.quest.sidecar.observation.v1", observation["schema"])
            self.assertEqual("prototype_complete", report["prototype_status"])
            self.assertTrue(validate_repo.validate_fixture(observation) == [])

    def test_run_report_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_REPORT)
        self.assertTrue(result.ok, result.errors)

    def test_generated_observation_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_OBSERVATION)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()

