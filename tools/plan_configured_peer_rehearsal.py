#!/usr/bin/env python3
"""Generate the descriptor-only plan for a configured peer rehearsal."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


PLAN_SCHEMA = "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1"
HANDOFF_REVIEW_SCHEMA = "rusty.quest.sidecar.no_network_prototype_handoff_review.v1"


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


def build_plan(handoff_review_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    handoff = load_json(handoff_review_path)
    handoff_result = validate_repo.validate_json_file(handoff_review_path)

    source_handoff_review = {
        "path": relative_output_path(handoff_review_path, repo_root),
        "schema": handoff.get("schema"),
        "review_id": handoff.get("review_id"),
        "review_status": handoff.get("review_status"),
        "next_gate": handoff.get("next_gate"),
    }
    rehearsal_scope = {
        "scope_class": "configured_peer_status_rehearsal",
        "source_mode": "synthetic_fixture",
        "live_exchange_status": "not_started",
        "status_payload_class": "low_rate_advisory_status",
        "peer_count": 3,
        "operator_approval_required_before_route_start": True,
    }
    authority = {
        "sidecar_role": "observer_proposer",
        "acceptance_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "operator_approval_required": True,
        "proposal_status": "not_accepted",
        "sidecar_device_action_authority": "forbidden",
        "sidecar_command_authority": "forbidden",
    }
    peer_set = [
        {
            "peer_id": "peer.quest_sidecar.synthetic_alpha",
            "role": "local_rehearsal_subject",
            "configured_material_status": "private_evidence_required_not_in_fixture",
            "contains_endpoint_values": False,
            "status_payload_class": "low_rate_advisory_status",
        },
        {
            "peer_id": "peer.quest_sidecar.synthetic_beta",
            "role": "configured_status_peer",
            "configured_material_status": "private_evidence_required_not_in_fixture",
            "contains_endpoint_values": False,
            "status_payload_class": "low_rate_advisory_status",
        },
        {
            "peer_id": "peer.quest_sidecar.synthetic_gamma",
            "role": "configured_status_peer",
            "configured_material_status": "private_evidence_required_not_in_fixture",
            "contains_endpoint_values": False,
            "status_payload_class": "low_rate_advisory_status",
        },
    ]
    transport_policy = {
        "route_policy": "operator_approval_before_transport",
        "status_payload_only": True,
        "commands_allowed": False,
        "adb_allowed": False,
        "remote_desktop_allowed": False,
        "file_transfer_allowed": False,
        "fixture_contains_endpoint_values": False,
        "network_binding_created": False,
        "route_started": False,
        "cleanup_evidence_required": True,
    }
    manifold_readiness = {
        "status": "candidate",
        "target_surface": "sidecar_peer_status_intake",
        "authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "source_role": "proposal_input",
        "acceptance_status": "not_implemented",
        "accepted_state_owner": "rusty.manifold",
        "rejection_terms": [
            "operator_approval_missing",
            "endpoint_values_rejected",
            "commands_rejected",
            "adb_rejected",
            "stale_peer_status",
            "redaction_incomplete",
        ],
    }
    hostess_readiness = {
        "status": "future_lane_not_requested",
        "role": "operator_recovery_after_manifold_acceptance",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "route_status": "not_implemented",
        "request_descriptor_fields": {
            "required_authority": "rusty.manifold_or_operator",
            "allowed_action_class": "operator_recovery_request_descriptor",
            "implementation_status": "not_implemented",
        },
        "rejection_terms": [
            "manifold_acceptance_missing",
            "operator_request_missing",
            "sidecar_device_action_forbidden",
        ],
    }
    evidence_policy = {
        "contains_endpoint_values": False,
        "contains_pairing_material": False,
        "contains_commands": False,
        "contains_raw_logs": False,
        "contains_visual_captures": False,
        "private_evidence_required_before_live_run": True,
        "sanitized_derivative_required": True,
        "public_fixture_policy": "synthetic_descriptor_only",
    }
    steps = [
        {
            "step_id": "approval.collect_operator_approval",
            "status": "planned",
            "owner": "operator",
            "output_class": "private_rehearsal_authorization",
        },
        {
            "step_id": "config.prepare_private_peer_material",
            "status": "planned",
            "owner": "operator",
            "output_class": "private_evidence_not_in_fixture",
        },
        {
            "step_id": "exchange.status_only_peer_rehearsal",
            "status": "planned",
            "owner": "sidecar_agents",
            "output_class": "low_rate_advisory_status",
        },
        {
            "step_id": "evidence.emit_sanitized_route_health",
            "status": "planned",
            "owner": "sidecar_agents",
            "output_class": "sanitized_derivative_fixture",
        },
        {
            "step_id": "handoff.submit_manifold_candidate",
            "status": "planned",
            "owner": "future_manifold_adapter",
            "output_class": "candidate_intake_not_accepted_state",
        },
        {
            "step_id": "hostess.keep_recovery_descriptor_only",
            "status": "planned",
            "owner": "future_hostess_lane",
            "output_class": "operator_recovery_request_descriptor",
        },
    ]

    checks = [
        check(
            "peer_rehearsal.source_handoff_ready",
            handoff_result.ok
            and handoff.get("schema") == HANDOFF_REVIEW_SCHEMA
            and handoff.get("review_status") == "handoff_review_ready"
            and handoff.get("next_gate") == "private_configured_peer_rehearsal_requires_operator_approval",
            {
                "schema": handoff.get("schema"),
                "review_status": handoff.get("review_status"),
                "next_gate": handoff.get("next_gate"),
            },
            {
                "schema": HANDOFF_REVIEW_SCHEMA,
                "review_status": "handoff_review_ready",
                "next_gate": "private_configured_peer_rehearsal_requires_operator_approval",
            },
            relative_output_path(handoff_review_path, repo_root),
        ),
        check(
            "peer_rehearsal.operator_approval_required",
            authority["operator_approval_required"] is True
            and rehearsal_scope["operator_approval_required_before_route_start"] is True
            and transport_policy["route_started"] is False,
            {
                "operator_approval_required": authority["operator_approval_required"],
                "operator_approval_required_before_route_start": rehearsal_scope["operator_approval_required_before_route_start"],
                "route_started": transport_policy["route_started"],
            },
            {
                "operator_approval_required": True,
                "operator_approval_required_before_route_start": True,
                "route_started": False,
            },
            "configured peer rehearsal is planned but not started",
        ),
        check(
            "peer_rehearsal.no_endpoint_or_runtime_payloads",
            transport_policy["fixture_contains_endpoint_values"] is False
            and evidence_policy["contains_endpoint_values"] is False
            and evidence_policy["contains_pairing_material"] is False
            and evidence_policy["contains_commands"] is False,
            {
                "fixture_contains_endpoint_values": transport_policy["fixture_contains_endpoint_values"],
                "contains_endpoint_values": evidence_policy["contains_endpoint_values"],
                "contains_pairing_material": evidence_policy["contains_pairing_material"],
                "contains_commands": evidence_policy["contains_commands"],
            },
            {
                "fixture_contains_endpoint_values": False,
                "contains_endpoint_values": False,
                "contains_pairing_material": False,
                "contains_commands": False,
            },
            "repository fixture remains a sanitized derivative descriptor",
        ),
        check(
            "peer_rehearsal.status_only_transport",
            transport_policy["status_payload_only"] is True
            and transport_policy["commands_allowed"] is False
            and transport_policy["adb_allowed"] is False
            and transport_policy["remote_desktop_allowed"] is False,
            {
                "status_payload_only": transport_policy["status_payload_only"],
                "commands_allowed": transport_policy["commands_allowed"],
                "adb_allowed": transport_policy["adb_allowed"],
                "remote_desktop_allowed": transport_policy["remote_desktop_allowed"],
            },
            {
                "status_payload_only": True,
                "commands_allowed": False,
                "adb_allowed": False,
                "remote_desktop_allowed": False,
            },
            "configured peer rehearsal only permits status gossip descriptors",
        ),
        check(
            "peer_rehearsal.manifold_candidate_only",
            manifold_readiness["authority_owner"] == "rusty.manifold"
            and manifold_readiness["audit_owner"] == "rusty.manifold.audit"
            and manifold_readiness["acceptance_status"] == "not_implemented"
            and manifold_readiness["accepted_state_owner"] == "rusty.manifold",
            {
                "authority_owner": manifold_readiness["authority_owner"],
                "audit_owner": manifold_readiness["audit_owner"],
                "acceptance_status": manifold_readiness["acceptance_status"],
                "accepted_state_owner": manifold_readiness["accepted_state_owner"],
            },
            {
                "authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "acceptance_status": "not_implemented",
                "accepted_state_owner": "rusty.manifold",
            },
            "future Manifold intake remains candidate-only",
        ),
        check(
            "peer_rehearsal.hostess_descriptor_only",
            hostess_readiness["status"] == "future_lane_not_requested"
            and hostess_readiness["device_action_authority"] == "not_in_sidecar"
            and hostess_readiness["input_role"] == "manifold_accepted_state_or_operator_request"
            and hostess_readiness["route_status"] == "not_implemented",
            {
                "status": hostess_readiness["status"],
                "device_action_authority": hostess_readiness["device_action_authority"],
                "input_role": hostess_readiness["input_role"],
                "route_status": hostess_readiness["route_status"],
            },
            {
                "status": "future_lane_not_requested",
                "device_action_authority": "not_in_sidecar",
                "input_role": "manifold_accepted_state_or_operator_request",
                "route_status": "not_implemented",
            },
            "Hostess recovery remains future descriptor-only integration",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": PLAN_SCHEMA,
        "plan_id": "plan.configured_peer_rehearsal.synthetic.001",
        "generated_at": now,
        "plan_status": "operator_approval_required" if fail_count == 0 else "blocked",
        "source_handoff_review": source_handoff_review,
        "rehearsal_scope": rehearsal_scope,
        "authority": authority,
        "peer_set": peer_set,
        "transport_policy": transport_policy,
        "manifold_readiness": manifold_readiness,
        "hostess_readiness": hostess_readiness,
        "evidence_policy": evidence_policy,
        "steps": steps,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": len(checks) - fail_count,
            "manual_review_count": 0,
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "The configured peer rehearsal plan is a descriptor only; it does not start routes, bind network ports, use ADB, open remote desktop, copy files, install apps, launch apps, recover devices, execute commands, or mutate Manifold state.",
            "Manifold remains the future owner of acceptance, rejection, revision, lease, topology, and audit records.",
            "Hostess remains a future operator-recovery lane after Manifold acceptance or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-review", required=True, help="Generated no-network prototype handoff review fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output rehearsal plan path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        plan = build_plan(Path(args.handoff_review), repo_root, args.now)
        write_json(Path(args.output), plan)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"plan_configured_peer_rehearsal failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": plan["plan_status"], "check_count": plan["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
