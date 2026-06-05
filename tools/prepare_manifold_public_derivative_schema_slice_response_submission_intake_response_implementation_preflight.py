#!/usr/bin/env python3
"""Generate a preflight for a future Manifold-owned submission intake response implementation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


PREFLIGHT_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.v1"
EXPECTATION_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1"


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


def build_preflight(expectation_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    expectation = load_json(expectation_path)
    expectation_result = validate_repo.validate_json_file(expectation_path)

    source_expectation = {
        "path": relative_output_path(expectation_path, repo_root),
        "schema": expectation.get("schema"),
        "expectation_id": expectation.get("expectation_id"),
        "expectation_status": expectation.get("expectation_status"),
        "next_gate": expectation.get("next_gate"),
    }
    implementation_preflight_scope = {
        "preflight_class": "manifold_repo_submission_intake_response_preflight",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "implementation_plan_status": "not_created",
        "submission_envelope_status": "not_created",
        "submission_status": "not_submitted",
        "intake_response_status": "not_created",
        "decision_status": "not_decided",
        "response_schema_status": "not_created",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "validation_report_status": "not_created",
        "public_derivative_status": "not_created",
        "hostess_boundary_descriptor_status": "not_created",
        "hostess_route_status": "not_created",
        "hostess_input_status": "not_created",
        "live_evidence_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    authority = {
        "preflight_owner": "rusty.quest.sidecar_mesh",
        "submission_envelope_owner": "operator",
        "submission_request_owner": "operator",
        "intake_response_implementation_owner": "rusty.manifold",
        "intake_response_owner": "rusty.manifold",
        "submission_acceptance_owner": "rusty.manifold",
        "decision_owner": "rusty.manifold",
        "response_schema_owner": "rusty.manifold",
        "route_implementation_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "validation_report_owner": "rusty.manifold",
        "rollback_owner": "rusty.manifold",
        "source_chain_digest_owner": "rusty.manifold",
        "redaction_review_input_owner": "operator",
        "redaction_review_validation_owner": "rusty.manifold",
        "hostess_boundary_descriptor_owner": "rusty.manifold",
        "future_hostess_route_owner": "rusty.hostess",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    requirements = {
        "slice_class": "manifold_owned_submission_intake_response",
        "target_repo": "rusty.manifold",
        "implementation_status": "not_created_by_sidecar",
        "required_manifold_owned_artifacts": [
            {
                "artifact_id": "artifact.submission_intake_response_schema",
                "artifact_kind": "response_schema",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_intake_response.required_fields",
            },
            {
                "artifact_id": "artifact.submission_intake_response_route_handler",
                "artifact_kind": "route_handler",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_intake_response.allowed_decisions",
            },
            {
                "artifact_id": "artifact.submission_intake_decision_event_schema",
                "artifact_kind": "decision_event_schema",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_intake_response.decision",
            },
            {
                "artifact_id": "artifact.submission_envelope_schema_binding",
                "artifact_kind": "submission_envelope_schema_binding",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "source_submission_envelope_expectation",
            },
            {
                "artifact_id": "artifact.submission_intake_accepted_state_candidate_fixture",
                "artifact_kind": "accepted_state_candidate_fixture",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "manifold_acceptance_after_response.accepted_state_status",
            },
            {
                "artifact_id": "artifact.submission_intake_audit_fixture",
                "artifact_kind": "audit_fixture",
                "owner": "rusty.manifold.audit",
                "status": "not_created_by_sidecar",
                "evidence_source": "manifold_acceptance_after_response.audit_record_status",
            },
            {
                "artifact_id": "artifact.submission_intake_validation_report_fixture",
                "artifact_kind": "validation_report_fixture",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "manifold_acceptance_after_response.validation_report_status",
            },
            {
                "artifact_id": "artifact.submission_intake_rejection_fixture",
                "artifact_kind": "rejection_fixture",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_intake_response.allowed_decisions",
            },
            {
                "artifact_id": "artifact.submission_intake_revision_fixture",
                "artifact_kind": "revision_fixture",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "expected_manifold_intake_response.allowed_decisions",
            },
            {
                "artifact_id": "artifact.submission_intake_hostess_boundary_descriptor",
                "artifact_kind": "hostess_boundary_descriptor",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "hostess_boundary_after_response",
            },
            {
                "artifact_id": "artifact.submission_intake_rollback_descriptor",
                "artifact_kind": "rollback_descriptor",
                "owner": "rusty.manifold",
                "status": "not_created_by_sidecar",
                "evidence_source": "validation_evidence.future_manifold_gate",
            },
        ],
        "required_validation_slots": [
            "slot.submission_intake_response_expectation_contract",
            "slot.submission_intake_response_schema_contract",
            "slot.submission_intake_received_for_review_fixture",
            "slot.submission_intake_revision_request_fixture",
            "slot.submission_intake_rejection_fixture",
            "slot.submission_intake_audit_fixture",
            "slot.submission_intake_validation_report_fixture",
            "slot.source_chain_digest_check",
            "slot.redaction_review_status_check",
            "slot.hostess_boundary_descriptor_check",
            "slot.no_private_endpoint_or_command_content",
            "slot.sidecar_non_authority_check",
        ],
        "required_response_decisions": [
            "received_for_review",
            "request_submission_revision",
            "reject_submission_envelope",
        ],
        "required_rejection_terms": [
            "missing_operator_submission_envelope",
            "invalid_submission_envelope",
            "source_chain_incomplete",
            "redaction_incomplete",
            "endpoint_values_rejected",
            "commands_rejected",
            "adb_rejected",
            "raw_logs_rejected",
            "visual_captures_rejected",
            "private_device_ids_rejected",
            "hostess_direct_action_rejected",
            "stale_handoff_package",
            "untrusted_sidecar",
        ],
        "required_revision_terms": [
            "submission_envelope_revision",
            "validation_report_revision",
            "redaction_summary_revision",
            "source_chain_digest_revision",
            "hostess_boundary_intent_revision",
            "reason_revision",
        ],
        "required_audit_terms": [
            "response_id",
            "submission_envelope_id",
            "source_handoff_package_id",
            "decision",
            "reason",
            "validation_report_ref",
            "audit_record_ref",
            "source_chain_digest_status",
            "redaction_review_status",
            "hostess_boundary_intent",
        ],
        "required_route_boundaries": {
            "input_payload_class": "low_rate_descriptor",
            "accepts_sanitized_summary_only": True,
            "requires_operator_submission_envelope": True,
            "requires_source_chain_digest": True,
            "requires_redaction_review": True,
            "allows_endpoint_values": False,
            "allows_commands": False,
            "allows_adb": False,
            "allows_raw_logs": False,
            "allows_visual_captures": False,
            "allows_private_device_ids": False,
            "allows_high_rate_payloads": False,
            "allows_sidecar_direct_hostess_input": False,
            "creates_response_by_sidecar": False,
            "creates_accepted_state_by_sidecar": False,
            "creates_audit_by_sidecar": False,
            "creates_validation_report_by_sidecar": False,
            "creates_hostess_input": False,
            "accepted_state_owner": "rusty.manifold",
            "audit_owner": "rusty.manifold.audit",
        },
        "rollback_policy": "manifold_owned_reject_submission_or_request_revision",
    }
    hostess_boundary_preflight = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "input_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "future_route_owner": "rusty.hostess",
        "boundary_descriptor_owner": "rusty.manifold",
        "consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_action_class": "operator_recovery_request_descriptor",
        "preflight_result": "hostess_deferred_until_manifold_submission_intake_acceptance",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.py --intake-response-expectation fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json --now 2026-06-05T01:36:00Z --output fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_submission_intake_response_implementation_and_audit",
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

    artifacts = requirements["required_manifold_owned_artifacts"]
    route_boundaries = requirements["required_route_boundaries"]
    required_artifact_kinds = {
        "response_schema",
        "route_handler",
        "decision_event_schema",
        "submission_envelope_schema_binding",
        "accepted_state_candidate_fixture",
        "audit_fixture",
        "validation_report_fixture",
        "rejection_fixture",
        "revision_fixture",
        "hostess_boundary_descriptor",
        "rollback_descriptor",
    }
    required_validation_slots = set(requirements["required_validation_slots"])
    required_response_decisions = {
        "received_for_review",
        "request_submission_revision",
        "reject_submission_envelope",
    }
    required_rejection_terms = set(requirements["required_rejection_terms"])
    required_revision_terms = set(requirements["required_revision_terms"])
    required_audit_terms = set(requirements["required_audit_terms"])

    checks = [
        check(
            "submission_intake_response_preflight.source_expectation_ready",
            expectation_result.ok
            and expectation.get("schema") == EXPECTATION_SCHEMA
            and expectation.get("expectation_status") == "ready_for_manifold_submission_intake_response"
            and expectation.get("next_gate") == "operator_submission_envelope_or_manifold_repo_submission_intake_response",
            {
                "schema": expectation.get("schema"),
                "expectation_status": expectation.get("expectation_status"),
                "next_gate": expectation.get("next_gate"),
            },
            {
                "schema": EXPECTATION_SCHEMA,
                "expectation_status": "ready_for_manifold_submission_intake_response",
                "next_gate": "operator_submission_envelope_or_manifold_repo_submission_intake_response",
            },
            relative_output_path(expectation_path, repo_root),
        ),
        check(
            "submission_intake_response_preflight.no_repo_response_state_audit_or_hostess_input",
            implementation_preflight_scope["repo_touch_status"] == "not_touched"
            and implementation_preflight_scope["branch_status"] == "not_created"
            and implementation_preflight_scope["implementation_plan_status"] == "not_created"
            and implementation_preflight_scope["submission_envelope_status"] == "not_created"
            and implementation_preflight_scope["submission_status"] == "not_submitted"
            and implementation_preflight_scope["intake_response_status"] == "not_created"
            and implementation_preflight_scope["decision_status"] == "not_decided"
            and implementation_preflight_scope["response_schema_status"] == "not_created"
            and implementation_preflight_scope["route_status"] == "not_created"
            and implementation_preflight_scope["accepted_state_status"] == "not_created"
            and implementation_preflight_scope["audit_record_status"] == "not_created"
            and implementation_preflight_scope["validation_report_status"] == "not_created"
            and implementation_preflight_scope["public_derivative_status"] == "not_created"
            and implementation_preflight_scope["hostess_boundary_descriptor_status"] == "not_created"
            and implementation_preflight_scope["hostess_route_status"] == "not_created"
            and implementation_preflight_scope["hostess_input_status"] == "not_created"
            and implementation_preflight_scope["adb_status"] == "not_used"
            and implementation_preflight_scope["command_status"] == "no_commands",
            implementation_preflight_scope,
            {
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "implementation_plan_status": "not_created",
                "submission_envelope_status": "not_created",
                "submission_status": "not_submitted",
                "intake_response_status": "not_created",
                "decision_status": "not_decided",
                "response_schema_status": "not_created",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "validation_report_status": "not_created",
                "public_derivative_status": "not_created",
                "hostess_boundary_descriptor_status": "not_created",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
            },
            "preflight creates no Manifold repo change, response, state, audit, validation report, Hostess input, ADB, or commands",
        ),
        check(
            "submission_intake_response_preflight.authority",
            authority["submission_envelope_owner"] == "operator"
            and authority["submission_request_owner"] == "operator"
            and authority["intake_response_implementation_owner"] == "rusty.manifold"
            and authority["intake_response_owner"] == "rusty.manifold"
            and authority["submission_acceptance_owner"] == "rusty.manifold"
            and authority["decision_owner"] == "rusty.manifold"
            and authority["response_schema_owner"] == "rusty.manifold"
            and authority["route_implementation_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["validation_report_owner"] == "rusty.manifold"
            and authority["rollback_owner"] == "rusty.manifold"
            and authority["source_chain_digest_owner"] == "rusty.manifold"
            and authority["redaction_review_input_owner"] == "operator"
            and authority["redaction_review_validation_owner"] == "rusty.manifold"
            and authority["hostess_boundary_descriptor_owner"] == "rusty.manifold"
            and authority["future_hostess_route_owner"] == "rusty.hostess"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer",
            authority,
            {
                "submission_envelope_owner": "operator",
                "submission_request_owner": "operator",
                "intake_response_implementation_owner": "rusty.manifold",
                "intake_response_owner": "rusty.manifold",
                "submission_acceptance_owner": "rusty.manifold",
                "decision_owner": "rusty.manifold",
                "response_schema_owner": "rusty.manifold",
                "route_implementation_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "validation_report_owner": "rusty.manifold",
                "rollback_owner": "rusty.manifold",
                "source_chain_digest_owner": "rusty.manifold",
                "redaction_review_input_owner": "operator",
                "redaction_review_validation_owner": "rusty.manifold",
                "hostess_boundary_descriptor_owner": "rusty.manifold",
                "future_hostess_route_owner": "rusty.hostess",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
            },
            "operator owns the future submission envelope; Manifold owns future response implementation, state, audit, validation, and Hostess boundary descriptor",
        ),
        check(
            "submission_intake_response_preflight.artifacts_manifold_owned_not_created",
            bool(artifacts)
            and required_artifact_kinds <= {artifact["artifact_kind"] for artifact in artifacts}
            and all(artifact["status"] == "not_created_by_sidecar" for artifact in artifacts)
            and all(artifact["owner"] in {"rusty.manifold", "rusty.manifold.audit"} for artifact in artifacts),
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
                "artifact_count": 11,
            },
            "all required submission intake response implementation artifacts are Manifold-owned and not created by the sidecar repo",
        ),
        check(
            "submission_intake_response_preflight.validation_rejection_revision_audit_terms",
            required_validation_slots <= set(requirements["required_validation_slots"])
            and required_response_decisions == set(requirements["required_response_decisions"])
            and required_rejection_terms <= set(requirements["required_rejection_terms"])
            and required_revision_terms <= set(requirements["required_revision_terms"])
            and required_audit_terms <= set(requirements["required_audit_terms"]),
            {
                "required_validation_slots": requirements["required_validation_slots"],
                "required_response_decisions": requirements["required_response_decisions"],
                "required_rejection_terms": requirements["required_rejection_terms"],
                "required_revision_terms": requirements["required_revision_terms"],
                "required_audit_terms": requirements["required_audit_terms"],
            },
            {
                "required_validation_slots": sorted(required_validation_slots),
                "required_response_decisions": sorted(required_response_decisions),
                "required_rejection_terms": sorted(required_rejection_terms),
                "required_revision_terms": sorted(required_revision_terms),
                "required_audit_terms": sorted(required_audit_terms),
            },
            "future Manifold submission intake response implementation must include received, revision, rejection, audit, validation, privacy, and Hostess coverage",
        ),
        check(
            "submission_intake_response_preflight.route_boundaries",
            route_boundaries["input_payload_class"] == "low_rate_descriptor"
            and route_boundaries["accepts_sanitized_summary_only"] is True
            and route_boundaries["requires_operator_submission_envelope"] is True
            and route_boundaries["requires_source_chain_digest"] is True
            and route_boundaries["requires_redaction_review"] is True
            and route_boundaries["allows_endpoint_values"] is False
            and route_boundaries["allows_commands"] is False
            and route_boundaries["allows_adb"] is False
            and route_boundaries["allows_raw_logs"] is False
            and route_boundaries["allows_visual_captures"] is False
            and route_boundaries["allows_private_device_ids"] is False
            and route_boundaries["allows_high_rate_payloads"] is False
            and route_boundaries["allows_sidecar_direct_hostess_input"] is False
            and route_boundaries["creates_response_by_sidecar"] is False
            and route_boundaries["creates_accepted_state_by_sidecar"] is False
            and route_boundaries["creates_audit_by_sidecar"] is False
            and route_boundaries["creates_validation_report_by_sidecar"] is False
            and route_boundaries["creates_hostess_input"] is False
            and route_boundaries["accepted_state_owner"] == "rusty.manifold"
            and route_boundaries["audit_owner"] == "rusty.manifold.audit"
            and requirements["rollback_policy"] == "manifold_owned_reject_submission_or_request_revision",
            {
                "required_route_boundaries": route_boundaries,
                "rollback_policy": requirements["rollback_policy"],
            },
            {
                "input_payload_class": "low_rate_descriptor",
                "accepts_sanitized_summary_only": True,
                "requires_operator_submission_envelope": True,
                "requires_source_chain_digest": True,
                "requires_redaction_review": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_raw_logs": False,
                "allows_visual_captures": False,
                "allows_private_device_ids": False,
                "allows_high_rate_payloads": False,
                "allows_sidecar_direct_hostess_input": False,
                "creates_response_by_sidecar": False,
                "creates_accepted_state_by_sidecar": False,
                "creates_audit_by_sidecar": False,
                "creates_validation_report_by_sidecar": False,
                "creates_hostess_input": False,
                "accepted_state_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "rollback_policy": "manifold_owned_reject_submission_or_request_revision",
            },
            "future Manifold submission intake response route preflight remains low-rate sanitized descriptor input only and rejects sidecar authority drift",
        ),
        check(
            "submission_intake_response_preflight.hostess_deferred",
            hostess_boundary_preflight["status"] == "future_lane_not_requested"
            and hostess_boundary_preflight["route_status"] == "not_created"
            and hostess_boundary_preflight["input_status"] == "not_created"
            and hostess_boundary_preflight["recovery_request_status"] == "not_created"
            and hostess_boundary_preflight["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary_preflight["future_route_owner"] == "rusty.hostess"
            and hostess_boundary_preflight["boundary_descriptor_owner"] == "rusty.manifold"
            and hostess_boundary_preflight["consumes_only"] == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and hostess_boundary_preflight["sidecar_direct_input_allowed"] is False
            and hostess_boundary_preflight["requires_manifold_accepted_state"] is True
            and hostess_boundary_preflight["requires_explicit_operator_request"] is True
            and hostess_boundary_preflight["preflight_result"] == "hostess_deferred_until_manifold_submission_intake_acceptance",
            hostess_boundary_preflight,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "input_status": "not_created",
                "recovery_request_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "future_route_owner": "rusty.hostess",
                "boundary_descriptor_owner": "rusty.manifold",
                "consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "preflight_result": "hostess_deferred_until_manifold_submission_intake_acceptance",
            },
            "Hostess remains deferred until Manifold accepted state or an explicit operator request exists",
        ),
        check(
            "submission_intake_response_preflight.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_submission_intake_response_implementation_and_audit"
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
                "future_manifold_gate": "manifold_repo_owns_submission_intake_response_implementation_and_audit",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "preflight remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": PREFLIGHT_SCHEMA,
        "preflight_id": "preflight.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation.synthetic.001",
        "generated_at": now,
        "preflight_status": "ready_for_manifold_submission_intake_response_implementation_planning" if fail_count == 0 else "blocked",
        "source_submission_intake_response_expectation": source_expectation,
        "implementation_preflight_scope": implementation_preflight_scope,
        "authority": authority,
        "manifold_repo_submission_intake_response_requirements": requirements,
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
            "The submission intake response implementation preflight is descriptor evidence only; it does not touch the Manifold repo, create a branch, create an implementation plan, create a submission envelope, create a response, decide the submission, create schemas, create routes, create accepted state, create audit records, create validation reports, create public derivative artifacts, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future submission intake response implementation, response, decision, route, command/session/audit, validation-report, rollback, source-chain, redaction-validation, and accepted-state authority.",
            "The operator remains responsible for any future submission envelope and redaction inputs before Manifold can accept or reject the submission.",
            "Hostess remains a future operator/recovery lane after Manifold accepted state or a separate explicit operator request descriptor; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "manifold_submission_intake_response_handoff_or_manifold_repo_submission_intake_response",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intake-response-expectation", required=True, help="Generated submission intake response expectation fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output submission intake response implementation preflight path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        preflight = build_preflight(Path(args.intake_response_expectation), repo_root, args.now)
        write_json(Path(args.output), preflight)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": preflight["preflight_status"], "check_count": preflight["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
