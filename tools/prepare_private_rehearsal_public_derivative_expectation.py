#!/usr/bin/env python3
"""Generate expectations for a future sanitized public derivative contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


EXPECTATION_SCHEMA = "rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1"
EVIDENCE_EXPECTATION_SCHEMA = "rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1"


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


def build_expectation(evidence_expectation_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    evidence_expectation = load_json(evidence_expectation_path)
    evidence_result = validate_repo.validate_json_file(evidence_expectation_path)

    source_private_rehearsal_evidence_expectation = {
        "path": relative_output_path(evidence_expectation_path, repo_root),
        "schema": evidence_expectation.get("schema"),
        "expectation_id": evidence_expectation.get("expectation_id"),
        "expectation_status": evidence_expectation.get("expectation_status"),
        "next_gate": evidence_expectation.get("next_gate"),
    }
    derivative_scope = {
        "expectation_class": "private_rehearsal_public_derivative_contract_expectation",
        "source_mode": "synthetic_fixture",
        "operator_approval_status": "not_recorded",
        "private_evidence_status": "not_collected",
        "public_derivative_status": "not_created",
        "derivative_schema_status": "not_created",
        "manifold_intake_status": "not_submitted",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
        "raw_artifact_status": "not_included",
        "endpoint_material_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "derivative_contract_owner": "rusty.quest.sidecar_mesh",
        "redaction_review_owner": "operator",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    expected_public_derivative = {
        "candidate_schema": "rusty.quest.sidecar.private_rehearsal_public_derivative.v1",
        "schema_status": "not_created",
        "artifact_status": "not_created",
        "source_private_evidence_policy": "operator_approved_private_store_only",
        "input_policy": "sanitized_summary_only",
        "allowed_message_class": "status_only",
        "allowed_payload_class": "low_rate_advisory_status",
        "public_fixture_policy": "synthetic_descriptor_only",
        "contains_private_values": False,
        "allowed_fields": [
            "derivative_id",
            "source_expectation_id",
            "approval_record_id",
            "rehearsal_id",
            "generated_at",
            "participant_count",
            "message_class",
            "route_health_summary",
            "sanitized_peer_status_summary",
            "stale_peer_count",
            "cleanup_status",
            "redaction_status",
            "rejected_input_classes",
            "privacy_boundary",
            "manifold_handoff_hint",
            "hostess_escalation_boundary",
            "validation_evidence",
            "summary",
        ],
        "prohibited_fields": [
            "endpoint_values",
            "commands",
            "adb",
            "pairing_material",
            "raw_logs",
            "visual_captures",
            "private_device_ids",
            "package_ids",
            "screenshots",
            "logcat",
            "shell_text",
        ],
        "required_redaction_results": [
            "endpoint_values_removed",
            "pairing_material_removed",
            "commands_absent",
            "adb_absent",
            "raw_logs_not_copied",
            "visual_captures_not_copied",
            "private_device_ids_removed",
        ],
        "accepted_summary_classes": [
            "aggregate_counts",
            "health_status",
            "stale_peer_count",
            "cleanup_result_summary",
            "rejection_terms",
        ],
        "rejects_direct_hostess_input": True,
        "rejects_manifold_accepted_state": True,
    }
    manifold_handoff_gate = {
        "target_repo": "rusty.manifold",
        "submission_status": "not_submitted",
        "requires_operator_approval": True,
        "requires_public_derivative_schema": True,
        "requires_redaction_review": True,
        "requires_validation_report": True,
        "acceptance_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_status": "not_created",
        "allowed_decisions": [
            "accepted_for_manifold_slice",
            "revision_requested",
            "rejected",
        ],
        "required_rejection_terms": [
            "operator_approval_missing",
            "public_derivative_schema_missing",
            "endpoint_values_rejected",
            "commands_rejected",
            "adb_rejected",
            "stale_peer_status",
            "untrusted_sidecar",
            "redaction_incomplete",
            "cleanup_incomplete",
        ],
    }
    hostess_escalation_boundary = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_private_rehearsal_public_derivative_expectation.py --evidence-expectation fixtures/valid/private-rehearsal-evidence-expectation.synthetic.json --now 2026-06-05T00:00:00Z --output fixtures/valid/private-rehearsal-public-derivative-expectation.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_accepts_only_sanitized_public_derivative",
        "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
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

    required_fields = {
        "derivative_id",
        "source_expectation_id",
        "approval_record_id",
        "rehearsal_id",
        "generated_at",
        "participant_count",
        "message_class",
        "route_health_summary",
        "sanitized_peer_status_summary",
        "stale_peer_count",
        "cleanup_status",
        "redaction_status",
        "rejected_input_classes",
        "privacy_boundary",
        "manifold_handoff_hint",
        "hostess_escalation_boundary",
        "validation_evidence",
        "summary",
    }
    prohibited_fields = {
        "endpoint_values",
        "commands",
        "adb",
        "pairing_material",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "package_ids",
        "screenshots",
        "logcat",
        "shell_text",
    }
    required_redactions = {
        "endpoint_values_removed",
        "pairing_material_removed",
        "commands_absent",
        "adb_absent",
        "raw_logs_not_copied",
        "visual_captures_not_copied",
        "private_device_ids_removed",
    }
    required_rejections = {
        "operator_approval_missing",
        "public_derivative_schema_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "cleanup_incomplete",
    }
    checks = [
        check(
            "private_rehearsal_public_derivative.source_evidence_expectation_ready",
            evidence_result.ok
            and evidence_expectation.get("schema") == EVIDENCE_EXPECTATION_SCHEMA
            and evidence_expectation.get("expectation_status") == "ready_for_operator_approved_private_evidence_plan"
            and evidence_expectation.get("next_gate") == "operator_decision_or_manifold_response_slice",
            {
                "schema": evidence_expectation.get("schema"),
                "expectation_status": evidence_expectation.get("expectation_status"),
                "next_gate": evidence_expectation.get("next_gate"),
            },
            {
                "schema": EVIDENCE_EXPECTATION_SCHEMA,
                "expectation_status": "ready_for_operator_approved_private_evidence_plan",
                "next_gate": "operator_decision_or_manifold_response_slice",
            },
            relative_output_path(evidence_expectation_path, repo_root),
        ),
        check(
            "private_rehearsal_public_derivative.no_derivative_or_intake_created",
            derivative_scope["operator_approval_status"] == "not_recorded"
            and derivative_scope["private_evidence_status"] == "not_collected"
            and derivative_scope["public_derivative_status"] == "not_created"
            and derivative_scope["derivative_schema_status"] == "not_created"
            and derivative_scope["manifold_intake_status"] == "not_submitted"
            and derivative_scope["hostess_route_status"] == "not_created"
            and derivative_scope["live_evidence_status"] == "not_included"
            and derivative_scope["endpoint_material_status"] == "not_included"
            and derivative_scope["adb_status"] == "not_used"
            and derivative_scope["command_status"] == "no_commands",
            derivative_scope,
            {
                "operator_approval_status": "not_recorded",
                "private_evidence_status": "not_collected",
                "public_derivative_status": "not_created",
                "derivative_schema_status": "not_created",
                "manifold_intake_status": "not_submitted",
                "hostess_route_status": "not_created",
                "live_evidence_status": "not_included",
                "endpoint_material_status": "not_included",
                "adb_status": "not_used",
                "command_status": "no_commands",
            },
            "public derivative expectation is contract-only and does not create derivative evidence or intake",
        ),
        check(
            "private_rehearsal_public_derivative.authority_split",
            authority["redaction_review_owner"] == "operator"
            and authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer"
            and authority["proposal_status"] == "not_accepted",
            authority,
            {
                "redaction_review_owner": "operator",
                "handoff_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
                "proposal_status": "not_accepted",
            },
            "operator owns redaction review; Manifold owns acceptance/state/audit; Hostess cannot consume sidecar-direct input",
        ),
        check(
            "private_rehearsal_public_derivative.sanitized_shape",
            expected_public_derivative["schema_status"] == "not_created"
            and expected_public_derivative["artifact_status"] == "not_created"
            and expected_public_derivative["source_private_evidence_policy"] == "operator_approved_private_store_only"
            and expected_public_derivative["input_policy"] == "sanitized_summary_only"
            and expected_public_derivative["allowed_message_class"] == "status_only"
            and expected_public_derivative["allowed_payload_class"] == "low_rate_advisory_status"
            and expected_public_derivative["public_fixture_policy"] == "synthetic_descriptor_only"
            and expected_public_derivative["contains_private_values"] is False
            and required_fields <= set(expected_public_derivative["allowed_fields"])
            and prohibited_fields <= set(expected_public_derivative["prohibited_fields"])
            and required_redactions <= set(expected_public_derivative["required_redaction_results"])
            and expected_public_derivative["rejects_direct_hostess_input"] is True
            and expected_public_derivative["rejects_manifold_accepted_state"] is True,
            expected_public_derivative,
            {
                "schema_status": "not_created",
                "artifact_status": "not_created",
                "source_private_evidence_policy": "operator_approved_private_store_only",
                "input_policy": "sanitized_summary_only",
                "allowed_message_class": "status_only",
                "allowed_payload_class": "low_rate_advisory_status",
                "public_fixture_policy": "synthetic_descriptor_only",
                "contains_private_values": False,
                "allowed_fields": sorted(required_fields),
                "prohibited_fields": sorted(prohibited_fields),
                "required_redaction_results": sorted(required_redactions),
                "rejects_direct_hostess_input": True,
                "rejects_manifold_accepted_state": True,
            },
            "future public derivative shape is sanitized summary-only and cannot act as accepted state or Hostess input",
        ),
        check(
            "private_rehearsal_public_derivative.manifold_handoff_gated",
            manifold_handoff_gate["submission_status"] == "not_submitted"
            and manifold_handoff_gate["requires_operator_approval"] is True
            and manifold_handoff_gate["requires_public_derivative_schema"] is True
            and manifold_handoff_gate["requires_redaction_review"] is True
            and manifold_handoff_gate["requires_validation_report"] is True
            and manifold_handoff_gate["acceptance_owner"] == "rusty.manifold"
            and manifold_handoff_gate["audit_owner"] == "rusty.manifold.audit"
            and manifold_handoff_gate["accepted_state_status"] == "not_created"
            and set(manifold_handoff_gate["allowed_decisions"]) == {
                "accepted_for_manifold_slice",
                "revision_requested",
                "rejected",
            }
            and required_rejections <= set(manifold_handoff_gate["required_rejection_terms"]),
            manifold_handoff_gate,
            {
                "submission_status": "not_submitted",
                "requires_operator_approval": True,
                "requires_public_derivative_schema": True,
                "requires_redaction_review": True,
                "requires_validation_report": True,
                "acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_status": "not_created",
                "allowed_decisions": ["accepted_for_manifold_slice", "revision_requested", "rejected"],
                "required_rejection_terms": sorted(required_rejections),
            },
            "Manifold intake remains gated behind operator approval, redaction review, derivative schema, and validation report",
        ),
        check(
            "private_rehearsal_public_derivative.hostess_deferred",
            hostess_escalation_boundary["status"] == "future_lane_not_requested"
            and hostess_escalation_boundary["route_status"] == "not_created"
            and hostess_escalation_boundary["recovery_request_status"] == "not_created"
            and hostess_escalation_boundary["device_action_authority"] == "not_in_sidecar"
            and hostess_escalation_boundary["input_role"] == "manifold_accepted_state_or_operator_request"
            and hostess_escalation_boundary["sidecar_direct_input_allowed"] is False
            and hostess_escalation_boundary["requires_manifold_accepted_state"] is True
            and hostess_escalation_boundary["requires_explicit_operator_request"] is True,
            hostess_escalation_boundary,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "recovery_request_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "input_role": "manifold_accepted_state_or_operator_request",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
            },
            "Hostess escalation remains deferred and requires Manifold state or explicit operator request",
        ),
        check(
            "private_rehearsal_public_derivative.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_accepts_only_sanitized_public_derivative"
            and validation_evidence["future_hostess_gate"] == "hostess_route_requires_manifold_state_or_operator_request"
            and not any(
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
            and privacy_boundary["public_fixture_policy"] == "synthetic_descriptor_only",
            {
                "validation_evidence": validation_evidence,
                "privacy_boundary": privacy_boundary,
            },
            {
                "local_validation_status": "expected_pass",
                "damaged_fixture_policy": "must_fail_validation",
                "future_manifold_gate": "manifold_accepts_only_sanitized_public_derivative",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "public derivative expectation remains descriptor-only and public-safe",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": EXPECTATION_SCHEMA,
        "expectation_id": "expectation.private_rehearsal_public_derivative.synthetic.001",
        "generated_at": now,
        "expectation_status": "ready_for_sanitized_public_derivative_contract" if fail_count == 0 else "blocked",
        "source_private_rehearsal_evidence_expectation": source_private_rehearsal_evidence_expectation,
        "derivative_scope": derivative_scope,
        "authority": authority,
        "expected_public_derivative": expected_public_derivative,
        "manifold_handoff_gate": manifold_handoff_gate,
        "hostess_escalation_boundary": hostess_escalation_boundary,
        "validation_evidence": validation_evidence,
        "privacy_boundary": privacy_boundary,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": sum(1 for row in checks if row["status"] == "pass"),
            "manual_review_count": sum(1 for row in checks if row["status"] == "manual_review"),
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "The private rehearsal public derivative expectation is descriptor evidence only; it does not record operator approval, collect private evidence, create a derivative artifact, submit to Manifold, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Future public derivatives may contain sanitized summaries only after operator approval, private evidence capture, cleanup, and redaction review.",
            "Manifold remains the future command/session/audit, handoff acceptance, and accepted-state authority for any sanitized public derivative.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; public derivative fixtures cannot directly drive Hostess device actions.",
        ],
        "next_gate": "operator_decision_or_manifold_public_derivative_schema_slice",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-expectation", required=True, help="Generated private rehearsal evidence expectation fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output public derivative expectation path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        expectation = build_expectation(Path(args.evidence_expectation), repo_root, args.now)
        write_json(Path(args.output), expectation)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_private_rehearsal_public_derivative_expectation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": expectation["expectation_status"], "check_count": expectation["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
