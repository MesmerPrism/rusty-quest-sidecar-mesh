#!/usr/bin/env python3
"""Generate expectations for future operator-approved private peer rehearsal evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


EXPECTATION_SCHEMA = "rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1"
APPROVAL_SCHEMA = "rusty.quest.sidecar.private_rehearsal_approval_request.v1"
HOSTESS_EXPECTATION_SCHEMA = "rusty.quest.sidecar.hostess_boundary_descriptor_expectation.v1"


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


def build_expectation(approval_request_path: Path, hostess_expectation_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    approval_request = load_json(approval_request_path)
    hostess_expectation = load_json(hostess_expectation_path)
    approval_result = validate_repo.validate_json_file(approval_request_path)
    hostess_result = validate_repo.validate_json_file(hostess_expectation_path)

    source_private_rehearsal_approval_request = {
        "path": relative_output_path(approval_request_path, repo_root),
        "schema": approval_request.get("schema"),
        "request_id": approval_request.get("request_id"),
        "request_status": approval_request.get("request_status"),
        "next_gate": approval_request.get("next_gate"),
    }
    source_hostess_boundary_descriptor_expectation = {
        "path": relative_output_path(hostess_expectation_path, repo_root),
        "schema": hostess_expectation.get("schema"),
        "expectation_id": hostess_expectation.get("expectation_id"),
        "expectation_status": hostess_expectation.get("expectation_status"),
        "next_gate": hostess_expectation.get("next_gate"),
    }
    evidence_scope = {
        "expectation_class": "private_configured_peer_rehearsal_evidence_expectation",
        "source_mode": "synthetic_fixture",
        "operator_approval_status": "not_recorded",
        "rehearsal_route_status": "not_started",
        "private_evidence_status": "not_collected",
        "public_derivative_status": "not_created",
        "manifold_intake_status": "not_submitted",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
        "endpoint_material_status": "private_only_after_operator_approval",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "approval_owner": "operator",
        "private_evidence_capture_owner": "operator",
        "public_derivative_owner": "rusty.quest.sidecar_mesh",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    private_evidence_requirements = {
        "status": "not_collected",
        "private_store_required": True,
        "public_fixture_may_include_private_values": False,
        "operator_approval_required": True,
        "duration_limit_required": True,
        "cleanup_required": True,
        "route_start_allowed_by_this_fixture": False,
        "allowed_transport_profile": "configured_status_only",
        "allowed_message_class": "status_only",
        "allowed_payload_class": "low_rate_advisory_status",
        "required_private_artifacts": [
            "peer_identity_map",
            "selected_transport_descriptor",
            "endpoint_material_private_evidence",
            "private_route_health_trace",
            "cleanup_result",
            "redaction_review_input",
        ],
        "disallowed_private_actions": [
            "commands",
            "adb",
            "install",
            "launch",
            "recovery",
            "remote_desktop_control",
            "file_transfer",
            "high_rate_payloads",
        ],
    }
    public_derivative_requirements = {
        "status": "not_created",
        "candidate_schema": "rusty.quest.sidecar.private_rehearsal_public_derivative.v1",
        "candidate_schema_status": "not_created",
        "contains_private_values": False,
        "required_fields": [
            "rehearsal_id",
            "approval_record_id",
            "participant_count",
            "message_class",
            "route_health_summary",
            "sanitized_peer_status_summary",
            "stale_peer_count",
            "redaction_status",
            "cleanup_status",
            "rejected_input_classes",
            "privacy_boundary",
        ],
        "prohibited_public_fields": [
            "endpoint_values",
            "commands",
            "adb",
            "pairing_material",
            "raw_logs",
            "visual_captures",
            "private_device_ids",
            "package_ids",
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
        "public_fixture_policy": "synthetic_descriptor_only",
    }
    manifold_handoff_expectation = {
        "target_repo": "rusty.manifold",
        "submission_status": "not_submitted",
        "requires_operator_approval": True,
        "requires_public_derivative": True,
        "requires_redaction_review": True,
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
            "python tools/prepare_private_rehearsal_evidence_expectation.py --approval-request fixtures/valid/private-rehearsal-approval-request.synthetic.json --hostess-expectation fixtures/valid/hostess-boundary-descriptor-expectation.synthetic.json --now 2026-06-04T23:52:00Z --output fixtures/valid/private-rehearsal-evidence-expectation.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_accepts_sanitized_derivative_after_operator_approval",
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

    required_private_artifacts = {
        "peer_identity_map",
        "selected_transport_descriptor",
        "endpoint_material_private_evidence",
        "private_route_health_trace",
        "cleanup_result",
        "redaction_review_input",
    }
    required_public_fields = {
        "rehearsal_id",
        "approval_record_id",
        "participant_count",
        "message_class",
        "route_health_summary",
        "sanitized_peer_status_summary",
        "stale_peer_count",
        "redaction_status",
        "cleanup_status",
        "rejected_input_classes",
        "privacy_boundary",
    }
    prohibited_public_fields = {
        "endpoint_values",
        "commands",
        "adb",
        "pairing_material",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "package_ids",
    }
    required_rejections = {
        "operator_approval_missing",
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
            "private_rehearsal_evidence.source_approval_request_ready",
            approval_result.ok
            and approval_request.get("schema") == APPROVAL_SCHEMA
            and approval_request.get("request_status") == "operator_approval_required"
            and approval_request.get("next_gate") == "operator_decision_or_manifold_repo_owned_contract_schema",
            {
                "schema": approval_request.get("schema"),
                "request_status": approval_request.get("request_status"),
                "next_gate": approval_request.get("next_gate"),
            },
            {
                "schema": APPROVAL_SCHEMA,
                "request_status": "operator_approval_required",
                "next_gate": "operator_decision_or_manifold_repo_owned_contract_schema",
            },
            relative_output_path(approval_request_path, repo_root),
        ),
        check(
            "private_rehearsal_evidence.source_hostess_expectation_ready",
            hostess_result.ok
            and hostess_expectation.get("schema") == HOSTESS_EXPECTATION_SCHEMA
            and hostess_expectation.get("expectation_status") == "ready_for_future_hostess_boundary_descriptor"
            and hostess_expectation.get("next_gate") == "manifold_response_slice_or_operator_decision",
            {
                "schema": hostess_expectation.get("schema"),
                "expectation_status": hostess_expectation.get("expectation_status"),
                "next_gate": hostess_expectation.get("next_gate"),
            },
            {
                "schema": HOSTESS_EXPECTATION_SCHEMA,
                "expectation_status": "ready_for_future_hostess_boundary_descriptor",
                "next_gate": "manifold_response_slice_or_operator_decision",
            },
            relative_output_path(hostess_expectation_path, repo_root),
        ),
        check(
            "private_rehearsal_evidence.no_route_evidence_or_submission",
            evidence_scope["operator_approval_status"] == "not_recorded"
            and evidence_scope["rehearsal_route_status"] == "not_started"
            and evidence_scope["private_evidence_status"] == "not_collected"
            and evidence_scope["public_derivative_status"] == "not_created"
            and evidence_scope["manifold_intake_status"] == "not_submitted"
            and evidence_scope["hostess_route_status"] == "not_created"
            and evidence_scope["live_evidence_status"] == "not_included"
            and evidence_scope["adb_status"] == "not_used"
            and evidence_scope["command_status"] == "no_commands",
            evidence_scope,
            {
                "operator_approval_status": "not_recorded",
                "rehearsal_route_status": "not_started",
                "private_evidence_status": "not_collected",
                "public_derivative_status": "not_created",
                "manifold_intake_status": "not_submitted",
                "hostess_route_status": "not_created",
                "live_evidence_status": "not_included",
                "adb_status": "not_used",
                "command_status": "no_commands",
            },
            "evidence expectation does not approve, start, collect, submit, or create routes",
        ),
        check(
            "private_rehearsal_evidence.authority_split",
            authority["approval_owner"] == "operator"
            and authority["private_evidence_capture_owner"] == "operator"
            and authority["public_derivative_owner"] == "rusty.quest.sidecar_mesh"
            and authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer",
            authority,
            {
                "approval_owner": "operator",
                "private_evidence_capture_owner": "operator",
                "public_derivative_owner": "rusty.quest.sidecar_mesh",
                "handoff_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
            },
            "operator owns private capture, sidecar may propose sanitized derivatives, and Manifold owns acceptance/audit",
        ),
        check(
            "private_rehearsal_evidence.private_requirements_status_only",
            private_evidence_requirements["status"] == "not_collected"
            and private_evidence_requirements["private_store_required"] is True
            and private_evidence_requirements["public_fixture_may_include_private_values"] is False
            and private_evidence_requirements["operator_approval_required"] is True
            and private_evidence_requirements["duration_limit_required"] is True
            and private_evidence_requirements["cleanup_required"] is True
            and private_evidence_requirements["route_start_allowed_by_this_fixture"] is False
            and private_evidence_requirements["allowed_transport_profile"] == "configured_status_only"
            and private_evidence_requirements["allowed_message_class"] == "status_only"
            and private_evidence_requirements["allowed_payload_class"] == "low_rate_advisory_status"
            and required_private_artifacts <= set(private_evidence_requirements["required_private_artifacts"]),
            private_evidence_requirements,
            {
                "status": "not_collected",
                "private_store_required": True,
                "public_fixture_may_include_private_values": False,
                "operator_approval_required": True,
                "duration_limit_required": True,
                "cleanup_required": True,
                "route_start_allowed_by_this_fixture": False,
                "allowed_transport_profile": "configured_status_only",
                "allowed_message_class": "status_only",
                "allowed_payload_class": "low_rate_advisory_status",
                "required_private_artifacts": sorted(required_private_artifacts),
            },
            "future private evidence remains approval-gated, private, duration-limited, cleanup-bound, and status-only",
        ),
        check(
            "private_rehearsal_evidence.public_derivative_redaction",
            public_derivative_requirements["status"] == "not_created"
            and public_derivative_requirements["candidate_schema_status"] == "not_created"
            and public_derivative_requirements["contains_private_values"] is False
            and required_public_fields <= set(public_derivative_requirements["required_fields"])
            and prohibited_public_fields <= set(public_derivative_requirements["prohibited_public_fields"])
            and {
                "endpoint_values_removed",
                "pairing_material_removed",
                "commands_absent",
                "adb_absent",
                "raw_logs_not_copied",
                "visual_captures_not_copied",
                "private_device_ids_removed",
            }
            <= set(public_derivative_requirements["required_redaction_results"])
            and public_derivative_requirements["public_fixture_policy"] == "synthetic_descriptor_only",
            public_derivative_requirements,
            {
                "status": "not_created",
                "candidate_schema_status": "not_created",
                "contains_private_values": False,
                "required_fields": sorted(required_public_fields),
                "prohibited_public_fields": sorted(prohibited_public_fields),
                "required_redaction_results": [
                    "adb_absent",
                    "commands_absent",
                    "endpoint_values_removed",
                    "pairing_material_removed",
                    "private_device_ids_removed",
                    "raw_logs_not_copied",
                    "visual_captures_not_copied",
                ],
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "future public derivative must be redacted and schema-bound before Manifold handoff",
        ),
        check(
            "private_rehearsal_evidence.manifold_handoff_gated",
            manifold_handoff_expectation["submission_status"] == "not_submitted"
            and manifold_handoff_expectation["requires_operator_approval"] is True
            and manifold_handoff_expectation["requires_public_derivative"] is True
            and manifold_handoff_expectation["requires_redaction_review"] is True
            and manifold_handoff_expectation["acceptance_owner"] == "rusty.manifold"
            and manifold_handoff_expectation["audit_owner"] == "rusty.manifold.audit"
            and manifold_handoff_expectation["accepted_state_status"] == "not_created"
            and set(manifold_handoff_expectation["allowed_decisions"]) == {
                "accepted_for_manifold_slice",
                "revision_requested",
                "rejected",
            }
            and required_rejections <= set(manifold_handoff_expectation["required_rejection_terms"]),
            manifold_handoff_expectation,
            {
                "submission_status": "not_submitted",
                "requires_operator_approval": True,
                "requires_public_derivative": True,
                "requires_redaction_review": True,
                "acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_status": "not_created",
                "allowed_decisions": ["accepted_for_manifold_slice", "revision_requested", "rejected"],
                "required_rejection_terms": sorted(required_rejections),
            },
            "Manifold intake remains gated behind operator approval, redaction review, and sanitized derivative creation",
        ),
        check(
            "private_rehearsal_evidence.hostess_escalation_deferred",
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
            "Hostess escalation remains deferred and cannot consume sidecar-direct evidence",
        ),
        check(
            "private_rehearsal_evidence.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_accepts_sanitized_derivative_after_operator_approval"
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
                "future_manifold_gate": "manifold_accepts_sanitized_derivative_after_operator_approval",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "private evidence expectation remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": EXPECTATION_SCHEMA,
        "expectation_id": "expectation.private_rehearsal_evidence.synthetic.001",
        "generated_at": now,
        "expectation_status": "ready_for_operator_approved_private_evidence_plan" if fail_count == 0 else "blocked",
        "source_private_rehearsal_approval_request": source_private_rehearsal_approval_request,
        "source_hostess_boundary_descriptor_expectation": source_hostess_boundary_descriptor_expectation,
        "evidence_scope": evidence_scope,
        "authority": authority,
        "private_evidence_requirements": private_evidence_requirements,
        "public_derivative_requirements": public_derivative_requirements,
        "manifold_handoff_expectation": manifold_handoff_expectation,
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
            "The private rehearsal evidence expectation is descriptor evidence only; it does not record operator approval, start peer routes, collect private evidence, create public derivatives, submit to Manifold, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Operator approval is required before private configured peer rehearsal evidence can be collected; public fixtures may contain only sanitized derivatives after redaction review.",
            "Manifold remains the future command/session/audit, handoff acceptance, and accepted-state authority for any sanitized peer rehearsal derivative.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar evidence cannot directly drive Hostess device actions.",
        ],
        "next_gate": "operator_decision_or_manifold_response_slice",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--approval-request", required=True, help="Generated private rehearsal approval request fixture.")
    parser.add_argument("--hostess-expectation", required=True, help="Generated Hostess boundary descriptor expectation fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output private rehearsal evidence expectation path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        expectation = build_expectation(Path(args.approval_request), Path(args.hostess_expectation), repo_root, args.now)
        write_json(Path(args.output), expectation)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_private_rehearsal_evidence_expectation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": expectation["expectation_status"], "check_count": expectation["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
