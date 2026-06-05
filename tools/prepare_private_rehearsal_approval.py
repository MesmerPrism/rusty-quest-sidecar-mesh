#!/usr/bin/env python3
"""Generate a descriptor-only approval request for private peer rehearsal."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


REQUEST_SCHEMA = "rusty.quest.sidecar.private_rehearsal_approval_request.v1"
PEER_PLAN_SCHEMA = "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1"
CONTRACT_INTAKE_SCHEMA = "rusty.quest.sidecar.manifold_contract_intake_request.v1"


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


def build_request(peer_plan_path: Path, contract_intake_request_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    peer_plan = load_json(peer_plan_path)
    contract_request = load_json(contract_intake_request_path)
    peer_result = validate_repo.validate_json_file(peer_plan_path)
    contract_result = validate_repo.validate_json_file(contract_intake_request_path)

    source_peer_rehearsal_plan = {
        "path": relative_output_path(peer_plan_path, repo_root),
        "schema": peer_plan.get("schema"),
        "plan_id": peer_plan.get("plan_id"),
        "plan_status": peer_plan.get("plan_status"),
        "next_gate": peer_plan.get("next_gate"),
    }
    source_contract_intake_request = {
        "path": relative_output_path(contract_intake_request_path, repo_root),
        "schema": contract_request.get("schema"),
        "request_id": contract_request.get("request_id"),
        "request_status": contract_request.get("request_status"),
        "next_gate": contract_request.get("next_gate"),
    }
    approval_scope = {
        "request_class": "private_configured_peer_rehearsal_approval_descriptor",
        "source_mode": "synthetic_fixture",
        "operator_approval_status": "not_recorded",
        "route_status": "not_started",
        "implementation_status": "not_implemented",
        "live_evidence_status": "not_collected",
        "endpoint_material_status": "private_evidence_required_not_in_fixture",
        "adb_status": "not_used",
        "command_status": "no_commands",
        "hostess_route_status": "not_created",
        "manifold_route_status": "not_created",
        "accepted_state_status": "not_created",
    }
    authority = {
        "request_owner": "rusty.quest.sidecar_mesh",
        "approval_owner": "operator",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    requested_rehearsal = {
        "rehearsal_id": "rehearsal.private_configured_peer_status.synthetic.001",
        "status": "candidate",
        "peer_scope": "configured_status_peers",
        "source_mode": "synthetic_fixture",
        "message_class": "status_only",
        "allowed_payload_class": "low_rate_advisory_status",
        "operator_approval_required": True,
        "route_start_allowed": False,
        "requires_private_configured_material": True,
        "public_fixture_contains_endpoint_values": False,
        "adb_allowed": False,
        "commands_allowed": False,
        "remote_desktop_allowed": False,
        "file_transfer_allowed": False,
        "hostess_escalation_input": "manifold_accepted_state_or_operator_request",
    }
    operator_packet = {
        "packet_status": "draft",
        "approval_decision": "not_recorded",
        "approval_record_status": "not_created",
        "required_private_inputs": [
            "peer_identity_map",
            "operator_selected_transport",
            "endpoint_material_private_evidence",
            "rehearsal_duration_limit",
            "cleanup_plan",
        ],
        "required_public_derivatives": [
            "route_health_summary",
            "sanitized_peer_status_summary",
            "cleanup_result_summary",
        ],
        "rejection_terms": [
            "operator_approval_missing",
            "endpoint_values_rejected",
            "commands_rejected",
            "adb_rejected",
            "stale_peer_status",
            "untrusted_sidecar",
            "redaction_incomplete",
            "hostess_route_rejected",
        ],
    }
    hostess_boundary = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_private_rehearsal_approval.py --peer-plan fixtures/valid/configured-peer-rehearsal-plan.synthetic.json --contract-intake-request fixtures/valid/manifold-contract-intake-request.synthetic.json --now 2026-06-04T22:56:00Z --output fixtures/valid/private-rehearsal-approval-request.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_schema_route_acceptance_and_audit",
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

    private_inputs = set(operator_packet["required_private_inputs"])
    public_derivatives = set(operator_packet["required_public_derivatives"])
    rejection_terms = set(operator_packet["rejection_terms"])
    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
    }

    checks = [
        check(
            "approval_request.source_peer_plan_ready",
            peer_result.ok
            and peer_plan.get("schema") == PEER_PLAN_SCHEMA
            and peer_plan.get("plan_status") == "operator_approval_required"
            and peer_plan.get("next_gate") == "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract",
            {
                "schema": peer_plan.get("schema"),
                "plan_status": peer_plan.get("plan_status"),
                "next_gate": peer_plan.get("next_gate"),
            },
            {
                "schema": PEER_PLAN_SCHEMA,
                "plan_status": "operator_approval_required",
                "next_gate": "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract",
            },
            relative_output_path(peer_plan_path, repo_root),
        ),
        check(
            "approval_request.source_contract_intake_ready",
            contract_result.ok
            and contract_request.get("schema") == CONTRACT_INTAKE_SCHEMA
            and contract_request.get("request_status") == "ready_for_manifold_contract_intake"
            and contract_request.get("next_gate") == "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence",
            {
                "schema": contract_request.get("schema"),
                "request_status": contract_request.get("request_status"),
                "next_gate": contract_request.get("next_gate"),
            },
            {
                "schema": CONTRACT_INTAKE_SCHEMA,
                "request_status": "ready_for_manifold_contract_intake",
                "next_gate": "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence",
            },
            relative_output_path(contract_intake_request_path, repo_root),
        ),
        check(
            "approval_request.no_route_live_state_or_actions",
            approval_scope["route_status"] == "not_started"
            and approval_scope["live_evidence_status"] == "not_collected"
            and approval_scope["hostess_route_status"] == "not_created"
            and approval_scope["manifold_route_status"] == "not_created"
            and approval_scope["accepted_state_status"] == "not_created"
            and approval_scope["adb_status"] == "not_used"
            and approval_scope["command_status"] == "no_commands",
            approval_scope,
            {
                "route_status": "not_started",
                "live_evidence_status": "not_collected",
                "hostess_route_status": "not_created",
                "manifold_route_status": "not_created",
                "accepted_state_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
            },
            "approval request is a descriptor only and creates no route, state, ADB, or command action",
        ),
        check(
            "approval_request.manifold_hostess_authority_boundary",
            authority["approval_owner"] == "operator"
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
                "handoff_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
            },
            "operator approves private rehearsal material while Manifold and Hostess authority boundaries remain explicit",
        ),
        check(
            "approval_request.status_only_rehearsal",
            requested_rehearsal["status"] == "candidate"
            and requested_rehearsal["message_class"] == "status_only"
            and requested_rehearsal["allowed_payload_class"] == "low_rate_advisory_status"
            and requested_rehearsal["operator_approval_required"] is True
            and requested_rehearsal["route_start_allowed"] is False
            and requested_rehearsal["public_fixture_contains_endpoint_values"] is False
            and requested_rehearsal["adb_allowed"] is False
            and requested_rehearsal["commands_allowed"] is False
            and requested_rehearsal["remote_desktop_allowed"] is False
            and requested_rehearsal["file_transfer_allowed"] is False,
            requested_rehearsal,
            {
                "status": "candidate",
                "message_class": "status_only",
                "allowed_payload_class": "low_rate_advisory_status",
                "operator_approval_required": True,
                "route_start_allowed": False,
                "public_fixture_contains_endpoint_values": False,
                "adb_allowed": False,
                "commands_allowed": False,
                "remote_desktop_allowed": False,
                "file_transfer_allowed": False,
            },
            "future private rehearsal stays status-only until separately approved",
        ),
        check(
            "approval_request.operator_packet_draft",
            operator_packet["packet_status"] == "draft"
            and operator_packet["approval_decision"] == "not_recorded"
            and operator_packet["approval_record_status"] == "not_created"
            and {"peer_identity_map", "operator_selected_transport", "endpoint_material_private_evidence", "cleanup_plan"} <= private_inputs
            and {"route_health_summary", "sanitized_peer_status_summary", "cleanup_result_summary"} <= public_derivatives
            and required_rejections <= rejection_terms,
            operator_packet,
            {
                "packet_status": "draft",
                "approval_decision": "not_recorded",
                "approval_record_status": "not_created",
                "required_private_inputs": sorted(["peer_identity_map", "operator_selected_transport", "endpoint_material_private_evidence", "cleanup_plan"]),
                "required_public_derivatives": sorted(["route_health_summary", "sanitized_peer_status_summary", "cleanup_result_summary"]),
                "required_rejection_terms": sorted(required_rejections),
            },
            "approval packet records required private inputs and public derivatives without approving the run",
        ),
        check(
            "approval_request.hostess_boundary",
            hostess_boundary["status"] == "future_lane_not_requested"
            and hostess_boundary["route_status"] == "not_created"
            and hostess_boundary["recovery_request_status"] == "not_created"
            and hostess_boundary["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary["input_role"] == "manifold_accepted_state_or_operator_request",
            hostess_boundary,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "recovery_request_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "input_role": "manifold_accepted_state_or_operator_request",
            },
            "Hostess remains a future operator/recovery lane and receives no sidecar-created route",
        ),
        check(
            "approval_request.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_schema_route_acceptance_and_audit"
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
                "future_manifold_gate": "manifold_repo_owns_schema_route_acceptance_and_audit",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "approval request remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": REQUEST_SCHEMA,
        "request_id": "request.private_rehearsal_approval.synthetic.001",
        "generated_at": now,
        "request_status": "operator_approval_required" if fail_count == 0 else "blocked",
        "source_peer_rehearsal_plan": source_peer_rehearsal_plan,
        "source_contract_intake_request": source_contract_intake_request,
        "approval_scope": approval_scope,
        "authority": authority,
        "requested_rehearsal": requested_rehearsal,
        "operator_packet": operator_packet,
        "hostess_boundary": hostess_boundary,
        "validation_evidence": validation_evidence,
        "privacy_boundary": privacy_boundary,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": len(checks) - fail_count,
            "manual_review_count": 0,
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "Operator approval is required before any private configured peer rehearsal material can be used; this request does not approve or start the rehearsal.",
            "The private rehearsal approval request is descriptor evidence only; it does not touch Manifold, create accepted Manifold state, touch Hostess, start a live Quest run, use ADB, open sockets, select public endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future command/session/audit and accepted-state authority for sidecar peer status intake.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "operator_decision_or_manifold_repo_owned_contract_schema",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--peer-plan", required=True, help="Generated configured peer rehearsal plan fixture.")
    parser.add_argument("--contract-intake-request", required=True, help="Generated Manifold contract intake request fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output private rehearsal approval request path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        request = build_request(Path(args.peer_plan), Path(args.contract_intake_request), repo_root, args.now)
        write_json(Path(args.output), request)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_private_rehearsal_approval failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": request["request_status"], "check_count": request["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
