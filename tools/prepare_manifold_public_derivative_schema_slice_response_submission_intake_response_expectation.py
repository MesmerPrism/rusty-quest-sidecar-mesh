#!/usr/bin/env python3
"""Generate a descriptor-only expectation for a future Manifold submission intake response."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


EXPECTATION_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1"
SUBMISSION_ENVELOPE_EXPECTATION_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_envelope_expectation.v1"


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


def build_expectation(envelope_expectation_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    envelope_expectation = load_json(envelope_expectation_path)
    envelope_result = validate_repo.validate_json_file(envelope_expectation_path)

    source_expectation = {
        "path": relative_output_path(envelope_expectation_path, repo_root),
        "schema": envelope_expectation.get("schema"),
        "expectation_id": envelope_expectation.get("expectation_id"),
        "expectation_status": envelope_expectation.get("expectation_status"),
        "next_gate": envelope_expectation.get("next_gate"),
    }
    expectation_scope = {
        "expectation_class": "manifold_submission_intake_response_expectation",
        "source_mode": "synthetic_fixture",
        "operator_decision_record_status": "not_created",
        "operator_decision_status": "not_recorded",
        "submission_envelope_status": "not_created",
        "manifold_submission_status": "not_submitted",
        "manifold_repo_touch_status": "not_touched",
        "manifold_intake_response_status": "not_created",
        "manifold_decision_status": "not_created",
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
        "submission_envelope_owner_after_operator_decision": "operator",
        "submission_request_owner": "operator",
        "intake_response_owner": "rusty.manifold",
        "submission_acceptance_owner": "rusty.manifold",
        "handoff_acceptance_owner": "rusty.manifold",
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
    expected_response = {
        "response_status": "not_created",
        "response_class": "manifold_owned_submission_intake_response",
        "allowed_response_owner": "rusty.manifold",
        "allowed_decisions": [
            "received_for_review",
            "request_submission_revision",
            "reject_submission_envelope",
        ],
        "required_fields": [
            "response_id",
            "submission_envelope_id",
            "source_handoff_package_id",
            "decision",
            "decision_owner",
            "created_at",
            "reviewed_artifacts",
            "validation_report_ref",
            "audit_record_ref",
            "source_chain_digest_status",
            "redaction_review_status",
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
            "sidecar_created_state",
        ],
        "default_without_response": "hold",
        "creates_accepted_state": False,
        "creates_hostess_input": False,
    }
    manifold_after_response = {
        "response_status": "not_created",
        "submission_status": "not_submitted",
        "acceptance_status": "not_accepted",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "validation_report_status": "not_created",
        "response_owner": "rusty.manifold",
        "acceptance_owner": "rusty.manifold",
        "accepted_state_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "requires_operator_submission_envelope": True,
        "requires_redaction_review": True,
        "requires_source_chain_digest": True,
        "sidecar_can_create_response": False,
        "sidecar_can_accept": False,
        "sidecar_can_create_state": False,
        "sidecar_can_create_audit": False,
    }
    hostess_after_response = {
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
        "gate_result": "intake_response_expectation_without_hostess_input",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.py --envelope-expectation fixtures/valid/manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json --now 2026-06-05T01:28:00Z --output fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owned_submission_intake_response",
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

    required_decisions = {
        "received_for_review",
        "request_submission_revision",
        "reject_submission_envelope",
    }
    required_fields = {
        "response_id",
        "submission_envelope_id",
        "source_handoff_package_id",
        "decision",
        "decision_owner",
        "created_at",
        "reviewed_artifacts",
        "validation_report_ref",
        "audit_record_ref",
        "source_chain_digest_status",
        "redaction_review_status",
        "hostess_boundary_intent",
        "reason",
    }
    required_absences = {
        "endpoint_values",
        "pairing_material",
        "adb_targets",
        "commands",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "hostess_direct_input",
        "sidecar_created_state",
    }

    checks = [
        check(
            "submission_intake_response_expectation.source_envelope_expectation_ready",
            envelope_result.ok
            and envelope_expectation.get("schema") == SUBMISSION_ENVELOPE_EXPECTATION_SCHEMA
            and envelope_expectation.get("expectation_status") == "ready_for_manifold_submission_envelope"
            and envelope_expectation.get("next_gate") == "operator_submission_envelope_or_manifold_repo_public_derivative_schema_slice_response",
            {
                "schema": envelope_expectation.get("schema"),
                "expectation_status": envelope_expectation.get("expectation_status"),
                "next_gate": envelope_expectation.get("next_gate"),
            },
            {
                "schema": SUBMISSION_ENVELOPE_EXPECTATION_SCHEMA,
                "expectation_status": "ready_for_manifold_submission_envelope",
                "next_gate": "operator_submission_envelope_or_manifold_repo_public_derivative_schema_slice_response",
            },
            relative_output_path(envelope_expectation_path, repo_root),
        ),
        check(
            "submission_intake_response_expectation.no_submission_response_state_or_hostess_input",
            expectation_scope["operator_decision_record_status"] == "not_created"
            and expectation_scope["operator_decision_status"] == "not_recorded"
            and expectation_scope["submission_envelope_status"] == "not_created"
            and expectation_scope["manifold_submission_status"] == "not_submitted"
            and expectation_scope["manifold_repo_touch_status"] == "not_touched"
            and expectation_scope["manifold_intake_response_status"] == "not_created"
            and expectation_scope["manifold_decision_status"] == "not_created"
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
                "submission_envelope_status": "not_created",
                "manifold_submission_status": "not_submitted",
                "manifold_repo_touch_status": "not_touched",
                "manifold_intake_response_status": "not_created",
                "manifold_decision_status": "not_created",
                "manifold_accepted_state_status": "not_created",
                "manifold_audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
            },
            "expectation creates no submission envelope, Manifold response/state/audit, Hostess input, ADB, or command action",
        ),
        check(
            "submission_intake_response_expectation.authority",
            authority["submission_envelope_owner_after_operator_decision"] == "operator"
            and authority["submission_request_owner"] == "operator"
            and authority["intake_response_owner"] == "rusty.manifold"
            and authority["submission_acceptance_owner"] == "rusty.manifold"
            and authority["handoff_acceptance_owner"] == "rusty.manifold"
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
                "submission_envelope_owner_after_operator_decision": "operator",
                "submission_request_owner": "operator",
                "intake_response_owner": "rusty.manifold",
                "submission_acceptance_owner": "rusty.manifold",
                "handoff_acceptance_owner": "rusty.manifold",
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
            "Manifold owns the future intake response while operator and Hostess boundaries stay explicit",
        ),
        check(
            "submission_intake_response_expectation.response_shape",
            expected_response["response_status"] == "not_created"
            and expected_response["allowed_response_owner"] == "rusty.manifold"
            and required_decisions <= set(expected_response["allowed_decisions"])
            and required_fields <= set(expected_response["required_fields"])
            and required_absences <= set(expected_response["must_not_contain"])
            and expected_response["default_without_response"] == "hold"
            and expected_response["creates_accepted_state"] is False
            and expected_response["creates_hostess_input"] is False,
            expected_response,
            {
                "response_status": "not_created",
                "allowed_response_owner": "rusty.manifold",
                "allowed_decisions": sorted(required_decisions),
                "required_fields": sorted(required_fields),
                "must_not_contain": sorted(required_absences),
                "default_without_response": "hold",
                "creates_accepted_state": False,
                "creates_hostess_input": False,
            },
            "future Manifold intake response shape is explicit without creating the response",
        ),
        check(
            "submission_intake_response_expectation.manifold_after_response",
            manifold_after_response["response_status"] == "not_created"
            and manifold_after_response["submission_status"] == "not_submitted"
            and manifold_after_response["acceptance_status"] == "not_accepted"
            and manifold_after_response["accepted_state_status"] == "not_created"
            and manifold_after_response["audit_record_status"] == "not_created"
            and manifold_after_response["validation_report_status"] == "not_created"
            and manifold_after_response["response_owner"] == "rusty.manifold"
            and manifold_after_response["acceptance_owner"] == "rusty.manifold"
            and manifold_after_response["accepted_state_owner"] == "rusty.manifold"
            and manifold_after_response["audit_owner"] == "rusty.manifold.audit"
            and manifold_after_response["requires_operator_submission_envelope"] is True
            and manifold_after_response["sidecar_can_create_response"] is False
            and manifold_after_response["sidecar_can_accept"] is False
            and manifold_after_response["sidecar_can_create_state"] is False
            and manifold_after_response["sidecar_can_create_audit"] is False,
            manifold_after_response,
            {
                "response_status": "not_created",
                "submission_status": "not_submitted",
                "acceptance_status": "not_accepted",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "validation_report_status": "not_created",
                "response_owner": "rusty.manifold",
                "acceptance_owner": "rusty.manifold",
                "accepted_state_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "requires_operator_submission_envelope": True,
                "sidecar_can_create_response": False,
                "sidecar_can_accept": False,
                "sidecar_can_create_state": False,
                "sidecar_can_create_audit": False,
            },
            "Manifold response, acceptance, accepted state, audit, and validation report stay future Manifold-owned artifacts",
        ),
        check(
            "submission_intake_response_expectation.hostess_after_response",
            hostess_after_response["status"] == "future_lane_not_requested"
            and hostess_after_response["route_status"] == "not_created"
            and hostess_after_response["input_status"] == "not_created"
            and hostess_after_response["device_action_authority"] == "not_in_sidecar"
            and hostess_after_response["future_route_owner"] == "rusty.hostess"
            and hostess_after_response["boundary_descriptor_owner"] == "rusty.manifold"
            and hostess_after_response["consumes_only"] == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and hostess_after_response["sidecar_direct_input_allowed"] is False
            and hostess_after_response["requires_manifold_accepted_state"] is True
            and hostess_after_response["requires_explicit_operator_request"] is True,
            hostess_after_response,
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
            "submission_intake_response_expectation.privacy_and_validation",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owned_submission_intake_response"
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
                "future_manifold_gate": "manifold_repo_owned_submission_intake_response",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "submission intake response expectation remains public-safe descriptor evidence",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": EXPECTATION_SCHEMA,
        "expectation_id": "expectation.manifold_public_derivative_schema_slice_response_submission_intake_response.synthetic.001",
        "generated_at": now,
        "expectation_status": "ready_for_manifold_submission_intake_response" if fail_count == 0 else "blocked",
        "source_submission_envelope_expectation": source_expectation,
        "expectation_scope": expectation_scope,
        "authority": authority,
        "expected_manifold_intake_response": expected_response,
        "manifold_acceptance_after_response": manifold_after_response,
        "hostess_boundary_after_response": hostess_after_response,
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
            "Submission intake response expectation is descriptor evidence only; it does not create a submission envelope or Manifold response.",
            "The future intake response is owned by Manifold and must not contain endpoints, pairing material, ADB targets, commands, raw logs, visual captures, private device identifiers, sidecar-created state, or direct Hostess input.",
            "Manifold remains the future submission acceptance, response, decision, route, command/session/audit, rollback, validation report, and accepted-state authority.",
            "Hostess remains a future route owner after Manifold accepted state or a separate explicit operator request descriptor; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "operator_submission_envelope_or_manifold_repo_submission_intake_response",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--envelope-expectation", required=True, help="Generated submission envelope expectation fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output submission intake response expectation path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        expectation = build_expectation(Path(args.envelope_expectation), repo_root, args.now)
        write_json(Path(args.output), expectation)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": expectation["expectation_status"], "check_count": expectation["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
