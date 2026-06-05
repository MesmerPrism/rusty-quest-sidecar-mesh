#!/usr/bin/env python3
"""Generate a descriptor-only expectation for a future operator decision record."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


EXPECTATION_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.v1"
REQUEST_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1"


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


def build_expectation(decision_request_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    decision_request = load_json(decision_request_path)
    request_result = validate_repo.validate_json_file(decision_request_path)

    source_request = {
        "path": relative_output_path(decision_request_path, repo_root),
        "schema": decision_request.get("schema"),
        "request_id": decision_request.get("request_id"),
        "request_status": decision_request.get("request_status"),
        "next_gate": decision_request.get("next_gate"),
    }
    expectation_scope = {
        "expectation_class": "operator_decision_record_expectation",
        "source_mode": "synthetic_fixture",
        "operator_decision_record_status": "not_created",
        "operator_decision_status": "not_recorded",
        "manifold_submission_status": "not_submitted",
        "manifold_repo_touch_status": "not_touched",
        "manifold_response_status": "not_created",
        "manifold_accepted_state_status": "not_created",
        "manifold_audit_record_status": "not_created",
        "hostess_route_status": "not_created",
        "hostess_input_status": "not_created",
        "live_evidence_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "operator_decision_record_owner": "operator",
        "submission_request_owner": "operator",
        "handoff_acceptance_owner": "rusty.manifold",
        "response_owner": "rusty.manifold",
        "decision_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "hostess_boundary_descriptor_owner": "rusty.manifold",
        "future_hostess_route_owner": "rusty.hostess",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    expected_record = {
        "record_status": "not_created",
        "record_class": "operator_owned_sidecar_handoff_decision",
        "allowed_record_owner": "operator",
        "allowed_decisions": [
            "submit_to_manifold_review",
            "hold_for_revision",
            "reject_sidecar_handoff",
        ],
        "required_fields": [
            "decision_record_id",
            "source_request_id",
            "source_handoff_package_id",
            "decision",
            "decision_owner",
            "created_at",
            "reviewed_artifacts",
            "redaction_review_status",
            "source_chain_digest_status",
            "manifold_submission_intent",
            "hostess_boundary_intent",
            "reason",
        ],
        "must_not_contain": [
            "endpoint_values",
            "pairing_material",
            "adb_targets",
            "commands",
            "raw_logs",
            "visual_captures",
            "private_device_ids",
            "hostess_direct_input",
        ],
        "default_without_record": "hold",
        "creates_manifold_state": False,
        "creates_hostess_input": False,
    }
    manifold_after_decision = {
        "submission_status": "not_submitted",
        "submit_decision_value": "submit_to_manifold_review",
        "submission_owner_after_operator_decision": "operator",
        "acceptance_owner": "rusty.manifold",
        "response_owner": "rusty.manifold",
        "accepted_state_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "requires_valid_operator_decision_record": True,
        "requires_source_handoff_package": True,
        "requires_redaction_review": True,
        "requires_source_chain_digest": True,
        "sidecar_can_submit_directly": False,
        "sidecar_can_accept": False,
        "sidecar_can_create_state": False,
    }
    hostess_after_decision = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "input_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "future_route_owner": "rusty.hostess",
        "boundary_descriptor_owner": "rusty.manifold",
        "consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "gate_result": "record_expectation_without_hostess_input",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.py --decision-request fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json --now 2026-06-05T01:12:00Z --output fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "operator_decision_record_then_manifold_repo_owned_response",
        "future_hostess_gate": "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor",
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

    required_decisions = {"submit_to_manifold_review", "hold_for_revision", "reject_sidecar_handoff"}
    required_fields = {
        "decision_record_id",
        "source_request_id",
        "source_handoff_package_id",
        "decision",
        "decision_owner",
        "created_at",
        "reviewed_artifacts",
        "redaction_review_status",
        "source_chain_digest_status",
        "manifold_submission_intent",
        "hostess_boundary_intent",
        "reason",
    }

    checks = [
        check(
            "operator_decision_record_expectation.source_request_ready",
            request_result.ok
            and decision_request.get("schema") == REQUEST_SCHEMA
            and decision_request.get("request_status") == "operator_decision_required"
            and decision_request.get("next_gate") == "operator_decision_or_manifold_repo_public_derivative_schema_slice_response",
            {
                "schema": decision_request.get("schema"),
                "request_status": decision_request.get("request_status"),
                "next_gate": decision_request.get("next_gate"),
            },
            {
                "schema": REQUEST_SCHEMA,
                "request_status": "operator_decision_required",
                "next_gate": "operator_decision_or_manifold_repo_public_derivative_schema_slice_response",
            },
            relative_output_path(decision_request_path, repo_root),
        ),
        check(
            "operator_decision_record_expectation.no_record_submission_or_hostess_input",
            expectation_scope["operator_decision_record_status"] == "not_created"
            and expectation_scope["operator_decision_status"] == "not_recorded"
            and expectation_scope["manifold_submission_status"] == "not_submitted"
            and expectation_scope["manifold_repo_touch_status"] == "not_touched"
            and expectation_scope["manifold_response_status"] == "not_created"
            and expectation_scope["manifold_accepted_state_status"] == "not_created"
            and expectation_scope["manifold_audit_record_status"] == "not_created"
            and expectation_scope["hostess_route_status"] == "not_created"
            and expectation_scope["hostess_input_status"] == "not_created"
            and expectation_scope["adb_status"] == "not_used"
            and expectation_scope["command_status"] == "no_commands",
            expectation_scope,
            {
                "operator_decision_record_status": "not_created",
                "operator_decision_status": "not_recorded",
                "manifold_submission_status": "not_submitted",
                "manifold_repo_touch_status": "not_touched",
                "manifold_response_status": "not_created",
                "manifold_accepted_state_status": "not_created",
                "manifold_audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
            },
            "expectation creates no decision record, Manifold submission/state/audit, Hostess input, ADB, or command action",
        ),
        check(
            "operator_decision_record_expectation.authority",
            authority["operator_decision_record_owner"] == "operator"
            and authority["submission_request_owner"] == "operator"
            and authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["response_owner"] == "rusty.manifold"
            and authority["decision_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["hostess_boundary_descriptor_owner"] == "rusty.manifold"
            and authority["future_hostess_route_owner"] == "rusty.hostess"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer",
            authority,
            {
                "operator_decision_record_owner": "operator",
                "submission_request_owner": "operator",
                "handoff_acceptance_owner": "rusty.manifold",
                "response_owner": "rusty.manifold",
                "decision_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_boundary_descriptor_owner": "rusty.manifold",
                "future_hostess_route_owner": "rusty.hostess",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
            },
            "operator owns the future decision record while Manifold and Hostess authority stay explicit",
        ),
        check(
            "operator_decision_record_expectation.record_shape",
            expected_record["record_status"] == "not_created"
            and expected_record["allowed_record_owner"] == "operator"
            and required_decisions <= set(expected_record["allowed_decisions"])
            and required_fields <= set(expected_record["required_fields"])
            and expected_record["default_without_record"] == "hold"
            and expected_record["creates_manifold_state"] is False
            and expected_record["creates_hostess_input"] is False
            and {"endpoint_values", "adb_targets", "commands", "hostess_direct_input"} <= set(expected_record["must_not_contain"]),
            expected_record,
            {
                "record_status": "not_created",
                "allowed_record_owner": "operator",
                "allowed_decisions": sorted(required_decisions),
                "required_fields": sorted(required_fields),
                "default_without_record": "hold",
                "creates_manifold_state": False,
                "creates_hostess_input": False,
                "must_not_contain": ["endpoint_values", "adb_targets", "commands", "hostess_direct_input"],
            },
            "future operator decision record shape is explicit without creating the record",
        ),
        check(
            "operator_decision_record_expectation.manifold_submission_after_decision",
            manifold_after_decision["submission_status"] == "not_submitted"
            and manifold_after_decision["submit_decision_value"] == "submit_to_manifold_review"
            and manifold_after_decision["submission_owner_after_operator_decision"] == "operator"
            and manifold_after_decision["acceptance_owner"] == "rusty.manifold"
            and manifold_after_decision["response_owner"] == "rusty.manifold"
            and manifold_after_decision["accepted_state_owner"] == "rusty.manifold"
            and manifold_after_decision["audit_owner"] == "rusty.manifold.audit"
            and manifold_after_decision["requires_valid_operator_decision_record"] is True
            and manifold_after_decision["sidecar_can_submit_directly"] is False
            and manifold_after_decision["sidecar_can_accept"] is False
            and manifold_after_decision["sidecar_can_create_state"] is False,
            manifold_after_decision,
            {
                "submission_status": "not_submitted",
                "submit_decision_value": "submit_to_manifold_review",
                "submission_owner_after_operator_decision": "operator",
                "acceptance_owner": "rusty.manifold",
                "response_owner": "rusty.manifold",
                "accepted_state_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "requires_valid_operator_decision_record": True,
                "sidecar_can_submit_directly": False,
                "sidecar_can_accept": False,
                "sidecar_can_create_state": False,
            },
            "Manifold submission remains future operator-owned request and Manifold-owned acceptance",
        ),
        check(
            "operator_decision_record_expectation.hostess_after_decision",
            hostess_after_decision["status"] == "future_lane_not_requested"
            and hostess_after_decision["route_status"] == "not_created"
            and hostess_after_decision["input_status"] == "not_created"
            and hostess_after_decision["device_action_authority"] == "not_in_sidecar"
            and hostess_after_decision["future_route_owner"] == "rusty.hostess"
            and hostess_after_decision["boundary_descriptor_owner"] == "rusty.manifold"
            and hostess_after_decision["consumes_only"] == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and hostess_after_decision["sidecar_direct_input_allowed"] is False
            and hostess_after_decision["requires_manifold_accepted_state"] is True
            and hostess_after_decision["requires_explicit_operator_request"] is True,
            hostess_after_decision,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "input_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "future_route_owner": "rusty.hostess",
                "boundary_descriptor_owner": "rusty.manifold",
                "consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
            },
            "Hostess remains a future downstream route owner without direct sidecar input",
        ),
        check(
            "operator_decision_record_expectation.privacy_and_validation",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "operator_decision_record_then_manifold_repo_owned_response"
            and validation_evidence["future_hostess_gate"] == "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor"
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
                "future_manifold_gate": "operator_decision_record_then_manifold_repo_owned_response",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "operator decision record expectation remains public-safe descriptor evidence",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": EXPECTATION_SCHEMA,
        "expectation_id": "expectation.manifold_public_derivative_schema_slice_response_operator_decision_record.synthetic.001",
        "generated_at": now,
        "expectation_status": "ready_for_operator_decision_record" if fail_count == 0 else "blocked",
        "source_operator_decision_request": source_request,
        "expectation_scope": expectation_scope,
        "authority": authority,
        "expected_operator_decision_record": expected_record,
        "manifold_submission_after_decision": manifold_after_decision,
        "hostess_boundary_after_decision": hostess_after_decision,
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
            "Operator decision record expectation is descriptor evidence only; it does not record a decision or submit the handoff package.",
            "The future operator decision record is owned by the operator and must not contain endpoints, pairing material, ADB targets, commands, raw logs, visual captures, private device identifiers, or direct Hostess input.",
            "Manifold remains the future submission acceptance, response, decision, route, command/session/audit, rollback, validation report, and accepted-state authority.",
            "Hostess remains a future route owner after Manifold accepted state or a separate explicit operator request descriptor; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "operator_decision_record_or_manifold_repo_public_derivative_schema_slice_response",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--decision-request", required=True, help="Generated operator decision request fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output operator decision record expectation path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        expectation = build_expectation(Path(args.decision_request), repo_root, args.now)
        write_json(Path(args.output), expectation)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": expectation["expectation_status"], "check_count": expectation["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
