#!/usr/bin/env python3
"""Generate a descriptor-only request for a future Manifold public derivative schema slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


REQUEST_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_request.v1"
PUBLIC_DERIVATIVE_EXPECTATION_SCHEMA = "rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1"


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


def build_request(public_derivative_expectation_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    public_derivative_expectation = load_json(public_derivative_expectation_path)
    source_result = validate_repo.validate_json_file(public_derivative_expectation_path)

    source_public_derivative_expectation = {
        "path": relative_output_path(public_derivative_expectation_path, repo_root),
        "schema": public_derivative_expectation.get("schema"),
        "expectation_id": public_derivative_expectation.get("expectation_id"),
        "expectation_status": public_derivative_expectation.get("expectation_status"),
        "next_gate": public_derivative_expectation.get("next_gate"),
    }
    request_scope = {
        "request_class": "manifold_owned_public_derivative_schema_request",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "schema_status": "not_created",
        "route_handler_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "public_derivative_status": "not_created",
        "private_evidence_status": "not_collected",
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
        "endpoint_material_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    authority = {
        "request_owner": "rusty.quest.sidecar_mesh",
        "schema_owner": "rusty.manifold",
        "route_owner": "rusty.manifold",
        "review_owner": "rusty.manifold",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "redaction_review_owner": "operator",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    proposed_manifold_schema = {
        "candidate_schema_id": "rusty.manifold.sidecar_peer_status_public_derivative.v1",
        "schema_status": "not_created",
        "schema_owner": "rusty.manifold",
        "source_contract": "rusty.quest.sidecar.private_rehearsal_public_derivative.v1",
        "source_contract_status": "not_created",
        "input_policy": "sanitized_summary_only",
        "allowed_payload_class": "low_rate_advisory_status",
        "allowed_message_class": "status_only",
        "public_fixture_policy": "synthetic_descriptor_only",
        "accepted_state_mapping_status": "not_created",
        "audit_fixture_status": "not_created",
        "required_fields": [
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
        "contains_private_values": False,
        "creates_accepted_state": False,
        "creates_hostess_input": False,
    }
    proposed_manifold_route = {
        "route_id": "route.sidecar_peer_status_public_derivative_intake",
        "route_status": "not_created",
        "route_owner": "rusty.manifold",
        "input_schema": "rusty.manifold.sidecar_peer_status_public_derivative.v1",
        "input_schema_status": "not_created",
        "decision_event_status": "not_created",
        "audit_record_status": "not_created",
        "accepted_state_status": "not_created",
        "allowed_decisions": [
            "accepted_for_manifold_slice",
            "revision_requested",
            "rejected",
        ],
        "forbidden_route_inputs": [
            "endpoint_values",
            "commands",
            "adb",
            "pairing_material",
            "raw_logs",
            "visual_captures",
            "private_device_ids",
            "hostess_direct_action",
        ],
    }
    manifold_review_gate = {
        "target_repo": "rusty.manifold",
        "review_status": "not_submitted",
        "requires_schema_review": True,
        "requires_route_review": True,
        "requires_redaction_review": True,
        "requires_validation_report": True,
        "requires_operator_approval": True,
        "acceptance_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_status": "not_created",
        "allowed_outcomes": [
            "accepted_for_manifold_slice",
            "revision_requested",
            "rejected",
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
            "python tools/prepare_manifold_public_derivative_schema_request.py --public-derivative-expectation fixtures/valid/private-rehearsal-public-derivative-expectation.synthetic.json --now 2026-06-05T00:08:00Z --output fixtures/valid/manifold-public-derivative-schema-request.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_public_derivative_schema_route_and_audit",
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

    required_schema_fields = set(proposed_manifold_schema["required_fields"])
    prohibited_fields = set(proposed_manifold_schema["prohibited_fields"])
    required_rejections = set(proposed_manifold_schema["required_rejection_terms"])
    checks = [
        check(
            "manifold_public_derivative_schema_request.source_expectation_ready",
            source_result.ok
            and public_derivative_expectation.get("schema") == PUBLIC_DERIVATIVE_EXPECTATION_SCHEMA
            and public_derivative_expectation.get("expectation_status") == "ready_for_sanitized_public_derivative_contract"
            and public_derivative_expectation.get("next_gate") == "operator_decision_or_manifold_public_derivative_schema_slice",
            {
                "schema": public_derivative_expectation.get("schema"),
                "expectation_status": public_derivative_expectation.get("expectation_status"),
                "next_gate": public_derivative_expectation.get("next_gate"),
            },
            {
                "schema": PUBLIC_DERIVATIVE_EXPECTATION_SCHEMA,
                "expectation_status": "ready_for_sanitized_public_derivative_contract",
                "next_gate": "operator_decision_or_manifold_public_derivative_schema_slice",
            },
            relative_output_path(public_derivative_expectation_path, repo_root),
        ),
        check(
            "manifold_public_derivative_schema_request.no_repo_or_runtime_mutation",
            request_scope["repo_touch_status"] == "not_touched"
            and request_scope["branch_status"] == "not_created"
            and request_scope["schema_status"] == "not_created"
            and request_scope["route_handler_status"] == "not_created"
            and request_scope["accepted_state_status"] == "not_created"
            and request_scope["audit_record_status"] == "not_created"
            and request_scope["public_derivative_status"] == "not_created"
            and request_scope["private_evidence_status"] == "not_collected"
            and request_scope["hostess_route_status"] == "not_created"
            and request_scope["adb_status"] == "not_used"
            and request_scope["command_status"] == "no_commands",
            request_scope,
            {
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "schema_status": "not_created",
                "route_handler_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "public_derivative_status": "not_created",
                "private_evidence_status": "not_collected",
                "hostess_route_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
            },
            "request is descriptor-only and does not mutate Manifold, Hostess, or runtime state",
        ),
        check(
            "manifold_public_derivative_schema_request.authority_split",
            authority["schema_owner"] == "rusty.manifold"
            and authority["route_owner"] == "rusty.manifold"
            and authority["review_owner"] == "rusty.manifold"
            and authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["redaction_review_owner"] == "operator"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer",
            authority,
            {
                "schema_owner": "rusty.manifold",
                "route_owner": "rusty.manifold",
                "review_owner": "rusty.manifold",
                "handoff_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "redaction_review_owner": "operator",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
            },
            "Manifold owns future schema/route/review/acceptance/state/audit; sidecar remains observer/proposer",
        ),
        check(
            "manifold_public_derivative_schema_request.schema_contract",
            proposed_manifold_schema["schema_status"] == "not_created"
            and proposed_manifold_schema["schema_owner"] == "rusty.manifold"
            and proposed_manifold_schema["source_contract_status"] == "not_created"
            and proposed_manifold_schema["input_policy"] == "sanitized_summary_only"
            and proposed_manifold_schema["allowed_payload_class"] == "low_rate_advisory_status"
            and proposed_manifold_schema["allowed_message_class"] == "status_only"
            and proposed_manifold_schema["public_fixture_policy"] == "synthetic_descriptor_only"
            and proposed_manifold_schema["accepted_state_mapping_status"] == "not_created"
            and proposed_manifold_schema["audit_fixture_status"] == "not_created"
            and required_schema_fields <= set(proposed_manifold_schema["required_fields"])
            and prohibited_fields <= set(proposed_manifold_schema["prohibited_fields"])
            and required_rejections <= set(proposed_manifold_schema["required_rejection_terms"])
            and proposed_manifold_schema["contains_private_values"] is False
            and proposed_manifold_schema["creates_accepted_state"] is False
            and proposed_manifold_schema["creates_hostess_input"] is False,
            proposed_manifold_schema,
            {
                "schema_status": "not_created",
                "schema_owner": "rusty.manifold",
                "input_policy": "sanitized_summary_only",
                "allowed_payload_class": "low_rate_advisory_status",
                "allowed_message_class": "status_only",
                "public_fixture_policy": "synthetic_descriptor_only",
                "required_fields": sorted(required_schema_fields),
                "prohibited_fields": sorted(prohibited_fields),
                "required_rejection_terms": sorted(required_rejections),
                "contains_private_values": False,
                "creates_accepted_state": False,
                "creates_hostess_input": False,
            },
            "future Manifold schema is sanitized summary-only and not accepted state or Hostess input",
        ),
        check(
            "manifold_public_derivative_schema_request.route_contract",
            proposed_manifold_route["route_status"] == "not_created"
            and proposed_manifold_route["route_owner"] == "rusty.manifold"
            and proposed_manifold_route["input_schema_status"] == "not_created"
            and proposed_manifold_route["decision_event_status"] == "not_created"
            and proposed_manifold_route["audit_record_status"] == "not_created"
            and proposed_manifold_route["accepted_state_status"] == "not_created"
            and set(proposed_manifold_route["allowed_decisions"]) == {
                "accepted_for_manifold_slice",
                "revision_requested",
                "rejected",
            }
            and {
                "endpoint_values",
                "commands",
                "adb",
                "pairing_material",
                "raw_logs",
                "visual_captures",
                "private_device_ids",
                "hostess_direct_action",
            }
            <= set(proposed_manifold_route["forbidden_route_inputs"]),
            proposed_manifold_route,
            {
                "route_status": "not_created",
                "route_owner": "rusty.manifold",
                "input_schema_status": "not_created",
                "decision_event_status": "not_created",
                "audit_record_status": "not_created",
                "accepted_state_status": "not_created",
                "allowed_decisions": ["accepted_for_manifold_slice", "revision_requested", "rejected"],
                "forbidden_route_inputs_present": True,
            },
            "future Manifold route is not created and rejects private/action inputs",
        ),
        check(
            "manifold_public_derivative_schema_request.review_gate",
            manifold_review_gate["review_status"] == "not_submitted"
            and manifold_review_gate["requires_schema_review"] is True
            and manifold_review_gate["requires_route_review"] is True
            and manifold_review_gate["requires_redaction_review"] is True
            and manifold_review_gate["requires_validation_report"] is True
            and manifold_review_gate["requires_operator_approval"] is True
            and manifold_review_gate["acceptance_owner"] == "rusty.manifold"
            and manifold_review_gate["audit_owner"] == "rusty.manifold.audit"
            and manifold_review_gate["accepted_state_status"] == "not_created",
            manifold_review_gate,
            {
                "review_status": "not_submitted",
                "requires_schema_review": True,
                "requires_route_review": True,
                "requires_redaction_review": True,
                "requires_validation_report": True,
                "requires_operator_approval": True,
                "acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_status": "not_created",
            },
            "Manifold review remains future and requires schema, route, redaction, validation, and operator gates",
        ),
        check(
            "manifold_public_derivative_schema_request.hostess_deferred",
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
                "device_action_authority": "not_in_sidecar",
                "input_role": "manifold_accepted_state_or_operator_request",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
            },
            "Hostess remains deferred behind Manifold accepted state or explicit operator request",
        ),
        check(
            "manifold_public_derivative_schema_request.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_public_derivative_schema_route_and_audit"
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
                "future_manifold_gate": "manifold_repo_owns_public_derivative_schema_route_and_audit",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "schema request remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": REQUEST_SCHEMA,
        "request_id": "request.manifold_public_derivative_schema.synthetic.001",
        "generated_at": now,
        "request_status": "ready_for_manifold_public_derivative_schema_review" if fail_count == 0 else "blocked",
        "source_public_derivative_expectation": source_public_derivative_expectation,
        "request_scope": request_scope,
        "authority": authority,
        "proposed_manifold_schema": proposed_manifold_schema,
        "proposed_manifold_route": proposed_manifold_route,
        "manifold_review_gate": manifold_review_gate,
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
            "The Manifold public derivative schema request is descriptor evidence only; it does not touch the Manifold repo, create a branch, create a schema, create a route, create accepted state, submit evidence, touch Hostess, start live Quest work, use ADB, select endpoints, install, launch, recover, copy files, or execute commands.",
            "The sidecar may request future review, but Manifold remains the command/session/audit, schema, route, handoff acceptance, and accepted-state authority.",
            "Operator approval and redaction review remain required before any real public derivative can be submitted.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar request fixtures cannot directly drive Hostess device actions.",
        ],
        "next_gate": "manifold_repo_public_derivative_schema_review_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-derivative-expectation", required=True, help="Generated public derivative expectation fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output Manifold public derivative schema request path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        request = build_request(Path(args.public_derivative_expectation), repo_root, args.now)
        write_json(Path(args.output), request)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_public_derivative_schema_request failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": request["request_status"], "check_count": request["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
