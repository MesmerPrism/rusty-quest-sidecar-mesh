#!/usr/bin/env python3
"""Generate a sidecar-owned expectation for a future Hostess boundary descriptor."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


EXPECTATION_SCHEMA = "rusty.quest.sidecar.hostess_boundary_descriptor_expectation.v1"
RESPONSE_HANDOFF_SCHEMA = "rusty.quest.sidecar.manifold_response_handoff_package.v1"


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


def build_expectation(response_handoff_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    response_handoff = load_json(response_handoff_path)
    handoff_result = validate_repo.validate_json_file(response_handoff_path)

    source_manifold_response_handoff_package = {
        "path": relative_output_path(response_handoff_path, repo_root),
        "schema": response_handoff.get("schema"),
        "package_id": response_handoff.get("package_id"),
        "package_status": response_handoff.get("package_status"),
        "next_gate": response_handoff.get("next_gate"),
    }
    expectation_scope = {
        "expectation_class": "hostess_boundary_descriptor_expectation",
        "source_mode": "synthetic_fixture",
        "target_descriptor_owner": "rusty.manifold",
        "future_consumer": "rusty.hostess",
        "manifold_repo_touch_status": "not_touched",
        "hostess_repo_touch_status": "not_touched",
        "hostess_route_status": "not_created",
        "manifold_accepted_state_status": "not_created",
        "operator_request_status": "not_recorded",
        "live_evidence_status": "not_included",
    }
    authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "boundary_descriptor_owner": "rusty.manifold",
        "source_of_truth_owner": "rusty.manifold",
        "response_decision_owner": "rusty.manifold",
        "accepted_state_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "future_hostess_route_owner": "rusty.hostess",
        "future_hostess_route_enablement_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    expected_hostess_boundary_descriptor = {
        "descriptor_status": "not_created",
        "descriptor_kind": "hostess_operator_recovery_boundary",
        "input_source_policy": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allows_endpoint_values": False,
        "allows_commands": False,
        "allows_adb": False,
        "allows_high_rate_payloads": False,
        "allowed_action_classes": [
            "read_only_status_view_descriptor",
            "operator_recovery_request_descriptor",
        ],
        "disallowed_input_classes": [
            "sidecar_peer_message_direct",
            "endpoint_values",
            "commands",
            "adb",
            "high_rate_payloads",
            "raw_logs",
            "visual_captures",
            "pairing_material",
        ],
        "required_descriptor_fields": [
            "manifold_decision_id",
            "accepted_state_id",
            "source_handoff_package_id",
            "decision_status",
            "operator_request_status",
            "rejection_terms",
            "audit_record_id",
            "privacy_boundary",
        ],
        "required_hostess_validation_slots": [
            "slot.hostess_boundary_descriptor_schema",
            "slot.hostess_rejects_sidecar_direct_input",
            "slot.hostess_requires_manifold_accepted_state",
            "slot.hostess_requires_operator_request_for_recovery",
            "slot.hostess_privacy_redaction_check",
            "slot.hostess_no_device_action_fixture",
        ],
        "safe_to_create_hostess_route": False,
    }
    manifold_acceptance_gate = {
        "handoff_acceptance_status": response_handoff.get("handoff_manifest", {}).get("handoff_acceptance_status"),
        "response_decision_status": response_handoff.get("package_scope", {}).get("decision_status"),
        "accepted_state_status": response_handoff.get("package_scope", {}).get("accepted_state_status"),
        "audit_record_status": response_handoff.get("package_scope", {}).get("audit_record_status"),
        "required_response_decision": "accepted_for_manifold_slice",
        "hostess_boundary_descriptor_status": "not_created",
        "hostess_route_status": "not_created",
        "hostess_enablement_status": "not_enabled",
        "gate_result": "hostess_boundary_descriptor_not_ready_for_route_creation",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_hostess_boundary_descriptor_expectation.py --response-handoff fixtures/valid/manifold-response-handoff-package.synthetic.json --now 2026-06-04T23:44:00Z --output fixtures/valid/hostess-boundary-descriptor-expectation.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_response_acceptance_before_hostess_descriptor_creation",
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
        "manifold_decision_id",
        "accepted_state_id",
        "source_handoff_package_id",
        "decision_status",
        "operator_request_status",
        "rejection_terms",
        "audit_record_id",
        "privacy_boundary",
    }
    required_slots = {
        "slot.hostess_boundary_descriptor_schema",
        "slot.hostess_rejects_sidecar_direct_input",
        "slot.hostess_requires_manifold_accepted_state",
        "slot.hostess_requires_operator_request_for_recovery",
        "slot.hostess_privacy_redaction_check",
        "slot.hostess_no_device_action_fixture",
    }
    checks = [
        check(
            "hostess_boundary_expectation.source_handoff_ready",
            handoff_result.ok
            and response_handoff.get("schema") == RESPONSE_HANDOFF_SCHEMA
            and response_handoff.get("package_status") == "response_handoff_package_ready"
            and response_handoff.get("next_gate") == "manifold_repo_response_slice_or_operator_decision",
            {
                "schema": response_handoff.get("schema"),
                "package_status": response_handoff.get("package_status"),
                "next_gate": response_handoff.get("next_gate"),
            },
            {
                "schema": RESPONSE_HANDOFF_SCHEMA,
                "package_status": "response_handoff_package_ready",
                "next_gate": "manifold_repo_response_slice_or_operator_decision",
            },
            relative_output_path(response_handoff_path, repo_root),
        ),
        check(
            "hostess_boundary_expectation.no_repo_route_state_or_live_evidence",
            expectation_scope["manifold_repo_touch_status"] == "not_touched"
            and expectation_scope["hostess_repo_touch_status"] == "not_touched"
            and expectation_scope["hostess_route_status"] == "not_created"
            and expectation_scope["manifold_accepted_state_status"] == "not_created"
            and expectation_scope["operator_request_status"] == "not_recorded"
            and expectation_scope["live_evidence_status"] == "not_included",
            expectation_scope,
            {
                "manifold_repo_touch_status": "not_touched",
                "hostess_repo_touch_status": "not_touched",
                "hostess_route_status": "not_created",
                "manifold_accepted_state_status": "not_created",
                "operator_request_status": "not_recorded",
                "live_evidence_status": "not_included",
            },
            "expectation does not touch Manifold, Hostess, create routes, accepted state, operator request, or live evidence",
        ),
        check(
            "hostess_boundary_expectation.authority_split",
            authority["boundary_descriptor_owner"] == "rusty.manifold"
            and authority["source_of_truth_owner"] == "rusty.manifold"
            and authority["response_decision_owner"] == "rusty.manifold"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["future_hostess_route_owner"] == "rusty.hostess"
            and authority["future_hostess_route_enablement_owner"] == "rusty.manifold"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer"
            and authority["proposal_status"] == "not_accepted",
            authority,
            {
                "boundary_descriptor_owner": "rusty.manifold",
                "source_of_truth_owner": "rusty.manifold",
                "response_decision_owner": "rusty.manifold",
                "accepted_state_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "future_hostess_route_owner": "rusty.hostess",
                "future_hostess_route_enablement_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
                "proposal_status": "not_accepted",
            },
            "Manifold owns the future descriptor and enablement gate; Hostess owns only a future route after explicit gate",
        ),
        check(
            "hostess_boundary_expectation.descriptor_constraints",
            expected_hostess_boundary_descriptor["descriptor_status"] == "not_created"
            and expected_hostess_boundary_descriptor["input_source_policy"] == "manifold_accepted_state_or_operator_request_descriptor"
            and expected_hostess_boundary_descriptor["sidecar_direct_input_allowed"] is False
            and expected_hostess_boundary_descriptor["requires_manifold_accepted_state"] is True
            and expected_hostess_boundary_descriptor["requires_explicit_operator_request"] is True
            and expected_hostess_boundary_descriptor["allows_endpoint_values"] is False
            and expected_hostess_boundary_descriptor["allows_commands"] is False
            and expected_hostess_boundary_descriptor["allows_adb"] is False
            and expected_hostess_boundary_descriptor["allows_high_rate_payloads"] is False
            and expected_hostess_boundary_descriptor["safe_to_create_hostess_route"] is False,
            expected_hostess_boundary_descriptor,
            {
                "descriptor_status": "not_created",
                "input_source_policy": "manifold_accepted_state_or_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "safe_to_create_hostess_route": False,
            },
            "future Hostess boundary descriptor stays gated and cannot accept sidecar-direct device-action input",
        ),
        check(
            "hostess_boundary_expectation.required_fields_and_validation_slots",
            required_fields <= set(expected_hostess_boundary_descriptor["required_descriptor_fields"])
            and required_slots <= set(expected_hostess_boundary_descriptor["required_hostess_validation_slots"])
            and set(expected_hostess_boundary_descriptor["allowed_action_classes"]) == {
                "read_only_status_view_descriptor",
                "operator_recovery_request_descriptor",
            }
            and {
                "sidecar_peer_message_direct",
                "endpoint_values",
                "commands",
                "adb",
                "high_rate_payloads",
                "raw_logs",
                "visual_captures",
                "pairing_material",
            }
            <= set(expected_hostess_boundary_descriptor["disallowed_input_classes"]),
            {
                "required_descriptor_fields": expected_hostess_boundary_descriptor["required_descriptor_fields"],
                "required_hostess_validation_slots": expected_hostess_boundary_descriptor["required_hostess_validation_slots"],
                "allowed_action_classes": expected_hostess_boundary_descriptor["allowed_action_classes"],
                "disallowed_input_classes": expected_hostess_boundary_descriptor["disallowed_input_classes"],
            },
            {
                "required_descriptor_fields": sorted(required_fields),
                "required_hostess_validation_slots": sorted(required_slots),
                "allowed_action_classes": [
                    "operator_recovery_request_descriptor",
                    "read_only_status_view_descriptor",
                ],
                "disallowed_input_classes": [
                    "adb",
                    "commands",
                    "endpoint_values",
                    "high_rate_payloads",
                    "pairing_material",
                    "raw_logs",
                    "sidecar_peer_message_direct",
                    "visual_captures",
                ],
            },
            "future descriptor includes enough fields and validation slots for Hostess without accepting device-action payloads",
        ),
        check(
            "hostess_boundary_expectation.manifold_gate_not_satisfied",
            manifold_acceptance_gate["handoff_acceptance_status"] == "not_accepted"
            and manifold_acceptance_gate["response_decision_status"] == "not_decided"
            and manifold_acceptance_gate["accepted_state_status"] == "not_created"
            and manifold_acceptance_gate["audit_record_status"] == "not_created"
            and manifold_acceptance_gate["required_response_decision"] == "accepted_for_manifold_slice"
            and manifold_acceptance_gate["hostess_boundary_descriptor_status"] == "not_created"
            and manifold_acceptance_gate["hostess_route_status"] == "not_created"
            and manifold_acceptance_gate["hostess_enablement_status"] == "not_enabled"
            and manifold_acceptance_gate["gate_result"] == "hostess_boundary_descriptor_not_ready_for_route_creation",
            manifold_acceptance_gate,
            {
                "handoff_acceptance_status": "not_accepted",
                "response_decision_status": "not_decided",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "required_response_decision": "accepted_for_manifold_slice",
                "hostess_boundary_descriptor_status": "not_created",
                "hostess_route_status": "not_created",
                "hostess_enablement_status": "not_enabled",
                "gate_result": "hostess_boundary_descriptor_not_ready_for_route_creation",
            },
            "current package is not a Manifold acceptance; Hostess descriptor and route remain not ready",
        ),
        check(
            "hostess_boundary_expectation.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_response_acceptance_before_hostess_descriptor_creation"
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
                "future_manifold_gate": "manifold_response_acceptance_before_hostess_descriptor_creation",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "Hostess boundary expectation remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": EXPECTATION_SCHEMA,
        "expectation_id": "expectation.hostess_boundary_descriptor.synthetic.001",
        "generated_at": now,
        "expectation_status": "ready_for_future_hostess_boundary_descriptor" if fail_count == 0 else "blocked",
        "source_manifold_response_handoff_package": source_manifold_response_handoff_package,
        "expectation_scope": expectation_scope,
        "authority": authority,
        "expected_hostess_boundary_descriptor": expected_hostess_boundary_descriptor,
        "manifold_acceptance_gate": manifold_acceptance_gate,
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
            "The Hostess boundary descriptor expectation is descriptor evidence only; it does not touch Manifold, touch Hostess, create a Hostess route, create Manifold accepted state, record operator approval, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future source of truth, response decision, accepted-state, audit, and Hostess route enablement authority for this sidecar mesh lane.",
            "Hostess remains a future operator-recovery and read-only status consumer after Manifold accepted state or explicit operator request; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "manifold_response_slice_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response-handoff", required=True, help="Generated Manifold response handoff package fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output Hostess boundary descriptor expectation path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        expectation = build_expectation(Path(args.response_handoff), repo_root, args.now)
        write_json(Path(args.output), expectation)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_hostess_boundary_descriptor_expectation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": expectation["expectation_status"], "check_count": expectation["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
