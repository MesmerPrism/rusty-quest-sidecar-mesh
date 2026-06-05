#!/usr/bin/env python3
"""Generate a descriptor-only handoff package for future Manifold work."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


PACKAGE_SCHEMA = "rusty.quest.sidecar.manifold_handoff_package.v1"
CONTRACT_REVIEW_SCHEMA = "rusty.quest.sidecar.manifold_adapter_contract_review.v1"


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


def build_package(contract_review_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    contract_review = load_json(contract_review_path)
    contract_result = validate_repo.validate_json_file(contract_review_path)

    artifact_set = [
        {
            "artifact_id": "artifact.public_lab_intake_report",
            "path": "fixtures/valid/public-lab-artifact-intake-report.synthetic.json",
            "schema": "rusty.quest.sidecar.public_lab_artifact_intake_report.v1",
            "role": "sanitized_source_evidence",
            "required_for_handoff": True,
        },
        {
            "artifact_id": "artifact.no_network_agent_recipe",
            "path": "fixtures/valid/no-network-agent-recipe.synthetic.json",
            "schema": "rusty.quest.sidecar.no_network_agent_recipe.v1",
            "role": "sidecar_runtime_boundary",
            "required_for_handoff": True,
        },
        {
            "artifact_id": "artifact.no_network_prototype_run",
            "path": "fixtures/valid/no-network-agent-run.synthetic.json",
            "schema": "rusty.quest.sidecar.no_network_agent_run.v1",
            "role": "offline_generation_evidence",
            "required_for_handoff": True,
        },
        {
            "artifact_id": "artifact.no_network_handoff_review",
            "path": "fixtures/valid/no-network-prototype-handoff-review.synthetic.json",
            "schema": "rusty.quest.sidecar.no_network_prototype_handoff_review.v1",
            "role": "manifold_hostess_mapping_evidence",
            "required_for_handoff": True,
        },
        {
            "artifact_id": "artifact.configured_peer_rehearsal_plan",
            "path": "fixtures/valid/configured-peer-rehearsal-plan.synthetic.json",
            "schema": "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1",
            "role": "future_peer_status_rehearsal_descriptor",
            "required_for_handoff": True,
        },
        {
            "artifact_id": "artifact.manifold_adapter_contract_review",
            "path": relative_output_path(contract_review_path, repo_root),
            "schema": CONTRACT_REVIEW_SCHEMA,
            "role": "future_manifold_adapter_contract_descriptor",
            "required_for_handoff": True,
        },
        {
            "artifact_id": "artifact.integration_acceptance_scorecard",
            "path": "fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "schema": "rusty.quest.sidecar.integration_acceptance_scorecard.v1",
            "role": "local_acceptance_evidence",
            "required_for_handoff": True,
        },
    ]
    package_scope = {
        "package_class": "manifold_handoff_descriptor",
        "source_mode": "synthetic_fixture",
        "implementation_status": "not_implemented",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "live_evidence_status": "not_included",
    }
    authority = {
        "package_owner": "rusty.quest.sidecar_mesh",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    proposed_handoff = {
        "handoff_id": "handoff.sidecar_mesh_to_manifold.synthetic.001",
        "status": "candidate",
        "target_repo": "rusty.manifold",
        "target_surfaces": [
            "sidecar_peer_status_source",
            "sidecar_peer_status_intake",
            "sidecar_peer_rehearsal_audit",
        ],
        "required_acceptance_owner": "rusty.manifold",
        "required_audit_owner": "rusty.manifold.audit",
        "accepted_state_status": "not_created",
        "required_rejection_terms": contract_review.get("proposed_manifold_contract", {}).get("required_rejection_terms", []),
        "required_validation_slots": [slot.get("slot_id") for slot in contract_review.get("validation_slots", [])],
    }
    hostess_boundary = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/package_manifold_handoff.py --contract-review fixtures/valid/manifold-adapter-contract-review.synthetic.json --now 2026-06-04T22:40:00Z --output fixtures/valid/manifold-handoff-package.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "reject_endpoint_command_adb_stale_untrusted_inputs_before_acceptance",
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

    checks = [
        check(
            "handoff_package.contract_review_ready",
            contract_result.ok
            and contract_review.get("schema") == CONTRACT_REVIEW_SCHEMA
            and contract_review.get("review_status") == "contract_ready"
            and contract_review.get("next_gate") == "manifold_owned_adapter_contract_or_operator_approved_private_rehearsal_evidence",
            {
                "schema": contract_review.get("schema"),
                "review_status": contract_review.get("review_status"),
                "next_gate": contract_review.get("next_gate"),
            },
            {
                "schema": CONTRACT_REVIEW_SCHEMA,
                "review_status": "contract_ready",
                "next_gate": "manifold_owned_adapter_contract_or_operator_approved_private_rehearsal_evidence",
            },
            relative_output_path(contract_review_path, repo_root),
        ),
        check(
            "handoff_package.artifact_set_complete",
            len(artifact_set) == 7 and all(artifact["required_for_handoff"] is True for artifact in artifact_set),
            [artifact["artifact_id"] for artifact in artifact_set],
            [
                "artifact.public_lab_intake_report",
                "artifact.no_network_agent_recipe",
                "artifact.no_network_prototype_run",
                "artifact.no_network_handoff_review",
                "artifact.configured_peer_rehearsal_plan",
                "artifact.manifold_adapter_contract_review",
                "artifact.integration_acceptance_scorecard",
            ],
            "handoff package names the generated sidecar evidence chain",
        ),
        check(
            "handoff_package.no_live_or_accepted_state",
            package_scope["route_status"] == "not_created"
            and package_scope["accepted_state_status"] == "not_created"
            and package_scope["live_evidence_status"] == "not_included"
            and proposed_handoff["accepted_state_status"] == "not_created",
            {
                "route_status": package_scope["route_status"],
                "accepted_state_status": package_scope["accepted_state_status"],
                "live_evidence_status": package_scope["live_evidence_status"],
                "handoff_accepted_state_status": proposed_handoff["accepted_state_status"],
            },
            {
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "live_evidence_status": "not_included",
                "handoff_accepted_state_status": "not_created",
            },
            "handoff package does not create routes, live evidence, or accepted state",
        ),
        check(
            "handoff_package.manifold_authority",
            authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["sidecar_role"] == "observer_proposer",
            {
                "handoff_acceptance_owner": authority["handoff_acceptance_owner"],
                "runtime_authority_owner": authority["runtime_authority_owner"],
                "session_authority_owner": authority["session_authority_owner"],
                "audit_owner": authority["audit_owner"],
                "accepted_state_owner": authority["accepted_state_owner"],
                "sidecar_role": authority["sidecar_role"],
            },
            {
                "handoff_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "sidecar_role": "observer_proposer",
            },
            "Manifold remains the handoff acceptance and runtime authority",
        ),
        check(
            "handoff_package.privacy_boundary",
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
            and privacy_boundary["public_fixture_policy"] == "synthetic_descriptor_only",
            privacy_boundary,
            {
                "contains_endpoint_values": False,
                "contains_pairing_material": False,
                "contains_commands": False,
                "contains_raw_logs": False,
                "contains_visual_captures": False,
                "contains_private_device_ids": False,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "handoff package remains public-safe synthetic descriptor evidence",
        ),
        check(
            "handoff_package.hostess_boundary",
            hostess_boundary["status"] == "future_lane_not_requested"
            and hostess_boundary["route_status"] == "not_created"
            and hostess_boundary["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary["input_role"] == "manifold_accepted_state_or_operator_request",
            hostess_boundary,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "input_role": "manifold_accepted_state_or_operator_request",
            },
            "Hostess remains descriptor-only and cannot be driven by sidecar authority",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": PACKAGE_SCHEMA,
        "package_id": "package.sidecar_mesh_manifold_handoff.synthetic.001",
        "generated_at": now,
        "package_status": "handoff_package_ready" if fail_count == 0 else "blocked",
        "source_contract_review": {
            "path": relative_output_path(contract_review_path, repo_root),
            "schema": contract_review.get("schema"),
            "review_id": contract_review.get("review_id"),
            "review_status": contract_review.get("review_status"),
            "next_gate": contract_review.get("next_gate"),
        },
        "package_scope": package_scope,
        "authority": authority,
        "artifact_set": artifact_set,
        "proposed_manifold_handoff": proposed_handoff,
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
            "The Manifold handoff package is descriptor evidence only; it does not create a Manifold route, Hostess route, live Quest run, ADB path, socket, endpoint discovery, install, launch, recovery path, remote desktop path, file copy path, or command execution path.",
            "Manifold remains the future command/session/audit and accepted-state authority for sidecar peer status intake.",
            "Hostess remains a future operator-recovery lane after Manifold acceptance or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "manifold_repo_contract_intake_or_operator_approved_private_rehearsal_evidence",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract-review", required=True, help="Generated Manifold adapter contract review fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output handoff package path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        package = build_package(Path(args.contract_review), repo_root, args.now)
        write_json(Path(args.output), package)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"package_manifold_handoff failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": package["package_status"], "check_count": package["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
