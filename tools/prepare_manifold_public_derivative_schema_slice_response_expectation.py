#!/usr/bin/env python3
"""Generate the expected envelope for a future Manifold-owned public derivative schema slice response."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


EXPECTATION_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_expectation.v1"
PACKAGE_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_handoff_package.v1"


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


def build_expectation(handoff_package_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    handoff_package = load_json(handoff_package_path)
    package_result = validate_repo.validate_json_file(handoff_package_path)
    manifest = handoff_package.get("handoff_manifest", {})

    source_package = {
        "path": relative_output_path(handoff_package_path, repo_root),
        "schema": handoff_package.get("schema"),
        "package_id": handoff_package.get("package_id"),
        "package_status": handoff_package.get("package_status"),
        "next_gate": handoff_package.get("next_gate"),
    }
    response_expectation_scope = {
        "expectation_class": "manifold_owned_public_derivative_schema_slice_response_expectation",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "implementation_status": "not_created",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "schema_status": "not_created",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "validation_report_status": "not_created",
        "public_derivative_status": "not_created",
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "handoff_acceptance_owner": "rusty.manifold",
        "implementation_plan_owner": "rusty.manifold",
        "response_owner": "rusty.manifold",
        "decision_owner": "rusty.manifold",
        "schema_owner": "rusty.manifold",
        "route_implementation_owner": "rusty.manifold",
        "request_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "rollback_owner": "rusty.manifold",
        "redaction_review_owner": "operator",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    expected_manifold_slice_response = {
        "response_class": "manifold_owned_public_derivative_schema_slice_handoff_response",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "allowed_decisions": [
            "accepted_for_manifold_schema_slice",
            "revision_requested",
            "rejected",
        ],
        "allowed_response_owner": "rusty.manifold",
        "required_fields": [
            "response_id",
            "package_id",
            "decision",
            "decision_owner",
            "response_owner",
            "created_at",
            "revision",
            "accepted_source_chain_ref",
            "implementation_plan_ref",
            "schema_ref",
            "route_ref",
            "accepted_state_ref",
            "audit_ref",
            "validation_report_ref",
            "hostess_boundary_ref",
            "rejection_terms",
            "required_revisions",
            "redaction_review",
            "operator_approval_status",
            "privacy_review",
            "rollback_ref",
        ],
        "required_rejection_terms": [
            "operator_approval_missing",
            "public_derivative_schema_missing",
            "source_chain_incomplete",
            "invalid_handoff_package",
            "endpoint_values_rejected",
            "commands_rejected",
            "adb_rejected",
            "stale_peer_status",
            "untrusted_sidecar",
            "redaction_incomplete",
            "cleanup_incomplete",
            "high_rate_payload_rejected",
            "hostess_direct_action_rejected",
        ],
        "required_revision_terms": [
            "schema_shape_revision",
            "route_semantics_revision",
            "audit_shape_revision",
            "accepted_state_mapping_revision",
            "hostess_boundary_revision",
            "privacy_boundary_revision",
            "validation_report_revision",
            "source_chain_revision",
            "package_manifest_revision",
        ],
        "required_audit_terms": [
            "package_id",
            "decision",
            "revision",
            "reject_or_revision_reason",
            "schema_ref",
            "route_ref",
            "accepted_state_ref",
            "validation_report_ref",
            "operator_approval_status",
            "redaction_review_status",
            "source_chain_digest",
        ],
        "disallowed_response_content": [
            "endpoint_values",
            "shell_text",
            "android_target",
            "adb_target",
            "pairing_material",
            "package_markers",
            "high_rate_payloads",
            "raw_logs",
            "visual_captures",
            "private_device_ids",
            "hostess_direct_action",
        ],
        "accepted_state_policy": "manifold_owned_monotonic_revision",
        "implementation_policy": "response_records_decision_only",
        "rollback_policy": "manifold_owned_disable_route_or_reject_source",
        "public_derivative_policy": "response_does_not_create_derivative_artifact",
        "hostess_input_policy": "response_does_not_create_hostess_input",
    }
    hostess_response_gate = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_action_class": "operator_recovery_request_descriptor",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_manifold_public_derivative_schema_slice_response_expectation.py --handoff-package fixtures/valid/manifold-public-derivative-schema-handoff-package.synthetic.json --now 2026-06-05T00:40:00Z --output fixtures/valid/manifold-public-derivative-schema-slice-response-expectation.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_public_derivative_schema_slice_response_and_audit",
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

    source_artifacts = manifest.get("source_chain_artifacts", [])
    downstream_artifacts = manifest.get("required_downstream_artifacts", [])
    route_boundaries = manifest.get("required_route_boundaries", {})
    required_decisions = set(expected_manifold_slice_response["allowed_decisions"])
    required_fields = set(expected_manifold_slice_response["required_fields"])
    required_rejections = set(expected_manifold_slice_response["required_rejection_terms"])
    required_revisions = set(expected_manifold_slice_response["required_revision_terms"])
    required_audit_terms = set(expected_manifold_slice_response["required_audit_terms"])
    disallowed_content = set(expected_manifold_slice_response["disallowed_response_content"])

    checks = [
        check(
            "public_derivative_schema_slice_response_expectation.source_package_ready",
            package_result.ok
            and handoff_package.get("schema") == PACKAGE_SCHEMA
            and handoff_package.get("package_status") == "public_derivative_schema_handoff_package_ready"
            and handoff_package.get("next_gate") == "manifold_repo_public_derivative_schema_slice_or_operator_decision",
            {
                "schema": handoff_package.get("schema"),
                "package_status": handoff_package.get("package_status"),
                "next_gate": handoff_package.get("next_gate"),
            },
            {
                "schema": PACKAGE_SCHEMA,
                "package_status": "public_derivative_schema_handoff_package_ready",
                "next_gate": "manifold_repo_public_derivative_schema_slice_or_operator_decision",
            },
            relative_output_path(handoff_package_path, repo_root),
        ),
        check(
            "public_derivative_schema_slice_response_expectation.no_response_schema_route_or_state",
            response_expectation_scope["repo_touch_status"] == "not_touched"
            and response_expectation_scope["branch_status"] == "not_created"
            and response_expectation_scope["implementation_status"] == "not_created"
            and response_expectation_scope["response_status"] == "not_created"
            and response_expectation_scope["decision_status"] == "not_decided"
            and response_expectation_scope["schema_status"] == "not_created"
            and response_expectation_scope["route_status"] == "not_created"
            and response_expectation_scope["accepted_state_status"] == "not_created"
            and response_expectation_scope["audit_record_status"] == "not_created"
            and response_expectation_scope["validation_report_status"] == "not_created"
            and response_expectation_scope["public_derivative_status"] == "not_created"
            and response_expectation_scope["hostess_route_status"] == "not_created",
            response_expectation_scope,
            {
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "implementation_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "schema_status": "not_created",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "validation_report_status": "not_created",
                "public_derivative_status": "not_created",
                "hostess_route_status": "not_created",
            },
            "slice response expectation is descriptor-only and does not mutate Manifold, Hostess, or runtime state",
        ),
        check(
            "public_derivative_schema_slice_response_expectation.authority_split",
            authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["implementation_plan_owner"] == "rusty.manifold"
            and authority["response_owner"] == "rusty.manifold"
            and authority["decision_owner"] == "rusty.manifold"
            and authority["schema_owner"] == "rusty.manifold"
            and authority["route_implementation_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["rollback_owner"] == "rusty.manifold"
            and authority["redaction_review_owner"] == "operator"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer",
            authority,
            {
                "handoff_acceptance_owner": "rusty.manifold",
                "implementation_plan_owner": "rusty.manifold",
                "response_owner": "rusty.manifold",
                "decision_owner": "rusty.manifold",
                "schema_owner": "rusty.manifold",
                "route_implementation_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "rollback_owner": "rusty.manifold",
                "redaction_review_owner": "operator",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_role": "observer_proposer",
            },
            "Manifold owns future handoff acceptance, response, decision, schema, route, state, audit, and rollback",
        ),
        check(
            "public_derivative_schema_slice_response_expectation.source_package_requirements_carried",
            len(source_artifacts) >= 12
            and len(downstream_artifacts) >= 8
            and manifest.get("handoff_acceptance_status") == "not_accepted"
            and manifest.get("downstream_implementation_status") == "not_created"
            and manifest.get("downstream_schema_status") == "not_created"
            and manifest.get("downstream_route_status") == "not_created"
            and manifest.get("downstream_validation_report_status") == "not_created"
            and manifest.get("downstream_hostess_boundary_status") == "not_created"
            and route_boundaries.get("allows_endpoint_values") is False
            and route_boundaries.get("allows_commands") is False
            and route_boundaries.get("allows_adb") is False
            and route_boundaries.get("allows_sidecar_direct_hostess_input") is False,
            {
                "source_artifact_count": len(source_artifacts),
                "downstream_artifact_count": len(downstream_artifacts),
                "handoff_acceptance_status": manifest.get("handoff_acceptance_status"),
                "downstream_implementation_status": manifest.get("downstream_implementation_status"),
                "downstream_schema_status": manifest.get("downstream_schema_status"),
                "downstream_route_status": manifest.get("downstream_route_status"),
                "downstream_validation_report_status": manifest.get("downstream_validation_report_status"),
                "downstream_hostess_boundary_status": manifest.get("downstream_hostess_boundary_status"),
                "route_boundaries": route_boundaries,
            },
            {
                "source_artifact_count": ">=12",
                "downstream_artifact_count": ">=8",
                "handoff_acceptance_status": "not_accepted",
                "downstream_implementation_status": "not_created",
                "downstream_schema_status": "not_created",
                "downstream_route_status": "not_created",
                "downstream_validation_report_status": "not_created",
                "downstream_hostess_boundary_status": "not_created",
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_sidecar_direct_hostess_input": False,
            },
            "source handoff package remains a complete proposal and has not created downstream work",
        ),
        check(
            "public_derivative_schema_slice_response_expectation.response_contract",
            expected_manifold_slice_response["response_status"] == "not_created"
            and expected_manifold_slice_response["decision_status"] == "not_decided"
            and expected_manifold_slice_response["allowed_response_owner"] == "rusty.manifold"
            and required_decisions <= set(expected_manifold_slice_response["allowed_decisions"])
            and required_fields <= set(expected_manifold_slice_response["required_fields"])
            and required_rejections <= set(expected_manifold_slice_response["required_rejection_terms"])
            and required_revisions <= set(expected_manifold_slice_response["required_revision_terms"])
            and required_audit_terms <= set(expected_manifold_slice_response["required_audit_terms"])
            and disallowed_content <= set(expected_manifold_slice_response["disallowed_response_content"])
            and expected_manifold_slice_response["accepted_state_policy"] == "manifold_owned_monotonic_revision"
            and expected_manifold_slice_response["implementation_policy"] == "response_records_decision_only"
            and expected_manifold_slice_response["rollback_policy"] == "manifold_owned_disable_route_or_reject_source",
            expected_manifold_slice_response,
            {
                "response_status": "not_created",
                "decision_status": "not_decided",
                "allowed_response_owner": "rusty.manifold",
                "allowed_decisions": sorted(required_decisions),
                "required_fields": sorted(required_fields),
                "required_rejection_terms": sorted(required_rejections),
                "required_revision_terms": sorted(required_revisions),
                "required_audit_terms": sorted(required_audit_terms),
                "disallowed_response_content": sorted(disallowed_content),
                "accepted_state_policy": "manifold_owned_monotonic_revision",
                "implementation_policy": "response_records_decision_only",
                "rollback_policy": "manifold_owned_disable_route_or_reject_source",
            },
            "future Manifold slice response defines bounded accept/revision/reject semantics without creating implementation",
        ),
        check(
            "public_derivative_schema_slice_response_expectation.no_public_derivative_or_hostess_input",
            expected_manifold_slice_response["public_derivative_policy"] == "response_does_not_create_derivative_artifact"
            and expected_manifold_slice_response["hostess_input_policy"] == "response_does_not_create_hostess_input"
            and response_expectation_scope["public_derivative_status"] == "not_created"
            and response_expectation_scope["operator_approval_status"] == "not_recorded"
            and response_expectation_scope["hostess_route_status"] == "not_created",
            {
                "public_derivative_policy": expected_manifold_slice_response["public_derivative_policy"],
                "hostess_input_policy": expected_manifold_slice_response["hostess_input_policy"],
                "public_derivative_status": response_expectation_scope["public_derivative_status"],
                "operator_approval_status": response_expectation_scope["operator_approval_status"],
                "hostess_route_status": response_expectation_scope["hostess_route_status"],
            },
            {
                "public_derivative_policy": "response_does_not_create_derivative_artifact",
                "hostess_input_policy": "response_does_not_create_hostess_input",
                "public_derivative_status": "not_created",
                "operator_approval_status": "not_recorded",
                "hostess_route_status": "not_created",
            },
            "future slice response expectation does not produce derivative evidence or direct Hostess input",
        ),
        check(
            "public_derivative_schema_slice_response_expectation.hostess_deferred",
            hostess_response_gate["status"] == "future_lane_not_requested"
            and hostess_response_gate["route_status"] == "not_created"
            and hostess_response_gate["recovery_request_status"] == "not_created"
            and hostess_response_gate["device_action_authority"] == "not_in_sidecar"
            and hostess_response_gate["consumes_only"] == "manifold_accepted_state_or_operator_request_descriptor"
            and hostess_response_gate["sidecar_direct_input_allowed"] is False
            and hostess_response_gate["requires_manifold_accepted_state"] is True
            and hostess_response_gate["requires_explicit_operator_request"] is True,
            hostess_response_gate,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "recovery_request_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
            },
            "Hostess remains deferred behind Manifold accepted state or explicit operator request",
        ),
        check(
            "public_derivative_schema_slice_response_expectation.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_public_derivative_schema_slice_response_and_audit"
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
                "future_manifold_gate": "manifold_repo_owns_public_derivative_schema_slice_response_and_audit",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "slice response expectation remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": EXPECTATION_SCHEMA,
        "expectation_id": "expectation.manifold_public_derivative_schema_slice_response.synthetic.001",
        "generated_at": now,
        "expectation_status": "ready_for_manifold_public_derivative_schema_slice_response" if fail_count == 0 else "blocked",
        "source_manifold_public_derivative_schema_handoff_package": source_package,
        "response_expectation_scope": response_expectation_scope,
        "authority": authority,
        "expected_manifold_slice_response": expected_manifold_slice_response,
        "hostess_response_gate": hostess_response_gate,
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
            "The Manifold public derivative schema slice response expectation is descriptor evidence only; it does not touch the Manifold repo, create a branch, create a response, decide the review, create schemas, create routes, create accepted state, create audit records, create validation reports, create public derivative artifacts, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "The sidecar may define the expected response envelope, but Manifold remains the handoff acceptance, implementation plan, schema, route, decision, command/session/audit, revision, lease, rollback, and accepted-state authority.",
            "Operator approval and redaction review remain required before real public derivative evidence can be accepted.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar expectation fixtures cannot directly drive Hostess device actions.",
        ],
        "next_gate": "manifold_public_derivative_schema_slice_response_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-package", required=True, help="Generated Manifold public derivative schema handoff package fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output Manifold public derivative schema slice response expectation path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        expectation = build_expectation(Path(args.handoff_package), repo_root, args.now)
        write_json(Path(args.output), expectation)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_public_derivative_schema_slice_response_expectation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": expectation["expectation_status"], "check_count": expectation["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
