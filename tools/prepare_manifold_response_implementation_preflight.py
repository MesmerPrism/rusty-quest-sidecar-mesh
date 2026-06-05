#!/usr/bin/env python3
"""Generate a sidecar-owned preflight for a future Manifold response slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


PREFLIGHT_SCHEMA = "rusty.quest.sidecar.manifold_response_implementation_preflight.v1"
EXPECTATION_SCHEMA = "rusty.quest.sidecar.manifold_route_design_response_expectation.v1"


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


def build_preflight(response_expectation_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    response_expectation = load_json(response_expectation_path)
    expectation_result = validate_repo.validate_json_file(response_expectation_path)

    source_manifold_route_design_response_expectation = {
        "path": relative_output_path(response_expectation_path, repo_root),
        "schema": response_expectation.get("schema"),
        "expectation_id": response_expectation.get("expectation_id"),
        "expectation_status": response_expectation.get("expectation_status"),
        "next_gate": response_expectation.get("next_gate"),
    }
    implementation_preflight_scope = {
        "preflight_class": "manifold_repo_response_slice_preflight",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    authority = {
        "preflight_owner": "rusty.quest.sidecar_mesh",
        "implementation_plan_owner": "rusty.manifold",
        "response_owner": "rusty.manifold",
        "decision_owner": "rusty.manifold",
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
    manifold_repo_slice_requirements = {
        "slice_class": "manifold_owned_sidecar_peer_status_response_slice",
        "target_repo": "rusty.manifold",
        "implementation_status": "not_created_by_sidecar",
        "required_manifold_owned_artifacts": [
            {
                "artifact_id": "artifact.sidecar_peer_status_design_response_schema",
                "artifact_kind": "schema",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_response.required_fields",
            },
            {
                "artifact_id": "artifact.sidecar_peer_status_route_handler",
                "artifact_kind": "route_handler",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "source_manifold_route_design_review_request",
            },
            {
                "artifact_id": "artifact.sidecar_peer_status_decision_event_fixture",
                "artifact_kind": "decision_event_fixture",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_response.allowed_decisions",
            },
            {
                "artifact_id": "artifact.sidecar_peer_status_accepted_state_fixture",
                "artifact_kind": "accepted_state_fixture",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_response.accepted_state_policy",
            },
            {
                "artifact_id": "artifact.sidecar_peer_status_audit_fixture",
                "artifact_kind": "audit_fixture",
                "owner": "rusty.manifold.audit",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_response.required_audit_terms",
            },
            {
                "artifact_id": "artifact.sidecar_peer_status_hostess_boundary_descriptor",
                "artifact_kind": "hostess_boundary_descriptor",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "hostess_response_gate",
            },
        ],
        "required_validation_slots": [
            "slot.manifold_response_schema_contract",
            "slot.sidecar_design_response_valid_fixture",
            "slot.sidecar_design_response_damaged_fixture",
            "slot.manifold_route_unit_tests",
            "slot.manifold_audit_fixture",
            "slot.hostess_boundary_descriptor_check",
            "slot.privacy_redaction_rejection_check",
        ],
        "required_response_decisions": [
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
            "high_rate_payload_rejected",
        ],
        "required_route_boundaries": {
            "input_payload_class": "low_rate_advisory_status",
            "allows_endpoint_values": False,
            "allows_commands": False,
            "allows_adb": False,
            "allows_high_rate_payloads": False,
            "allows_sidecar_direct_hostess_input": False,
        },
        "rollback_policy": "manifold_owned_disable_route_or_reject_source",
    }
    hostess_boundary_preflight = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_action_class": "operator_recovery_request_descriptor",
        "preflight_result": "hostess_deferred_until_manifold_acceptance",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_manifold_response_implementation_preflight.py --response-expectation fixtures/valid/manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures/valid/manifold-response-implementation-preflight.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_response_slice_implementation_and_audit",
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

    required_artifact_kinds = {
        "schema",
        "route_handler",
        "decision_event_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "hostess_boundary_descriptor",
    }
    required_validation_slots = {
        "slot.manifold_response_schema_contract",
        "slot.sidecar_design_response_valid_fixture",
        "slot.sidecar_design_response_damaged_fixture",
        "slot.manifold_route_unit_tests",
        "slot.manifold_audit_fixture",
        "slot.hostess_boundary_descriptor_check",
        "slot.privacy_redaction_rejection_check",
    }
    required_rejection_terms = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "high_rate_payload_rejected",
    }

    artifacts = manifold_repo_slice_requirements["required_manifold_owned_artifacts"]
    route_boundaries = manifold_repo_slice_requirements["required_route_boundaries"]
    checks = [
        check(
            "manifold_response_preflight.source_expectation_ready",
            expectation_result.ok
            and response_expectation.get("schema") == EXPECTATION_SCHEMA
            and response_expectation.get("expectation_status") == "ready_for_manifold_owned_response"
            and response_expectation.get("next_gate") == "manifold_owned_response_or_operator_decision",
            {
                "schema": response_expectation.get("schema"),
                "expectation_status": response_expectation.get("expectation_status"),
                "next_gate": response_expectation.get("next_gate"),
            },
            {
                "schema": EXPECTATION_SCHEMA,
                "expectation_status": "ready_for_manifold_owned_response",
                "next_gate": "manifold_owned_response_or_operator_decision",
            },
            relative_output_path(response_expectation_path, repo_root),
        ),
        check(
            "manifold_response_preflight.no_repo_response_route_or_state",
            implementation_preflight_scope["repo_touch_status"] == "not_touched"
            and implementation_preflight_scope["branch_status"] == "not_created"
            and implementation_preflight_scope["response_status"] == "not_created"
            and implementation_preflight_scope["decision_status"] == "not_decided"
            and implementation_preflight_scope["route_status"] == "not_created"
            and implementation_preflight_scope["accepted_state_status"] == "not_created"
            and implementation_preflight_scope["audit_record_status"] == "not_created"
            and implementation_preflight_scope["hostess_route_status"] == "not_created"
            and implementation_preflight_scope["live_evidence_status"] == "not_included",
            implementation_preflight_scope,
            {
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "live_evidence_status": "not_included",
            },
            "preflight does not touch Manifold, create branch, response, decision, route, state, audit, Hostess route, or live evidence",
        ),
        check(
            "manifold_response_preflight.manifold_authority",
            authority["implementation_plan_owner"] == "rusty.manifold"
            and authority["response_owner"] == "rusty.manifold"
            and authority["decision_owner"] == "rusty.manifold"
            and authority["route_implementation_owner"] == "rusty.manifold"
            and authority["request_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["rollback_owner"] == "rusty.manifold"
            and authority["sidecar_role"] == "observer_proposer",
            authority,
            {
                "implementation_plan_owner": "rusty.manifold",
                "response_owner": "rusty.manifold",
                "decision_owner": "rusty.manifold",
                "route_implementation_owner": "rusty.manifold",
                "request_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "rollback_owner": "rusty.manifold",
                "sidecar_role": "observer_proposer",
            },
            "Manifold remains implementation plan, response, decision, route, runtime, session, audit, state, and rollback owner",
        ),
        check(
            "manifold_response_preflight.artifacts_manifold_owned_not_created",
            bool(artifacts)
            and required_artifact_kinds <= {artifact["artifact_kind"] for artifact in artifacts}
            and all(artifact["status"] == "not_created_by_sidecar" for artifact in artifacts)
            and all(
                artifact["owner"] in {"rusty.manifold", "rusty.manifold.audit"}
                for artifact in artifacts
            ),
            {
                "artifact_kinds": sorted({artifact["artifact_kind"] for artifact in artifacts}),
                "owners": sorted({artifact["owner"] for artifact in artifacts}),
                "statuses": sorted({artifact["status"] for artifact in artifacts}),
                "artifact_count": len(artifacts),
            },
            {
                "artifact_kinds": sorted(required_artifact_kinds),
                "owners": ["rusty.manifold", "rusty.manifold.audit"],
                "status": "not_created_by_sidecar",
                "artifact_count": 6,
            },
            "all required implementation artifacts are Manifold-owned and not created by the sidecar repo",
        ),
        check(
            "manifold_response_preflight.validation_and_rejection_terms",
            required_validation_slots <= set(manifold_repo_slice_requirements["required_validation_slots"])
            and set(manifold_repo_slice_requirements["required_response_decisions"])
            == {"accepted_for_manifold_slice", "revision_requested", "rejected"}
            and required_rejection_terms <= set(manifold_repo_slice_requirements["required_rejection_terms"]),
            {
                "required_validation_slots": manifold_repo_slice_requirements["required_validation_slots"],
                "required_response_decisions": manifold_repo_slice_requirements["required_response_decisions"],
                "required_rejection_terms": manifold_repo_slice_requirements["required_rejection_terms"],
            },
            {
                "required_validation_slots": sorted(required_validation_slots),
                "required_response_decisions": ["accepted_for_manifold_slice", "revision_requested", "rejected"],
                "required_rejection_terms": sorted(required_rejection_terms),
            },
            "Manifold implementation slice must include fixture, route, audit, Hostess, privacy, decision, and rejection coverage",
        ),
        check(
            "manifold_response_preflight.route_boundaries",
            route_boundaries["input_payload_class"] == "low_rate_advisory_status"
            and route_boundaries["allows_endpoint_values"] is False
            and route_boundaries["allows_commands"] is False
            and route_boundaries["allows_adb"] is False
            and route_boundaries["allows_high_rate_payloads"] is False
            and route_boundaries["allows_sidecar_direct_hostess_input"] is False
            and manifold_repo_slice_requirements["rollback_policy"] == "manifold_owned_disable_route_or_reject_source",
            {
                "required_route_boundaries": route_boundaries,
                "rollback_policy": manifold_repo_slice_requirements["rollback_policy"],
            },
            {
                "input_payload_class": "low_rate_advisory_status",
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "allows_sidecar_direct_hostess_input": False,
                "rollback_policy": "manifold_owned_disable_route_or_reject_source",
            },
            "Manifold route preflight remains low-rate advisory input only and rejects sidecar device-action drift",
        ),
        check(
            "manifold_response_preflight.hostess_deferred",
            hostess_boundary_preflight["status"] == "future_lane_not_requested"
            and hostess_boundary_preflight["route_status"] == "not_created"
            and hostess_boundary_preflight["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary_preflight["consumes_only"] == "manifold_accepted_state_or_operator_request_descriptor"
            and hostess_boundary_preflight["sidecar_direct_input_allowed"] is False
            and hostess_boundary_preflight["requires_manifold_accepted_state"] is True
            and hostess_boundary_preflight["requires_explicit_operator_request"] is True
            and hostess_boundary_preflight["preflight_result"] == "hostess_deferred_until_manifold_acceptance",
            hostess_boundary_preflight,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "preflight_result": "hostess_deferred_until_manifold_acceptance",
            },
            "Hostess remains deferred until Manifold accepted state or explicit operator request exists",
        ),
        check(
            "manifold_response_preflight.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_response_slice_implementation_and_audit"
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
                "future_manifold_gate": "manifold_repo_owns_response_slice_implementation_and_audit",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "preflight remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": PREFLIGHT_SCHEMA,
        "preflight_id": "preflight.manifold_response_implementation.synthetic.001",
        "generated_at": now,
        "preflight_status": "ready_for_manifold_repo_slice_planning" if fail_count == 0 else "blocked",
        "source_manifold_route_design_response_expectation": source_manifold_route_design_response_expectation,
        "implementation_preflight_scope": implementation_preflight_scope,
        "authority": authority,
        "manifold_repo_slice_requirements": manifold_repo_slice_requirements,
        "hostess_boundary_preflight": hostess_boundary_preflight,
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
            "The Manifold response implementation preflight is descriptor evidence only; it does not touch the Manifold repo, create a branch, create a response, decide the review, create schemas, create routes, create accepted state, create audit records, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future implementation plan, response, decision, route implementation, request acceptance, command/session/audit, revision, lease, rollback, and accepted-state authority.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "manifold_repo_response_slice_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response-expectation", required=True, help="Manifold route design response expectation fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output preflight path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        preflight = build_preflight(Path(args.response_expectation), repo_root, args.now)
        write_json(Path(args.output), preflight)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_response_implementation_preflight failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": preflight["preflight_status"], "check_count": preflight["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
