#!/usr/bin/env python3
"""Generate a descriptor-only operator decision request for the Manifold slice response handoff."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


REQUEST_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1"
HANDOFF_PACKAGE_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_handoff_package.v1"


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
    handoff_result = validate_repo.validate_json_file(handoff_package_path)
    handoff_manifest = handoff_package.get("handoff_manifest", {})
    hostess_handoff = handoff_package.get("hostess_boundary_handoff", {})

    source_handoff_package = {
        "path": relative_output_path(handoff_package_path, repo_root),
        "schema": handoff_package.get("schema"),
        "package_id": handoff_package.get("package_id"),
        "package_status": handoff_package.get("package_status"),
        "next_gate": handoff_package.get("next_gate"),
    }
    decision_request_scope = {
        "request_class": "manifold_public_derivative_schema_slice_response_operator_decision_request",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "operator_decision_status": "not_recorded",
        "operator_decision_record_status": "not_created",
        "manifold_submission_status": "not_submitted",
        "manifold_repo_touch_status": "not_touched",
        "manifold_branch_status": "not_created",
        "manifold_response_status": "not_created",
        "manifold_decision_status": "not_decided",
        "manifold_accepted_state_status": "not_created",
        "manifold_audit_record_status": "not_created",
        "public_derivative_status": "not_created",
        "hostess_route_status": "not_created",
        "hostess_input_status": "not_created",
        "live_evidence_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    authority = {
        "request_owner": "rusty.quest.sidecar_mesh",
        "operator_decision_owner": "operator",
        "submission_request_owner": "operator",
        "handoff_acceptance_owner": "rusty.manifold",
        "response_owner": "rusty.manifold",
        "decision_owner": "rusty.manifold",
        "schema_owner": "rusty.manifold",
        "route_implementation_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "rollback_owner": "rusty.manifold",
        "hostess_boundary_descriptor_owner": "rusty.manifold",
        "future_hostess_route_owner": "rusty.hostess",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    requested_decision = {
        "decision_class": "submit_handoff_package_to_manifold_or_hold",
        "decision_status": "not_recorded",
        "allowed_decisions": [
            "submit_to_manifold_review",
            "hold_for_revision",
            "reject_sidecar_handoff",
        ],
        "default_without_decision": "hold",
        "requires_operator_review": True,
        "creates_manifold_state": False,
        "creates_manifold_route": False,
        "creates_hostess_input": False,
        "route_start_allowed": False,
        "live_evidence_allowed": False,
    }
    operator_packet = {
        "packet_status": "draft",
        "decision_record_status": "not_created",
        "required_review_items": [
            "source_handoff_package_status",
            "source_chain_summary",
            "manifold_owned_artifact_requirements",
            "validation_summary",
            "privacy_boundary",
            "hostess_boundary_gate",
            "rollback_policy",
        ],
        "allowed_decision_records": [
            "operator.submit_to_manifold_review",
            "operator.hold_for_revision",
            "operator.reject_sidecar_handoff",
        ],
        "rejection_terms": [
            "operator_decision_missing",
            "handoff_package_invalid",
            "source_chain_incomplete",
            "redaction_incomplete",
            "hostess_boundary_unclear",
            "manifold_response_scope_unclear",
            "endpoint_values_rejected",
            "commands_rejected",
            "adb_rejected",
        ],
        "revision_terms": [
            "handoff_manifest_revision",
            "source_chain_revision",
            "hostess_boundary_revision",
            "validation_evidence_revision",
            "privacy_boundary_revision",
        ],
    }
    manifold_submission_gate = {
        "submission_status": "not_submitted",
        "target_repo": "rusty.manifold",
        "allowed_submission_owner": "operator",
        "acceptance_owner": "rusty.manifold",
        "response_owner": "rusty.manifold",
        "decision_owner": "rusty.manifold",
        "accepted_state_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "requires_source_package_ready": True,
        "requires_operator_decision": True,
        "requires_redaction_review": True,
        "requires_source_chain_digest": True,
        "sidecar_can_submit_directly": False,
        "sidecar_can_accept": False,
        "sidecar_can_create_state": False,
        "sidecar_can_create_response": False,
    }
    hostess_boundary_gate = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "input_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "boundary_descriptor_owner": "rusty.manifold",
        "future_route_owner": "rusty.hostess",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "gate_result": "prepared_without_hostess_input",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.py --handoff-package fixtures/valid/manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json --now 2026-06-05T01:04:00Z --output fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "operator_decision_then_manifold_repo_owned_public_derivative_schema_slice_response",
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

    required_review_items = {
        "source_handoff_package_status",
        "source_chain_summary",
        "manifold_owned_artifact_requirements",
        "validation_summary",
        "privacy_boundary",
        "hostess_boundary_gate",
        "rollback_policy",
    }
    required_rejections = {
        "operator_decision_missing",
        "handoff_package_invalid",
        "source_chain_incomplete",
        "redaction_incomplete",
        "hostess_boundary_unclear",
        "manifold_response_scope_unclear",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
    }
    required_revisions = {
        "handoff_manifest_revision",
        "source_chain_revision",
        "hostess_boundary_revision",
        "validation_evidence_revision",
        "privacy_boundary_revision",
    }

    checks = [
        check(
            "operator_decision_request.source_handoff_package_ready",
            handoff_result.ok
            and handoff_package.get("schema") == HANDOFF_PACKAGE_SCHEMA
            and handoff_package.get("package_status") == "public_derivative_schema_slice_response_handoff_package_ready"
            and handoff_package.get("next_gate") == "manifold_repo_public_derivative_schema_slice_response_or_operator_decision",
            {
                "schema": handoff_package.get("schema"),
                "package_status": handoff_package.get("package_status"),
                "next_gate": handoff_package.get("next_gate"),
            },
            {
                "schema": HANDOFF_PACKAGE_SCHEMA,
                "package_status": "public_derivative_schema_slice_response_handoff_package_ready",
                "next_gate": "manifold_repo_public_derivative_schema_slice_response_or_operator_decision",
            },
            relative_output_path(handoff_package_path, repo_root),
        ),
        check(
            "operator_decision_request.no_submission_state_route_or_hostess_input",
            decision_request_scope["operator_decision_status"] == "not_recorded"
            and decision_request_scope["manifold_submission_status"] == "not_submitted"
            and decision_request_scope["manifold_repo_touch_status"] == "not_touched"
            and decision_request_scope["manifold_response_status"] == "not_created"
            and decision_request_scope["manifold_accepted_state_status"] == "not_created"
            and decision_request_scope["manifold_audit_record_status"] == "not_created"
            and decision_request_scope["hostess_route_status"] == "not_created"
            and decision_request_scope["hostess_input_status"] == "not_created"
            and decision_request_scope["live_evidence_status"] == "not_included"
            and decision_request_scope["adb_status"] == "not_used"
            and decision_request_scope["command_status"] == "no_commands",
            decision_request_scope,
            {
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
            },
            "operator decision request creates no downstream submission, state, route, Hostess input, live evidence, ADB, or command action",
        ),
        check(
            "operator_decision_request.authority_boundary",
            authority["operator_decision_owner"] == "operator"
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
            and authority["sidecar_role"] == "observer_proposer"
            and authority["proposal_status"] == "not_accepted",
            authority,
            {
                "operator_decision_owner": "operator",
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
            },
            "operator owns the go/no-go request while Manifold and Hostess authority boundaries stay explicit",
        ),
        check(
            "operator_decision_request.operator_packet_draft",
            requested_decision["decision_status"] == "not_recorded"
            and set(requested_decision["allowed_decisions"])
            == {"submit_to_manifold_review", "hold_for_revision", "reject_sidecar_handoff"}
            and requested_decision["default_without_decision"] == "hold"
            and requested_decision["requires_operator_review"] is True
            and requested_decision["creates_manifold_state"] is False
            and requested_decision["creates_hostess_input"] is False
            and requested_decision["route_start_allowed"] is False
            and operator_packet["packet_status"] == "draft"
            and operator_packet["decision_record_status"] == "not_created"
            and required_review_items <= set(operator_packet["required_review_items"])
            and required_rejections <= set(operator_packet["rejection_terms"])
            and required_revisions <= set(operator_packet["revision_terms"]),
            {
                "requested_decision": requested_decision,
                "operator_packet": operator_packet,
            },
            {
                "decision_status": "not_recorded",
                "allowed_decisions": ["submit_to_manifold_review", "hold_for_revision", "reject_sidecar_handoff"],
                "default_without_decision": "hold",
                "requires_operator_review": True,
                "creates_manifold_state": False,
                "creates_hostess_input": False,
                "route_start_allowed": False,
                "packet_status": "draft",
                "decision_record_status": "not_created",
                "required_review_items": sorted(required_review_items),
                "required_rejections": sorted(required_rejections),
                "required_revisions": sorted(required_revisions),
            },
            "operator packet is a draft decision surface, not an approval or submission",
        ),
        check(
            "operator_decision_request.manifold_submission_gate",
            manifold_submission_gate["submission_status"] == "not_submitted"
            and manifold_submission_gate["target_repo"] == "rusty.manifold"
            and manifold_submission_gate["allowed_submission_owner"] == "operator"
            and manifold_submission_gate["acceptance_owner"] == "rusty.manifold"
            and manifold_submission_gate["response_owner"] == "rusty.manifold"
            and manifold_submission_gate["decision_owner"] == "rusty.manifold"
            and manifold_submission_gate["accepted_state_owner"] == "rusty.manifold"
            and manifold_submission_gate["audit_owner"] == "rusty.manifold.audit"
            and manifold_submission_gate["requires_source_package_ready"] is True
            and manifold_submission_gate["requires_operator_decision"] is True
            and manifold_submission_gate["requires_redaction_review"] is True
            and manifold_submission_gate["requires_source_chain_digest"] is True
            and manifold_submission_gate["sidecar_can_submit_directly"] is False
            and manifold_submission_gate["sidecar_can_accept"] is False
            and manifold_submission_gate["sidecar_can_create_state"] is False
            and manifold_submission_gate["sidecar_can_create_response"] is False,
            manifold_submission_gate,
            {
                "submission_status": "not_submitted",
                "target_repo": "rusty.manifold",
                "allowed_submission_owner": "operator",
                "acceptance_owner": "rusty.manifold",
                "response_owner": "rusty.manifold",
                "decision_owner": "rusty.manifold",
                "accepted_state_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "requires_source_package_ready": True,
                "requires_operator_decision": True,
                "requires_redaction_review": True,
                "requires_source_chain_digest": True,
                "sidecar_can_submit_directly": False,
                "sidecar_can_accept": False,
                "sidecar_can_create_state": False,
                "sidecar_can_create_response": False,
            },
            "Manifold submission remains an explicit future operator action and Manifold remains acceptance owner",
        ),
        check(
            "operator_decision_request.hostess_boundary_gate",
            hostess_handoff.get("status") == "future_lane_not_requested"
            and hostess_boundary_gate["status"] == "future_lane_not_requested"
            and hostess_boundary_gate["route_status"] == "not_created"
            and hostess_boundary_gate["input_status"] == "not_created"
            and hostess_boundary_gate["recovery_request_status"] == "not_created"
            and hostess_boundary_gate["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary_gate["consumes_only"] == "manifold_accepted_state_or_operator_request_descriptor"
            and hostess_boundary_gate["sidecar_direct_input_allowed"] is False
            and hostess_boundary_gate["requires_manifold_accepted_state"] is True
            and hostess_boundary_gate["requires_explicit_operator_request"] is True
            and hostess_boundary_gate["boundary_descriptor_owner"] == "rusty.manifold"
            and hostess_boundary_gate["future_route_owner"] == "rusty.hostess"
            and hostess_boundary_gate["gate_result"] == "prepared_without_hostess_input",
            {
                "source_hostess_handoff": hostess_handoff,
                "hostess_boundary_gate": hostess_boundary_gate,
            },
            {
                "source_status": "future_lane_not_requested",
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "input_status": "not_created",
                "recovery_request_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "boundary_descriptor_owner": "rusty.manifold",
                "future_route_owner": "rusty.hostess",
                "gate_result": "prepared_without_hostess_input",
            },
            "Hostess remains prepared as a downstream route owner without direct sidecar input",
        ),
        check(
            "operator_decision_request.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "operator_decision_then_manifold_repo_owned_public_derivative_schema_slice_response"
            and validation_evidence["future_hostess_gate"] == "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor"
            and handoff_manifest.get("handoff_acceptance_status") == "not_accepted"
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
                "handoff_acceptance_status": handoff_manifest.get("handoff_acceptance_status"),
                "privacy_boundary": privacy_boundary,
            },
            {
                "local_validation_status": "expected_pass",
                "damaged_fixture_policy": "must_fail_validation",
                "future_manifold_gate": "operator_decision_then_manifold_repo_owned_public_derivative_schema_slice_response",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor",
                "handoff_acceptance_status": "not_accepted",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "operator decision request remains public-safe descriptor evidence with Manifold and Hostess gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": REQUEST_SCHEMA,
        "request_id": "request.manifold_public_derivative_schema_slice_response_operator_decision.synthetic.001",
        "generated_at": now,
        "request_status": "operator_decision_required" if fail_count == 0 else "blocked",
        "source_manifold_public_derivative_schema_slice_response_handoff_package": source_handoff_package,
        "decision_request_scope": decision_request_scope,
        "authority": authority,
        "requested_decision": requested_decision,
        "operator_packet": operator_packet,
        "manifold_submission_gate": manifold_submission_gate,
        "hostess_boundary_gate": hostess_boundary_gate,
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
            "Operator decision is required before the sidecar handoff package can be submitted for Manifold review; this request does not record that decision.",
            "The operator decision request is descriptor evidence only; it does not touch Manifold, submit the handoff, create a response, decide the review, create accepted state, create audit records, touch Hostess, create Hostess input, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future handoff acceptance, response, decision, schema, route implementation, command/session/audit, rollback, validation report, and accepted-state authority.",
            "Hostess remains a future route owner after Manifold accepted state or a separate explicit operator request descriptor; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "operator_decision_or_manifold_repo_public_derivative_schema_slice_response",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--handoff-package", required=True, help="Generated Manifold public derivative schema slice response handoff package fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output operator decision request path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        request = build_request(Path(args.handoff_package), repo_root, args.now)
        write_json(Path(args.output), request)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_public_derivative_schema_slice_response_operator_decision_request failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": request["request_status"], "check_count": request["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
