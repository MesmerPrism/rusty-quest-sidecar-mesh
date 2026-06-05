#!/usr/bin/env python3
"""Generate a descriptor-only request for Manifold route design review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


REQUEST_SCHEMA = "rusty.quest.sidecar.manifold_route_design_review_request.v1"
BLUEPRINT_SCHEMA = "rusty.quest.sidecar.manifold_route_blueprint.v1"


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


def build_request(route_blueprint_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    blueprint = load_json(route_blueprint_path)
    blueprint_result = validate_repo.validate_json_file(route_blueprint_path)

    source_manifold_route_blueprint = {
        "path": relative_output_path(route_blueprint_path, repo_root),
        "schema": blueprint.get("schema"),
        "blueprint_id": blueprint.get("blueprint_id"),
        "blueprint_status": blueprint.get("blueprint_status"),
        "next_gate": blueprint.get("next_gate"),
    }
    request_scope = {
        "request_class": "manifold_repo_route_design_review_request",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "hostess_route_status": "not_created",
        "operator_decision_status": "not_recorded",
        "live_evidence_status": "not_included",
    }
    authority = {
        "request_owner": "rusty.quest.sidecar_mesh",
        "design_review_owner": "rusty.manifold",
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
    proposed_manifold_review = {
        "review_id": "review.sidecar_peer_status_route.synthetic.001",
        "review_status": "requested_not_opened",
        "review_owner": "rusty.manifold",
        "requested_route_name": blueprint.get("proposed_manifold_route", {}).get("route_name"),
        "requested_route_status": "candidate",
        "requested_payload_class": "low_rate_advisory_status",
        "review_topics": [
            "topic.schema_contract",
            "topic.accept_reject_decision_event",
            "topic.accepted_state_revision_policy",
            "topic.audit_record_shape",
            "topic.hostess_boundary_preconditions",
            "topic.privacy_redaction_rejection_terms",
        ],
        "decision_status": "not_decided",
        "required_output_class": "manifold_owned_schema_route_decision_or_rejection",
    }
    proposed_manifold_work_items = [
        {
            "work_item_id": "work.sidecar_peer_status_request_schema",
            "work_item_kind": "schema",
            "owner": "rusty.manifold",
            "status": "not_created",
            "source_blueprint_field": "candidate_schemas.request",
            "acceptance_required": True,
        },
        {
            "work_item_id": "work.sidecar_peer_status_decision_schema",
            "work_item_kind": "schema",
            "owner": "rusty.manifold",
            "status": "not_created",
            "source_blueprint_field": "candidate_schemas.decision_event",
            "acceptance_required": True,
        },
        {
            "work_item_id": "work.sidecar_peer_status_accepted_state_schema",
            "work_item_kind": "schema",
            "owner": "rusty.manifold",
            "status": "not_created",
            "source_blueprint_field": "candidate_schemas.accepted_state",
            "acceptance_required": True,
        },
        {
            "work_item_id": "work.sidecar_peer_status_route_handler",
            "work_item_kind": "route_handler",
            "owner": "rusty.manifold",
            "status": "not_created",
            "source_blueprint_field": "proposed_manifold_route",
            "acceptance_required": True,
        },
        {
            "work_item_id": "work.sidecar_peer_status_audit_fixture",
            "work_item_kind": "audit_fixture",
            "owner": "rusty.manifold",
            "status": "not_created",
            "source_blueprint_field": "audit_contract",
            "acceptance_required": True,
        },
        {
            "work_item_id": "work.sidecar_peer_status_hostess_boundary_descriptor",
            "work_item_kind": "hostess_boundary_descriptor",
            "owner": "rusty.manifold",
            "status": "not_created",
            "source_blueprint_field": "hostess_boundary",
            "acceptance_required": True,
        },
    ]
    hostess_integration_preconditions = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_input_class": "manifold_accepted_state_or_operator_request_descriptor",
        "disallowed_input_classes": [
            "sidecar_peer_message",
            "endpoint_value",
            "command_payload",
            "adb_target",
            "pairing_material",
            "high_rate_payload",
        ],
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/prepare_manifold_route_design_review.py --route-blueprint fixtures/valid/manifold-route-blueprint.synthetic.json --now 2026-06-04T23:12:00Z --output fixtures/valid/manifold-route-design-review-request.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_schema_route_acceptance_and_audit",
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

    observed_topics = set(proposed_manifold_review["review_topics"])
    required_topics = {
        "topic.schema_contract",
        "topic.accept_reject_decision_event",
        "topic.accepted_state_revision_policy",
        "topic.audit_record_shape",
        "topic.hostess_boundary_preconditions",
        "topic.privacy_redaction_rejection_terms",
    }
    checks = [
        check(
            "route_design_review.source_blueprint_ready",
            blueprint_result.ok
            and blueprint.get("schema") == BLUEPRINT_SCHEMA
            and blueprint.get("blueprint_status") == "ready_for_manifold_repo_design_review"
            and blueprint.get("next_gate") == "manifold_repo_design_review_or_operator_decision",
            {
                "schema": blueprint.get("schema"),
                "blueprint_status": blueprint.get("blueprint_status"),
                "next_gate": blueprint.get("next_gate"),
            },
            {
                "schema": BLUEPRINT_SCHEMA,
                "blueprint_status": "ready_for_manifold_repo_design_review",
                "next_gate": "manifold_repo_design_review_or_operator_decision",
            },
            relative_output_path(route_blueprint_path, repo_root),
        ),
        check(
            "route_design_review.no_repo_route_or_state",
            request_scope["repo_touch_status"] == "not_touched"
            and request_scope["route_status"] == "not_created"
            and request_scope["accepted_state_status"] == "not_created"
            and request_scope["audit_record_status"] == "not_created"
            and request_scope["hostess_route_status"] == "not_created"
            and request_scope["live_evidence_status"] == "not_included",
            request_scope,
            {
                "repo_touch_status": "not_touched",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "live_evidence_status": "not_included",
            },
            "design review request does not touch Manifold, Hostess, route, state, audit, or live evidence",
        ),
        check(
            "route_design_review.manifold_authority",
            authority["design_review_owner"] == "rusty.manifold"
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
                "design_review_owner": "rusty.manifold",
                "route_implementation_owner": "rusty.manifold",
                "request_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "rollback_owner": "rusty.manifold",
                "sidecar_role": "observer_proposer",
            },
            "Manifold remains design review, route, request, runtime, session, audit, state, and rollback owner",
        ),
        check(
            "route_design_review.work_items_not_created",
            bool(proposed_manifold_work_items)
            and all(item["owner"] == "rusty.manifold" for item in proposed_manifold_work_items)
            and all(item["status"] == "not_created" for item in proposed_manifold_work_items)
            and all(item["acceptance_required"] is True for item in proposed_manifold_work_items),
            {
                "owners": sorted({item["owner"] for item in proposed_manifold_work_items}),
                "statuses": sorted({item["status"] for item in proposed_manifold_work_items}),
                "work_item_count": len(proposed_manifold_work_items),
            },
            {
                "owner": "rusty.manifold",
                "status": "not_created",
                "acceptance_required": True,
                "work_item_count": 6,
            },
            "all proposed work remains Manifold-owned and not created",
        ),
        check(
            "route_design_review.review_topics_cover_boundaries",
            required_topics <= observed_topics
            and proposed_manifold_review["review_owner"] == "rusty.manifold"
            and proposed_manifold_review["decision_status"] == "not_decided",
            {
                "review_owner": proposed_manifold_review["review_owner"],
                "decision_status": proposed_manifold_review["decision_status"],
                "review_topics": sorted(observed_topics),
            },
            {
                "review_owner": "rusty.manifold",
                "decision_status": "not_decided",
                "review_topics": sorted(required_topics),
            },
            "review request covers schema, decision, state, audit, Hostess, and privacy topics",
        ),
        check(
            "route_design_review.hostess_preconditions",
            hostess_integration_preconditions["status"] == "future_lane_not_requested"
            and hostess_integration_preconditions["route_status"] == "not_created"
            and hostess_integration_preconditions["device_action_authority"] == "not_in_sidecar"
            and hostess_integration_preconditions["requires_manifold_accepted_state"] is True
            and hostess_integration_preconditions["requires_explicit_operator_request"] is True
            and "command_payload" in hostess_integration_preconditions["disallowed_input_classes"]
            and "adb_target" in hostess_integration_preconditions["disallowed_input_classes"],
            hostess_integration_preconditions,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "disallows_command_and_adb_markers": True,
            },
            "Hostess stays a future lane gated by Manifold accepted state or an operator request",
        ),
        check(
            "route_design_review.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_schema_route_acceptance_and_audit"
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
                "future_manifold_gate": "manifold_repo_owns_schema_route_acceptance_and_audit",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "design review request remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": REQUEST_SCHEMA,
        "request_id": "request.manifold_route_design_review.synthetic.001",
        "generated_at": now,
        "request_status": "ready_for_manifold_route_design_review" if fail_count == 0 else "blocked",
        "source_manifold_route_blueprint": source_manifold_route_blueprint,
        "request_scope": request_scope,
        "authority": authority,
        "proposed_manifold_review": proposed_manifold_review,
        "proposed_manifold_work_items": proposed_manifold_work_items,
        "hostess_integration_preconditions": hostess_integration_preconditions,
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
            "The Manifold route design review request is descriptor evidence only; it does not touch the Manifold repo, create schemas, create a route, create accepted Manifold state, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future design review, route implementation, request acceptance, command/session/audit, revision, lease, rollback, and accepted-state authority.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot perform device actions.",
        ],
        "next_gate": "manifold_repo_design_review_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route-blueprint", required=True, help="Generated Manifold route blueprint fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output Manifold route design review request path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        request = build_request(Path(args.route_blueprint), repo_root, args.now)
        write_json(Path(args.output), request)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"prepare_manifold_route_design_review failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": request["request_status"], "check_count": request["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
