#!/usr/bin/env python3
"""Generate the expected envelope for a future Manifold-owned design response."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


EXPECTATION_SCHEMA = "rusty.quest.sidecar.manifold_route_design_response_expectation.v1"
REQUEST_SCHEMA = "rusty.quest.sidecar.manifold_route_design_review_request.v1"


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


def build_expectation(design_review_request_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    design_review_request = load_json(design_review_request_path)
    request_result = validate_repo.validate_json_file(design_review_request_path)

    source_manifold_route_design_review_request = {
        "path": relative_output_path(design_review_request_path, repo_root),
        "schema": design_review_request.get("schema"),
        "request_id": design_review_request.get("request_id"),
        "request_status": design_review_request.get("request_status"),
        "next_gate": design_review_request.get("next_gate"),
    }
    response_expectation_scope = {
        "expectation_class": "manifold_owned_design_response_expectation",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
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
    expected_manifold_response = {
        "response_class": "manifold_owned_design_review_response",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "allowed_decisions": [
            "accepted_for_manifold_slice",
            "revision_requested",
            "rejected",
        ],
        "allowed_response_owner": "rusty.manifold",
        "required_fields": [
            "response_id",
            "request_id",
            "decision",
            "decision_owner",
            "response_owner",
            "created_at",
            "revision",
            "route_ref",
            "schema_refs",
            "accepted_state_ref",
            "audit_ref",
            "rejection_terms",
            "required_revisions",
            "hostess_boundary_ref",
            "privacy_review",
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
        "required_revision_terms": [
            "schema_shape_revision",
            "route_semantics_revision",
            "audit_shape_revision",
            "hostess_boundary_revision",
            "privacy_boundary_revision",
        ],
        "required_audit_terms": [
            "request_id",
            "decision",
            "revision",
            "reject_or_revision_reason",
            "accepted_state_ref",
        ],
        "disallowed_response_content": [
            "endpoint_values",
            "shell_text",
            "android_target",
            "pairing_material",
            "package_markers",
            "high_rate_payloads",
            "raw_logs",
            "visual_captures",
        ],
        "accepted_state_policy": "manifold_owned_monotonic_revision",
        "rollback_policy": "manifold_owned_disable_route_or_reject_source",
    }
    hostess_response_gate = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
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
            "python tools/prepare_manifold_route_design_response_expectation.py --design-review-request fixtures/valid/manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures/valid/manifold-route-design-response-expectation.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_response_decision_route_state_and_audit",
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
        "response_id",
        "request_id",
        "decision",
        "decision_owner",
        "response_owner",
        "created_at",
        "revision",
        "route_ref",
        "schema_refs",
        "accepted_state_ref",
        "audit_ref",
        "rejection_terms",
        "required_revisions",
        "hostess_boundary_ref",
        "privacy_review",
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
    required_revision_terms = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
    }
    disallowed_response_content = {
        "endpoint_values",
        "shell_text",
        "android_target",
        "pairing_material",
        "package_markers",
        "high_rate_payloads",
        "raw_logs",
        "visual_captures",
    }

    checks = [
        check(
            "route_design_response_expectation.source_request_ready",
            request_result.ok
            and design_review_request.get("schema") == REQUEST_SCHEMA
            and design_review_request.get("request_status") == "ready_for_manifold_route_design_review"
            and design_review_request.get("next_gate") == "manifold_repo_design_review_or_operator_decision",
            {
                "schema": design_review_request.get("schema"),
                "request_status": design_review_request.get("request_status"),
                "next_gate": design_review_request.get("next_gate"),
            },
            {
                "schema": REQUEST_SCHEMA,
                "request_status": "ready_for_manifold_route_design_review",
                "next_gate": "manifold_repo_design_review_or_operator_decision",
            },
            relative_output_path(design_review_request_path, repo_root),
        ),
        check(
            "route_design_response_expectation.no_response_route_or_state",
            response_expectation_scope["repo_touch_status"] == "not_touched"
            and response_expectation_scope["response_status"] == "not_created"
            and response_expectation_scope["decision_status"] == "not_decided"
            and response_expectation_scope["route_status"] == "not_created"
            and response_expectation_scope["accepted_state_status"] == "not_created"
            and response_expectation_scope["audit_record_status"] == "not_created"
            and response_expectation_scope["hostess_route_status"] == "not_created"
            and response_expectation_scope["live_evidence_status"] == "not_included",
            response_expectation_scope,
            {
                "repo_touch_status": "not_touched",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "live_evidence_status": "not_included",
            },
            "response expectation does not touch Manifold, Hostess, route, state, audit, or live evidence",
        ),
        check(
            "route_design_response_expectation.manifold_response_authority",
            authority["response_owner"] == "rusty.manifold"
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
            "Manifold remains response, decision, route, request, runtime, session, audit, state, and rollback owner",
        ),
        check(
            "route_design_response_expectation.response_envelope_constrained",
            expected_manifold_response["response_status"] == "not_created"
            and expected_manifold_response["decision_status"] == "not_decided"
            and set(expected_manifold_response["allowed_decisions"])
            == {"accepted_for_manifold_slice", "revision_requested", "rejected"}
            and expected_manifold_response["allowed_response_owner"] == "rusty.manifold"
            and required_fields <= set(expected_manifold_response["required_fields"])
            and required_rejection_terms <= set(expected_manifold_response["required_rejection_terms"])
            and required_revision_terms <= set(expected_manifold_response["required_revision_terms"])
            and disallowed_response_content <= set(expected_manifold_response["disallowed_response_content"]),
            {
                "response_status": expected_manifold_response["response_status"],
                "decision_status": expected_manifold_response["decision_status"],
                "allowed_decisions": expected_manifold_response["allowed_decisions"],
                "allowed_response_owner": expected_manifold_response["allowed_response_owner"],
                "required_field_count": len(expected_manifold_response["required_fields"]),
                "required_rejection_terms": expected_manifold_response["required_rejection_terms"],
                "required_revision_terms": expected_manifold_response["required_revision_terms"],
                "disallowed_response_content": expected_manifold_response["disallowed_response_content"],
            },
            {
                "response_status": "not_created",
                "decision_status": "not_decided",
                "allowed_decisions": ["accepted_for_manifold_slice", "revision_requested", "rejected"],
                "allowed_response_owner": "rusty.manifold",
                "required_fields": sorted(required_fields),
                "required_rejection_terms": sorted(required_rejection_terms),
                "required_revision_terms": sorted(required_revision_terms),
                "disallowed_response_content": sorted(disallowed_response_content),
            },
            "future Manifold response must be explicit about decision, fields, rejection, revision, and disallowed content",
        ),
        check(
            "route_design_response_expectation.hostess_gate",
            hostess_response_gate["status"] == "future_lane_not_requested"
            and hostess_response_gate["route_status"] == "not_created"
            and hostess_response_gate["device_action_authority"] == "not_in_sidecar"
            and hostess_response_gate["consumes_only"] == "manifold_accepted_state_or_operator_request_descriptor"
            and hostess_response_gate["sidecar_direct_input_allowed"] is False
            and hostess_response_gate["requires_manifold_accepted_state"] is True
            and hostess_response_gate["requires_explicit_operator_request"] is True,
            hostess_response_gate,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
            },
            "Hostess remains gated behind Manifold accepted state or explicit operator request",
        ),
        check(
            "route_design_response_expectation.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_response_decision_route_state_and_audit"
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
                "future_manifold_gate": "manifold_repo_owns_response_decision_route_state_and_audit",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "response expectation remains public-safe descriptor evidence with validation gates",
        ),
        check(
            "route_design_response_expectation.expectation_only_not_decision",
            response_expectation_scope["decision_status"] == "not_decided"
            and expected_manifold_response["response_status"] == "not_created"
            and expected_manifold_response["decision_status"] == "not_decided"
            and authority["proposal_status"] == "not_accepted",
            {
                "scope_decision_status": response_expectation_scope["decision_status"],
                "response_status": expected_manifold_response["response_status"],
                "response_decision_status": expected_manifold_response["decision_status"],
                "proposal_status": authority["proposal_status"],
            },
            {
                "scope_decision_status": "not_decided",
                "response_status": "not_created",
                "response_decision_status": "not_decided",
                "proposal_status": "not_accepted",
            },
            "sidecar expectation does not decide, accept, revise, reject, or create Manifold state",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": EXPECTATION_SCHEMA,
        "expectation_id": "expectation.manifold_route_design_response.synthetic.001",
        "generated_at": now,
        "expectation_status": "ready_for_manifold_owned_response" if fail_count == 0 else "blocked",
        "source_manifold_route_design_review_request": source_manifold_route_design_review_request,
        "response_expectation_scope": response_expectation_scope,
        "authority": authority,
        "expected_manifold_response": expected_manifold_response,
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
            "The Manifold route design response expectation is descriptor evidence only; it does not create a Manifold response, decide the review, create schemas, create routes, create accepted state, create audit records, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future response, decision, route implementation, request acceptance, command/session/audit, revision, lease, rollback, and accepted-state authority.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "manifold_owned_response_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design-review-request", required=True, help="Manifold route design review request fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output expectation path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        expectation = build_expectation(Path(args.design_review_request), repo_root, args.now)
        write_json(Path(args.output), expectation)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_route_design_response_expectation failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": expectation["expectation_status"], "check_count": expectation["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
