#!/usr/bin/env python3
"""Generate a descriptor-only Manifold adapter contract review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


REVIEW_SCHEMA = "rusty.quest.sidecar.manifold_adapter_contract_review.v1"
PEER_PLAN_SCHEMA = "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1"


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


def build_review(peer_plan_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    peer_plan = load_json(peer_plan_path)
    peer_plan_result = validate_repo.validate_json_file(peer_plan_path)

    integration_status = {
        "manifold_repo_touched": False,
        "hostess_repo_touched": False,
        "live_device_used": False,
        "runtime_route_created": False,
        "accepted_manifold_state_created": False,
        "hostess_route_created": False,
    }
    contract_scope = {
        "contract_class": "manifold_adapter_contract_review",
        "source_mode": "synthetic_fixture",
        "implementation_status": "not_implemented",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "payload_rate_class": "low_rate",
        "payload_authority": "advisory_only",
    }
    authority = {
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "sidecar_role": "observer_proposer",
        "operator_role": "approval_gate_for_private_evidence",
        "hostess_role": "future_operator_recovery_after_manifold_acceptance",
        "proposal_status": "not_accepted",
    }
    proposed_manifold_contract = {
        "contract_id": "contract.sidecar_peer_status_adapter.synthetic.001",
        "status": "candidate",
        "source_schema": PEER_PLAN_SCHEMA,
        "source_path": relative_output_path(peer_plan_path, repo_root),
        "surfaces": [
            {
                "surface_id": "surface.sidecar_peer_status_source.synthetic",
                "kind": "source_descriptor",
                "rate_class": "low_rate",
                "acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_status": "not_created",
            },
            {
                "surface_id": "surface.sidecar_peer_status_intake.synthetic",
                "kind": "intake_descriptor",
                "rate_class": "low_rate",
                "acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_status": "not_created",
            },
            {
                "surface_id": "surface.sidecar_peer_rehearsal_audit.synthetic",
                "kind": "audit_descriptor",
                "rate_class": "control",
                "acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_status": "not_created",
            },
        ],
        "lifecycle_states": [
            "proposed",
            "operator_approval_required",
            "manifold_reviewing",
            "accepted_by_manifold",
            "rejected_by_manifold",
            "retired",
        ],
        "candidate_intake_fields": [
            "source_agent_id",
            "observed_peer_id",
            "observed_at",
            "status",
            "truth_level",
            "transport_mode",
            "redaction_class",
            "staleness_policy",
        ],
        "candidate_audit_fields": [
            "source_plan_id",
            "contract_id",
            "operator_approval_status",
            "acceptance_status",
            "rejection_reason",
            "accepted_state_owner",
            "audit_owner",
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
        ],
    }
    hostess_boundary = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "request_descriptor_fields": {
            "required_authority": "rusty.manifold_or_operator",
            "allowed_action_class": "operator_recovery_request_descriptor",
            "implementation_status": "not_implemented",
        },
        "required_rejection_terms": [
            "manifold_acceptance_missing",
            "operator_request_missing",
            "sidecar_device_action_forbidden",
        ],
    }
    validation_slots = [
        {
            "slot_id": "slot.schema_and_fixture_validation",
            "owner": "rusty.quest.sidecar_mesh",
            "protected_risk": "contract_descriptor_drift",
            "command": "python tools/validate_repo.py --repo-root .",
        },
        {
            "slot_id": "slot.damaged_boundary_fixtures",
            "owner": "rusty.quest.sidecar_mesh",
            "protected_risk": "sidecar_authority_drift",
            "command": "python -m unittest discover -s tests -p test_*.py",
        },
        {
            "slot_id": "slot.future_manifold_contract_gate",
            "owner": "rusty.manifold",
            "protected_risk": "accepted_state_without_manifold_audit",
            "command": "future manifold adapter tests must reject endpoint, command, ADB, stale, and untrusted peer status inputs",
        },
    ]
    rollback_policy = {
        "rollback_owner": "rusty.manifold",
        "sidecar_rollback_role": "emit_retire_proposal_only",
        "accepted_state_removal_owner": "rusty.manifold",
        "audit_record_required": True,
        "hostess_action_required": False,
    }

    checks = [
        check(
            "manifold_contract.source_peer_plan_ready",
            peer_plan_result.ok
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
            "manifold_contract.no_live_integration",
            not any(integration_status.values()),
            integration_status,
            {
                "manifold_repo_touched": False,
                "hostess_repo_touched": False,
                "live_device_used": False,
                "runtime_route_created": False,
                "accepted_manifold_state_created": False,
                "hostess_route_created": False,
            },
            "contract review does not touch live repos, devices, routes, or accepted state",
        ),
        check(
            "manifold_contract.manifold_authority",
            authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["sidecar_role"] == "observer_proposer"
            and authority["proposal_status"] == "not_accepted",
            {
                "runtime_authority_owner": authority["runtime_authority_owner"],
                "session_authority_owner": authority["session_authority_owner"],
                "audit_owner": authority["audit_owner"],
                "accepted_state_owner": authority["accepted_state_owner"],
                "sidecar_role": authority["sidecar_role"],
                "proposal_status": authority["proposal_status"],
            },
            {
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "sidecar_role": "observer_proposer",
                "proposal_status": "not_accepted",
            },
            "Manifold owns command/session/audit authority; sidecar only proposes",
        ),
        check(
            "manifold_contract.surfaces_candidate_only",
            proposed_manifold_contract["status"] == "candidate"
            and all(surface["acceptance_owner"] == "rusty.manifold" for surface in proposed_manifold_contract["surfaces"])
            and all(surface["audit_owner"] == "rusty.manifold.audit" for surface in proposed_manifold_contract["surfaces"])
            and all(surface["accepted_state_status"] == "not_created" for surface in proposed_manifold_contract["surfaces"]),
            {
                "status": proposed_manifold_contract["status"],
                "surface_count": len(proposed_manifold_contract["surfaces"]),
                "accepted_state_statuses": [surface["accepted_state_status"] for surface in proposed_manifold_contract["surfaces"]],
            },
            {
                "status": "candidate",
                "surface_count": 3,
                "accepted_state_status": "not_created",
            },
            "proposed Manifold surfaces remain descriptors only",
        ),
        check(
            "manifold_contract.rejection_vocabulary_complete",
            set(proposed_manifold_contract["required_rejection_terms"]) >= {
                "operator_approval_missing",
                "endpoint_values_rejected",
                "commands_rejected",
                "adb_rejected",
                "stale_peer_status",
                "untrusted_sidecar",
                "redaction_incomplete",
            },
            sorted(proposed_manifold_contract["required_rejection_terms"]),
            sorted(
                [
                    "operator_approval_missing",
                    "endpoint_values_rejected",
                    "commands_rejected",
                    "adb_rejected",
                    "stale_peer_status",
                    "untrusted_sidecar",
                    "redaction_incomplete",
                ]
            ),
            "future Manifold adapter must reject unsafe peer status inputs",
        ),
        check(
            "manifold_contract.hostess_boundary_descriptor_only",
            hostess_boundary["status"] == "future_lane_not_requested"
            and hostess_boundary["route_status"] == "not_created"
            and hostess_boundary["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary["input_role"] == "manifold_accepted_state_or_operator_request",
            {
                "status": hostess_boundary["status"],
                "route_status": hostess_boundary["route_status"],
                "device_action_authority": hostess_boundary["device_action_authority"],
                "input_role": hostess_boundary["input_role"],
            },
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "input_role": "manifold_accepted_state_or_operator_request",
            },
            "Hostess remains a future operator-recovery descriptor lane",
        ),
        check(
            "manifold_contract.validation_slots_present",
            len(validation_slots) == 3
            and {slot["slot_id"] for slot in validation_slots}
            == {
                "slot.schema_and_fixture_validation",
                "slot.damaged_boundary_fixtures",
                "slot.future_manifold_contract_gate",
            },
            sorted(slot["slot_id"] for slot in validation_slots),
            sorted(
                [
                    "slot.schema_and_fixture_validation",
                    "slot.damaged_boundary_fixtures",
                    "slot.future_manifold_contract_gate",
                ]
            ),
            "contract review names local and future Manifold validation slots",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": REVIEW_SCHEMA,
        "review_id": "review.manifold_adapter_contract.synthetic.001",
        "generated_at": now,
        "review_status": "contract_ready" if fail_count == 0 else "blocked",
        "source_peer_rehearsal_plan": {
            "path": relative_output_path(peer_plan_path, repo_root),
            "schema": peer_plan.get("schema"),
            "plan_id": peer_plan.get("plan_id"),
            "plan_status": peer_plan.get("plan_status"),
            "next_gate": peer_plan.get("next_gate"),
        },
        "integration_status": integration_status,
        "contract_scope": contract_scope,
        "authority": authority,
        "proposed_manifold_contract": proposed_manifold_contract,
        "hostess_boundary": hostess_boundary,
        "validation_slots": validation_slots,
        "rollback_policy": rollback_policy,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": len(checks) - fail_count,
            "manual_review_count": 0,
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "The Manifold adapter contract review is descriptor evidence only; it does not create a Manifold route, Hostess route, live Quest run, ADB path, socket, endpoint discovery, install, launch, recovery path, remote desktop path, file copy path, or command execution path.",
            "Manifold remains the future command/session/audit and accepted-state authority for sidecar peer status intake.",
            "Hostess remains a future operator-recovery lane after Manifold acceptance or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "manifold_owned_adapter_contract_or_operator_approved_private_rehearsal_evidence",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--peer-plan", required=True, help="Generated configured peer rehearsal plan fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output contract review path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        review = build_review(Path(args.peer_plan), repo_root, args.now)
        write_json(Path(args.output), review)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"review_manifold_adapter_contract failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": review["review_status"], "check_count": review["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
