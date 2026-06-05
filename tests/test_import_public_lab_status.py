import json
import tempfile
import unittest
from pathlib import Path

from tools import import_public_lab_status
from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
QUEST_TERMUX_LAB = REPO_ROOT.parent / "quest-termux-lab"
MANIFEST = REPO_ROOT / "fixtures" / "valid" / "public-lab-artifact-intake-manifest.synthetic.json"
EXPECTED_REPORT = REPO_ROOT / "fixtures" / "valid" / "public-lab-artifact-intake-report.synthetic.json"


class ImportPublicLabStatusTests(unittest.TestCase):
    def test_importer_generates_expected_fixture(self) -> None:
        manifest = import_public_lab_status.load_json(MANIFEST)
        generated = import_public_lab_status.build_report(
            manifest,
            QUEST_TERMUX_LAB,
            "2026-06-04T21:41:00Z",
        )
        expected = import_public_lab_status.load_json(EXPECTED_REPORT)
        self.assertEqual(expected, generated)

    def test_cli_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.json"
            code = import_public_lab_status.main(
                [
                    "--manifest",
                    str(MANIFEST),
                    "--source-root",
                    str(QUEST_TERMUX_LAB),
                    "--now",
                    "2026-06-04T21:41:00Z",
                    "--output",
                    str(output),
                ]
            )
            self.assertEqual(0, code)
            self.assertEqual(json.loads(EXPECTED_REPORT.read_text(encoding="utf-8")), json.loads(output.read_text(encoding="utf-8")))

    def test_path_escape_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            import_public_lab_status.require_relative_path("../private.json")

    def test_report_passes_repo_validator(self) -> None:
        result = validate_repo.validate_json_file(EXPECTED_REPORT)
        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
