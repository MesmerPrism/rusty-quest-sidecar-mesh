#!/usr/bin/env python3
"""Review sanitized quest-termux-lab intake for source drift."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import import_public_lab_status
from tools import validate_repo


REVIEW_SCHEMA = "rusty.quest.sidecar.public_lab_artifact_drift_review.v1"
MANIFEST_SCHEMA = "rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1"
REPORT_SCHEMA = "rusty.quest.sidecar.public_lab_artifact_intake_report.v1"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=2)
        handle.write("\n")


def relative_output_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def check(check_id: str, passed: bool, observed: Any, expected: Any, evidence: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "pass" if passed else "fail",
        "observed": observed,
        "expected": expected,
        "evidence": evidence,
    }


def artifact_by_id(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {artifact.get("artifact_id", ""): artifact for artifact in report.get("artifacts", []) if isinstance(artifact, dict)}


def compare_artifacts(stored_report: dict[str, Any], current_report: dict[str, Any], manifest: dict[str, Any], source_root: Path) -> list[dict[str, Any]]:
    stored_by_id = artifact_by_id(stored_report)
    current_by_id = artifact_by_id(current_report)
    comparisons: list[dict[str, Any]] = []
    for ref in manifest.get("artifact_refs", []):
        artifact_id = ref.get("artifact_id", "")
        stored = stored_by_id.get(artifact_id, {})
        current = current_by_id.get(artifact_id, {})
        source_path = source_root / import_public_lab_status.require_relative_path(ref.get("path", ""))
        comparison = {
            "artifact_id": artifact_id,
            "path": ref.get("path", ""),
            "source_path_exists": source_path.exists(),
            "expected_schema": ref.get("expected_schema", ""),
            "stored_schema": stored.get("observed_schema", ""),
            "current_schema": current.get("observed_schema", ""),
            "stored_status": stored.get("source_status", ""),
            "current_status": current.get("source_status", ""),
            "expected_status_class": ref.get("expected_status_class", ""),
            "stored_status_class": stored.get("observed_status_class", ""),
            "current_status_class": current.get("observed_status_class", ""),
            "stored_result": stored.get("status", ""),
            "current_result": current.get("status", ""),
            "schema_match": stored.get("observed_schema", "") == current.get("observed_schema", "") == ref.get("expected_schema", ""),
            "status_class_match": stored.get("observed_status_class", "") == current.get("observed_status_class", "") == ref.get("expected_status_class", ""),
            "source_status_match": stored.get("source_status", "") == current.get("source_status", ""),
            "result_match": stored.get("status", "") == current.get("status", "") == "passed",
            "summary_match": stored.get("summary", {}) == current.get("summary", {}),
        }
        comparison["drift_status"] = "drift_clear" if all(
            [
                comparison["source_path_exists"],
                comparison["schema_match"],
                comparison["status_class_match"],
                comparison["source_status_match"],
                comparison["result_match"],
                comparison["summary_match"],
            ]
        ) else "drift_detected"
        comparisons.append(comparison)
    return comparisons


def build_review(manifest_path: Path, report_path: Path, source_root: Path, repo_root: Path, now: str) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    report = load_json(report_path)
    manifest_result = validate_repo.validate_json_file(manifest_path)
    report_result = validate_repo.validate_json_file(report_path)
    current_report = import_public_lab_status.build_report(manifest, source_root, report.get("generated_at", now))
    artifact_comparisons = compare_artifacts(report, current_report, manifest, source_root)

    source_manifest = {
        "path": relative_output_path(manifest_path, repo_root),
        "schema": manifest.get("schema"),
        "intake_id": manifest.get("intake_id"),
        "artifact_count": len(manifest.get("artifact_refs", [])),
    }
    source_report = {
        "path": relative_output_path(report_path, repo_root),
        "schema": report.get("schema"),
        "intake_id": report.get("intake_id"),
        "overall_status": report.get("overall_status"),
        "generated_at": report.get("generated_at"),
    }
    source_access_policy = {
        "source_root_mode": "cli_supplied",
        "read_declared_public_artifacts": True,
        "copy_raw_artifact": False,
        "execute_source_validation": False,
        "read_private_evidence": False,
        "import_private_values": False,
    }
    authority = {
        "review_owner": "rusty.quest.sidecar_mesh",
        "source_truth_owner": "quest-termux-lab.public_artifacts",
        "handoff_acceptance_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/review_public_lab_artifact_drift.py --manifest fixtures/valid/public-lab-artifact-intake-manifest.synthetic.json --report fixtures/valid/public-lab-artifact-intake-report.synthetic.json --source-root ../quest-termux-lab --now 2026-06-04T21:43:00Z --output fixtures/valid/public-lab-artifact-drift-review.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
    }
    privacy_boundary = {
        "contains_endpoint_values": False,
        "contains_pairing_material": False,
        "contains_commands": False,
        "contains_raw_logs": False,
        "contains_visual_captures": False,
        "contains_private_device_ids": False,
        "public_fixture_policy": "synthetic_descriptor_only",
    }

    extraction_policy = manifest.get("extraction_policy", {})
    report_redaction = report.get("redaction", {})
    drifted = [row for row in artifact_comparisons if row["drift_status"] != "drift_clear"]
    expected_blocked = [row for row in artifact_comparisons if row["expected_status_class"] == "blocked"]
    checks = [
        check(
            "public_lab_drift.manifest_valid",
            manifest_result.ok
            and manifest.get("schema") == MANIFEST_SCHEMA
            and extraction_policy.get("copy_raw_artifact") is False
            and extraction_policy.get("execute_source_validation") is False
            and extraction_policy.get("contains_endpoint_values") is False,
            {
                "schema": manifest.get("schema"),
                "copy_raw_artifact": extraction_policy.get("copy_raw_artifact"),
                "execute_source_validation": extraction_policy.get("execute_source_validation"),
                "contains_endpoint_values": extraction_policy.get("contains_endpoint_values"),
            },
            {
                "schema": MANIFEST_SCHEMA,
                "copy_raw_artifact": False,
                "execute_source_validation": False,
                "contains_endpoint_values": False,
            },
            relative_output_path(manifest_path, repo_root),
        ),
        check(
            "public_lab_drift.report_valid",
            report_result.ok
            and report.get("schema") == REPORT_SCHEMA
            and report.get("overall_status") == "intake_ready"
            and report.get("manifold_handoff_role") == "proposal_evidence_only",
            {
                "schema": report.get("schema"),
                "overall_status": report.get("overall_status"),
                "manifold_handoff_role": report.get("manifold_handoff_role"),
            },
            {
                "schema": REPORT_SCHEMA,
                "overall_status": "intake_ready",
                "manifold_handoff_role": "proposal_evidence_only",
            },
            relative_output_path(report_path, repo_root),
        ),
        check(
            "public_lab_drift.artifacts_match_current_source",
            not drifted and len(artifact_comparisons) == len(manifest.get("artifact_refs", [])),
            {
                "artifact_count": len(artifact_comparisons),
                "drifted_artifacts": [row["artifact_id"] for row in drifted],
            },
            {
                "artifact_count": len(manifest.get("artifact_refs", [])),
                "drifted_artifacts": [],
            },
            "current source-derived sanitized report matches stored sidecar intake report",
        ),
        check(
            "public_lab_drift.expected_blocked_preserved",
            len(expected_blocked) >= 1 and all(row["current_status_class"] == "blocked" for row in expected_blocked),
            {
                "expected_blocked_count": len(expected_blocked),
                "blocked_status_classes": [row["current_status_class"] for row in expected_blocked],
            },
            {
                "expected_blocked_count": ">=1",
                "blocked_status_class": "blocked",
            },
            "expected blocked public-lab lanes remain blocked rather than falsely promoted",
        ),
        check(
            "public_lab_drift.source_access_policy",
            source_access_policy["read_declared_public_artifacts"] is True
            and source_access_policy["copy_raw_artifact"] is False
            and source_access_policy["execute_source_validation"] is False
            and source_access_policy["read_private_evidence"] is False
            and source_access_policy["import_private_values"] is False,
            source_access_policy,
            {
                "read_declared_public_artifacts": True,
                "copy_raw_artifact": False,
                "execute_source_validation": False,
                "read_private_evidence": False,
                "import_private_values": False,
            },
            "drift review reads declared public artifacts only and does not copy or execute source validation",
        ),
        check(
            "public_lab_drift.privacy_boundary",
            not any(
                privacy_boundary[key]
                for key in [
                    "contains_endpoint_values",
                    "contains_pairing_material",
                    "contains_commands",
                    "contains_raw_logs",
                    "contains_visual_captures",
                    "contains_private_device_ids",
                ]
            )
            and report_redaction.get("contains_endpoint_values") is False
            and report_redaction.get("contains_commands") is False
            and report_redaction.get("contains_pairing_material") is False
            and report_redaction.get("contains_raw_logs") is False,
            {
                "privacy_boundary": privacy_boundary,
                "report_redaction": report_redaction,
            },
            {
                "privacy_flags_all_false": True,
                "report_redaction_flags_false": True,
            },
            "drift review remains public-safe and redacted",
        ),
        check(
            "public_lab_drift.manifold_authority",
            authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["sidecar_role"] == "observer_proposer"
            and authority["proposal_status"] == "not_accepted",
            authority,
            {
                "handoff_acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "sidecar_role": "observer_proposer",
                "proposal_status": "not_accepted",
            },
            "public lab drift review remains advisory evidence for future Manifold handoff",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    manual_review_count = sum(1 for row in checks if row["status"] == "manual_review")
    return {
        "schema": REVIEW_SCHEMA,
        "review_id": "review.public_lab_artifact_drift.synthetic.001",
        "generated_at": now,
        "drift_status": "drift_clear" if fail_count == 0 and manual_review_count == 0 else "drift_detected",
        "source_manifest": source_manifest,
        "source_report": source_report,
        "source_access_policy": source_access_policy,
        "authority": authority,
        "artifact_comparisons": artifact_comparisons,
        "validation_evidence": validation_evidence,
        "privacy_boundary": privacy_boundary,
        "checks": checks,
        "summary": {
            "artifact_count": len(artifact_comparisons),
            "drifted_artifact_count": len(drifted),
            "expected_blocked_artifact_count": len(expected_blocked),
            "check_count": len(checks),
            "pass_count": len(checks) - fail_count,
            "manual_review_count": manual_review_count,
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "Public lab artifact drift review reads declared public-safe fixture reports only and does not copy raw artifacts, execute source validation, read private evidence, select endpoints, open sockets, use ADB, install apps, launch apps, or execute commands.",
            "The drift review is advisory proposal evidence only; Manifold remains the future owner of acceptance, rejection, revision, leases, and audit records.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "public_lab_drift_clear_before_manifold_handoff_or_contract_intake",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Public lab intake manifest.")
    parser.add_argument("--report", required=True, help="Stored public lab intake report.")
    parser.add_argument("--source-root", required=True, help="quest-termux-lab repository root.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output drift review path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        review = build_review(Path(args.manifest), Path(args.report), Path(args.source_root).resolve(), repo_root, args.now)
        write_json(Path(args.output), review)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"review_public_lab_artifact_drift failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": review["drift_status"], "check_count": review["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
