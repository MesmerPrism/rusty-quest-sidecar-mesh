#!/usr/bin/env python3
"""Generate a descriptor-only request for future Manifold contract intake."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


REQUEST_SCHEMA = "rusty.quest.sidecar.manifold_contract_intake_request.v1"
HANDOFF_PACKAGE_SCHEMA = "rusty.quest.sidecar.manifold_handoff_package.v1"


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


def build_request(handoff_package_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    handoff_package = load_json(handoff_package_path)
    package_result = validate_repo.validate_json_file(handoff_package_path)

    source_handoff_package = {
        "path": relative_output_path(handoff_package_path, repo_root),
        "schema": handoff_package.get("schema"),
        "package_id": handoff_package.get("package_id"),
        "package_status": handoff_package.get("package_status"),
        "next_gate": handoff_package.get("next_gate"),
    }
    request_scope = {
        "request_class": "manifold_contract_intake_descriptor",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "implementation_status": "not_implemented",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "live_evidence_status": "not_included",
    }
    authority = {
        "request_owner": "rusty.quest.sidecar_mesh",
        "intake_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    package_handoff = handoff_package.get("proposed_manifold_handoff", {})
    proposed_contract_intake = {
        "intake_id": "intake.sidecar_mesh_contract.synthetic.001",
        "status": "candidate",
        "target_repo": "rusty.manifold",
        "requested_request_type": "open_sidecar_mesh_contract_intake",
        "candidate_surfaces": package_handoff.get("target_surfaces", []),
        "candidate_validation_slots": package_handoff.get("required_validation_slots", []),
        "required_rejection_terms": package_handoff.get("required_rejection_terms", []),
        "required_acceptance_owner": "rusty.manifold",
        "required_audit_owner": "rusty.manifold.audit",
        "accepted_state_status": "not_created",
        "hostess_escalation_input": "manifold_accepted_state_or_operator_request",
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
            "python tools/prepare_manifold_contract_intake.py --handoff-package fixtures/valid/manifold-handoff-package.synthetic.json --now 2026-06-04T22:48:00Z --output fixtures/valid/manifold-contract-intake-request.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_schema_route_acceptance_and_audit",
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

    required_surfaces = {
        "sidecar_peer_status_source",
        "sidecar_peer_status_intake",
        "sidecar_peer_rehearsal_audit",
    }
    required_slots = {
        "slot.schema_and_fixture_validation",
        "slot.damaged_boundary_fixtures",
        "slot.future_manifold_contract_gate",
    }
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
            "contract_intake.source_package_ready",
            package_result.ok
            and handoff_package.get("schema") == HANDOFF_PACKAGE_SCHEMA
            and handoff_package.get("package_status") == "handoff_package_ready"
            and handoff_package.get("next_gate") == "manifold_repo_contract_intake_or_operator_approved_private_rehearsal_evidence",
            {
                "schema": handoff_package.get("schema"),
                "package_status": handoff_package.get("package_status"),
                "next_gate": handoff_package.get("next_gate"),
            },
            {
                "schema": HANDOFF_PACKAGE_SCHEMA,
                "package_status": "handoff_package_ready",
                "next_gate": "manifold_repo_contract_intake_or_operator_approved_private_rehearsal_evidence",
            },
            relative_output_path(handoff_package_path, repo_root),
        ),
        check(
            "contract_intake.no_repo_route_or_state",
            request_scope["repo_touch_status"] == "not_touched"
            and request_scope["route_status"] == "not_created"
            and request_scope["accepted_state_status"] == "not_created"
            and request_scope["live_evidence_status"] == "not_included"
            and proposed_contract_intake["accepted_state_status"] == "not_created",
            {
                "repo_touch_status": request_scope["repo_touch_status"],
                "route_status": request_scope["route_status"],
                "accepted_state_status": request_scope["accepted_state_status"],
                "live_evidence_status": request_scope["live_evidence_status"],
                "intake_accepted_state_status": proposed_contract_intake["accepted_state_status"],
            },
            {
                "repo_touch_status": "not_touched",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "live_evidence_status": "not_included",
                "intake_accepted_state_status": "not_created",
            },
            "contract intake request does not touch Manifold or create route/state",
        ),
        check(
            "contract_intake.manifold_authority",
            authority["intake_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["sidecar_role"] == "observer_proposer",
            {
                "intake_acceptance_owner": authority["intake_acceptance_owner"],
                "runtime_authority_owner": authority["runtime_authority_owner"],
                "session_authority_owner": authority["session_authority_owner"],
                "audit_owner": authority["audit_owner"],
                "accepted_state_owner": authority["accepted_state_owner"],
                "sidecar_role": authority["sidecar_role"],
            },
            {
                "intake_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "sidecar_role": "observer_proposer",
            },
            "Manifold remains intake acceptance, runtime, session, accepted-state, and audit authority",
        ),
        check(
            "contract_intake.surfaces_slots_and_rejections",
            required_surfaces <= set(proposed_contract_intake["candidate_surfaces"])
            and required_slots <= set(proposed_contract_intake["candidate_validation_slots"])
            and required_rejections <= set(proposed_contract_intake["required_rejection_terms"]),
            {
                "candidate_surfaces": proposed_contract_intake["candidate_surfaces"],
                "candidate_validation_slots": proposed_contract_intake["candidate_validation_slots"],
                "required_rejection_terms": proposed_contract_intake["required_rejection_terms"],
            },
            {
                "required_surfaces": sorted(required_surfaces),
                "required_validation_slots": sorted(required_slots),
                "required_rejection_terms": sorted(required_rejections),
            },
            "contract intake request carries the candidate Manifold surfaces, validation slots, and rejection terms",
        ),
        check(
            "contract_intake.hostess_boundary",
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
        check(
            "contract_intake.privacy_boundary",
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
            "contract intake request remains public-safe synthetic descriptor evidence",
        ),
        check(
            "contract_intake.validation_gate",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_schema_route_acceptance_and_audit",
            validation_evidence,
            {
                "local_validation_status": "expected_pass",
                "damaged_fixture_policy": "must_fail_validation",
                "future_manifold_gate": "manifold_repo_owns_schema_route_acceptance_and_audit",
            },
            "contract intake request records validation and future Manifold ownership gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": REQUEST_SCHEMA,
        "request_id": "request.sidecar_mesh_manifold_contract_intake.synthetic.001",
        "generated_at": now,
        "request_status": "ready_for_manifold_contract_intake" if fail_count == 0 else "blocked",
        "source_handoff_package": source_handoff_package,
        "request_scope": request_scope,
        "authority": authority,
        "proposed_contract_intake": proposed_contract_intake,
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
            "The Manifold contract intake request is descriptor evidence only; it does not touch the Manifold repo, create a Manifold route, create accepted Manifold state, touch Hostess, start a live Quest run, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future command/session/audit and accepted-state authority for sidecar peer status intake.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-package", required=True, help="Generated Manifold handoff package fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output contract intake request path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        request = build_request(Path(args.handoff_package), repo_root, args.now)
        write_json(Path(args.output), request)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_contract_intake failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": request["request_status"], "check_count": request["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
