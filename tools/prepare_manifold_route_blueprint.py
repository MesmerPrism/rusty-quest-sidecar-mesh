#!/usr/bin/env python3
"""Generate a descriptor-only blueprint for a future Manifold route slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


BLUEPRINT_SCHEMA = "rusty.quest.sidecar.manifold_route_blueprint.v1"
CONTRACT_INTAKE_SCHEMA = "rusty.quest.sidecar.manifold_contract_intake_request.v1"
PRIVATE_APPROVAL_SCHEMA = "rusty.quest.sidecar.private_rehearsal_approval_request.v1"


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


def build_blueprint(contract_intake_request_path: Path, private_approval_request_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    contract_request = load_json(contract_intake_request_path)
    approval_request = load_json(private_approval_request_path)
    contract_result = validate_repo.validate_json_file(contract_intake_request_path)
    approval_result = validate_repo.validate_json_file(private_approval_request_path)

    source_contract_intake_request = {
        "path": relative_output_path(contract_intake_request_path, repo_root),
        "schema": contract_request.get("schema"),
        "request_id": contract_request.get("request_id"),
        "request_status": contract_request.get("request_status"),
        "next_gate": contract_request.get("next_gate"),
    }
    source_private_rehearsal_approval_request = {
        "path": relative_output_path(private_approval_request_path, repo_root),
        "schema": approval_request.get("schema"),
        "request_id": approval_request.get("request_id"),
        "request_status": approval_request.get("request_status"),
        "next_gate": approval_request.get("next_gate"),
    }
    blueprint_scope = {
        "blueprint_class": "manifold_owned_sidecar_peer_status_route_blueprint",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "implementation_status": "not_implemented",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "live_evidence_status": "not_included",
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
    }
    authority = {
        "blueprint_owner": "rusty.quest.sidecar_mesh",
        "route_implementation_owner": "rusty.manifold",
        "request_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "rollback_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    proposed_manifold_route = {
        "route_id": "route.sidecar_peer_status_intake.synthetic.001",
        "route_name": "sidecar_peer_status_intake",
        "route_status": "candidate",
        "route_creation_status": "not_created",
        "request_type": "submit_sidecar_peer_status_candidate",
        "input_payload_class": "low_rate_advisory_status",
        "output_event_class": "accept_reject_revision_audit",
        "requires_operator_approval_for_private_material": True,
        "requires_redaction_complete": True,
        "allows_endpoint_values": False,
        "allows_commands": False,
        "allows_adb": False,
        "allows_high_rate_payloads": False,
        "hostess_escalation_input": "manifold_accepted_state_or_operator_request",
        "required_validation_slots": [
            "slot.manifold_schema_contract_validation",
            "slot.sidecar_damaged_boundary_fixtures",
            "slot.manifold_accept_reject_audit_fixture",
            "slot.hostess_boundary_descriptor_check",
        ],
        "required_rejection_terms": [
            "operator_approval_missing",
            "endpoint_values_rejected",
            "commands_rejected",
            "adb_rejected",
            "stale_peer_status",
            "untrusted_sidecar",
            "redaction_incomplete",
            "high_rate_payload_rejected",
            "unsupported_transport",
            "hostess_route_rejected",
        ],
    }
    candidate_schemas = [
        {
            "schema_id": "rusty.manifold.sidecar_peer_status.request.v1",
            "schema_role": "request",
            "owner": "rusty.manifold",
            "status": "candidate_not_created",
            "required_fields": [
                "request_id",
                "source_sidecar_id",
                "observed_peer_id",
                "observed_at",
                "status_payload_class",
                "redaction",
                "operator_approval_ref",
            ],
        },
        {
            "schema_id": "rusty.manifold.sidecar_peer_status.decision.v1",
            "schema_role": "decision_event",
            "owner": "rusty.manifold",
            "status": "candidate_not_created",
            "required_fields": [
                "decision_id",
                "request_id",
                "decision",
                "rejection_terms",
                "revision",
                "audit_ref",
            ],
        },
        {
            "schema_id": "rusty.manifold.sidecar_peer_status.accepted_state.v1",
            "schema_role": "accepted_state",
            "owner": "rusty.manifold",
            "status": "candidate_not_created",
            "required_fields": [
                "state_id",
                "revision",
                "accepted_at",
                "source_request_id",
                "lease_ref",
                "audit_ref",
            ],
        },
    ]
    audit_contract = {
        "audit_surface": "sidecar_peer_rehearsal_audit",
        "audit_owner": "rusty.manifold.audit",
        "audit_record_status": "not_created",
        "required_audit_fields": [
            "request_id",
            "source_fixture_refs",
            "decision",
            "rejection_terms",
            "redaction_summary",
            "operator_approval_status",
            "hostess_boundary_status",
        ],
        "revision_policy": "manifold_owned_monotonic_revision",
        "rollback_policy": "manifold_owned_disable_route_or_reject_source",
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
            "python tools/prepare_manifold_route_blueprint.py --contract-intake-request fixtures/valid/manifold-contract-intake-request.synthetic.json --private-approval-request fixtures/valid/private-rehearsal-approval-request.synthetic.json --now 2026-06-04T23:04:00Z --output fixtures/valid/manifold-route-blueprint.synthetic.json",
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

    required_schema_roles = {"request", "decision_event", "accepted_state"}
    observed_schema_roles = {schema["schema_role"] for schema in candidate_schemas}
    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "high_rate_payload_rejected",
    }

    checks = [
        check(
            "route_blueprint.source_contract_intake_ready",
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
            "route_blueprint.source_private_approval_ready",
            approval_result.ok
            and approval_request.get("schema") == PRIVATE_APPROVAL_SCHEMA
            and approval_request.get("request_status") == "operator_approval_required"
            and approval_request.get("next_gate") == "operator_decision_or_manifold_repo_owned_contract_schema",
            {
                "schema": approval_request.get("schema"),
                "request_status": approval_request.get("request_status"),
                "next_gate": approval_request.get("next_gate"),
            },
            {
                "schema": PRIVATE_APPROVAL_SCHEMA,
                "request_status": "operator_approval_required",
                "next_gate": "operator_decision_or_manifold_repo_owned_contract_schema",
            },
            relative_output_path(private_approval_request_path, repo_root),
        ),
        check(
            "route_blueprint.no_repo_route_or_state",
            blueprint_scope["repo_touch_status"] == "not_touched"
            and blueprint_scope["route_status"] == "not_created"
            and blueprint_scope["accepted_state_status"] == "not_created"
            and blueprint_scope["live_evidence_status"] == "not_included"
            and proposed_manifold_route["route_creation_status"] == "not_created"
            and audit_contract["audit_record_status"] == "not_created",
            {
                "repo_touch_status": blueprint_scope["repo_touch_status"],
                "route_status": blueprint_scope["route_status"],
                "accepted_state_status": blueprint_scope["accepted_state_status"],
                "live_evidence_status": blueprint_scope["live_evidence_status"],
                "route_creation_status": proposed_manifold_route["route_creation_status"],
                "audit_record_status": audit_contract["audit_record_status"],
            },
            {
                "repo_touch_status": "not_touched",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "live_evidence_status": "not_included",
                "route_creation_status": "not_created",
                "audit_record_status": "not_created",
            },
            "blueprint does not touch Manifold or create route/state/audit records",
        ),
        check(
            "route_blueprint.manifold_authority",
            authority["route_implementation_owner"] == "rusty.manifold"
            and authority["request_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["sidecar_role"] == "observer_proposer",
            authority,
            {
                "route_implementation_owner": "rusty.manifold",
                "request_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "sidecar_role": "observer_proposer",
            },
            "Manifold remains route, request, runtime, session, accepted-state, and audit authority",
        ),
        check(
            "route_blueprint.route_constraints",
            proposed_manifold_route["route_status"] == "candidate"
            and proposed_manifold_route["input_payload_class"] == "low_rate_advisory_status"
            and proposed_manifold_route["requires_operator_approval_for_private_material"] is True
            and proposed_manifold_route["allows_endpoint_values"] is False
            and proposed_manifold_route["allows_commands"] is False
            and proposed_manifold_route["allows_adb"] is False
            and proposed_manifold_route["allows_high_rate_payloads"] is False
            and required_rejections <= set(proposed_manifold_route["required_rejection_terms"]),
            proposed_manifold_route,
            {
                "route_status": "candidate",
                "input_payload_class": "low_rate_advisory_status",
                "requires_operator_approval_for_private_material": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "required_rejection_terms": sorted(required_rejections),
            },
            "future Manifold route remains candidate-only and low-rate with rejection vocabulary",
        ),
        check(
            "route_blueprint.candidate_schemas_and_audit",
            required_schema_roles <= observed_schema_roles
            and all(schema["owner"] == "rusty.manifold" for schema in candidate_schemas)
            and all(schema["status"] == "candidate_not_created" for schema in candidate_schemas)
            and audit_contract["audit_owner"] == "rusty.manifold.audit"
            and audit_contract["audit_record_status"] == "not_created"
            and audit_contract["revision_policy"] == "manifold_owned_monotonic_revision",
            {
                "schema_roles": sorted(observed_schema_roles),
                "schema_owners": sorted({schema["owner"] for schema in candidate_schemas}),
                "schema_statuses": sorted({schema["status"] for schema in candidate_schemas}),
                "audit_owner": audit_contract["audit_owner"],
                "audit_record_status": audit_contract["audit_record_status"],
                "revision_policy": audit_contract["revision_policy"],
            },
            {
                "schema_roles": sorted(required_schema_roles),
                "schema_owner": "rusty.manifold",
                "schema_status": "candidate_not_created",
                "audit_owner": "rusty.manifold.audit",
                "audit_record_status": "not_created",
                "revision_policy": "manifold_owned_monotonic_revision",
            },
            "candidate schemas and audit contract are Manifold-owned and not created",
        ),
        check(
            "route_blueprint.hostess_boundary",
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
            "Hostess remains descriptor-only and receives no route or device-action authority",
        ),
        check(
            "route_blueprint.privacy_and_validation_boundary",
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
            "blueprint remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": BLUEPRINT_SCHEMA,
        "blueprint_id": "blueprint.manifold_route.synthetic.001",
        "generated_at": now,
        "blueprint_status": "ready_for_manifold_repo_design_review" if fail_count == 0 else "blocked",
        "source_contract_intake_request": source_contract_intake_request,
        "source_private_rehearsal_approval_request": source_private_rehearsal_approval_request,
        "blueprint_scope": blueprint_scope,
        "authority": authority,
        "proposed_manifold_route": proposed_manifold_route,
        "candidate_schemas": candidate_schemas,
        "audit_contract": audit_contract,
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
            "The Manifold route blueprint is descriptor evidence only; it does not touch the Manifold repo, create a Manifold route, create accepted Manifold state, touch Hostess, start a live Quest run, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future route implementation, request acceptance, command/session/audit, revision, lease, and accepted-state authority.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "manifold_repo_design_review_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract-intake-request", required=True, help="Generated Manifold contract intake request fixture.")
    parser.add_argument("--private-approval-request", required=True, help="Generated private rehearsal approval request fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output Manifold route blueprint path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        blueprint = build_blueprint(Path(args.contract_intake_request), Path(args.private_approval_request), repo_root, args.now)
        write_json(Path(args.output), blueprint)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_route_blueprint failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": blueprint["blueprint_status"], "check_count": blueprint["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
