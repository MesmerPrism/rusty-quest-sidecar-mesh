#!/usr/bin/env python3
"""Generate a sidecar-owned handoff package for a future Manifold response slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


PACKAGE_SCHEMA = "rusty.quest.sidecar.manifold_response_handoff_package.v1"
PREFLIGHT_SCHEMA = "rusty.quest.sidecar.manifold_response_implementation_preflight.v1"


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


def source_artifact(path: str, schema: str, role: str) -> dict[str, Any]:
    return {
        "artifact_id": f"artifact.{Path(path).stem.replace('-', '_').replace('.synthetic', '')}",
        "path": path,
        "schema": schema,
        "role": role,
        "required_for_handoff": True,
    }


def build_package(preflight_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    preflight = load_json(preflight_path)
    preflight_result = validate_repo.validate_json_file(preflight_path)

    requirements = preflight.get("manifold_repo_slice_requirements", {})
    source_manifold_response_implementation_preflight = {
        "path": relative_output_path(preflight_path, repo_root),
        "schema": preflight.get("schema"),
        "preflight_id": preflight.get("preflight_id"),
        "preflight_status": preflight.get("preflight_status"),
        "next_gate": preflight.get("next_gate"),
    }
    package_scope = {
        "package_class": "manifold_response_slice_handoff_package",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "implementation_status": "not_created",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    authority = {
        "package_owner": "rusty.quest.sidecar_mesh",
        "handoff_acceptance_owner": "rusty.manifold",
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
    source_chain_artifacts = [
        source_artifact(
            "fixtures/valid/public-lab-artifact-drift-review.synthetic.json",
            "rusty.quest.sidecar.public_lab_artifact_drift_review.v1",
            "sanitized_public_lab_drift_evidence",
        ),
        source_artifact(
            "fixtures/valid/no-network-prototype-handoff-review.synthetic.json",
            "rusty.quest.sidecar.no_network_prototype_handoff_review.v1",
            "offline_agent_handoff_review",
        ),
        source_artifact(
            "fixtures/valid/configured-peer-rehearsal-plan.synthetic.json",
            "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1",
            "operator_approval_gated_peer_plan",
        ),
        source_artifact(
            "fixtures/valid/manifold-adapter-contract-review.synthetic.json",
            "rusty.quest.sidecar.manifold_adapter_contract_review.v1",
            "future_manifold_adapter_contract_review",
        ),
        source_artifact(
            "fixtures/valid/manifold-contract-intake-request.synthetic.json",
            "rusty.quest.sidecar.manifold_contract_intake_request.v1",
            "future_manifold_contract_intake_request",
        ),
        source_artifact(
            "fixtures/valid/private-rehearsal-approval-request.synthetic.json",
            "rusty.quest.sidecar.private_rehearsal_approval_request.v1",
            "operator_decision_packet",
        ),
        source_artifact(
            "fixtures/valid/manifold-route-blueprint.synthetic.json",
            "rusty.quest.sidecar.manifold_route_blueprint.v1",
            "future_manifold_route_blueprint",
        ),
        source_artifact(
            "fixtures/valid/manifold-route-design-review-request.synthetic.json",
            "rusty.quest.sidecar.manifold_route_design_review_request.v1",
            "future_manifold_route_design_review_request",
        ),
        source_artifact(
            "fixtures/valid/manifold-route-design-response-expectation.synthetic.json",
            "rusty.quest.sidecar.manifold_route_design_response_expectation.v1",
            "future_manifold_response_expectation",
        ),
        source_artifact(
            relative_output_path(preflight_path, repo_root),
            PREFLIGHT_SCHEMA,
            "future_manifold_response_implementation_preflight",
        ),
        source_artifact(
            "fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "rusty.quest.sidecar.integration_acceptance_scorecard.v1",
            "local_acceptance_summary",
        ),
    ]
    handoff_manifest = {
        "manifest_id": "manifest.manifold_response_slice_handoff.synthetic.001",
        "status": "candidate",
        "target_repo": "rusty.manifold",
        "source_chain_artifacts": source_chain_artifacts,
        "required_downstream_artifacts": requirements.get("required_manifold_owned_artifacts", []),
        "required_downstream_validation_slots": requirements.get("required_validation_slots", []),
        "required_downstream_decisions": requirements.get("required_response_decisions", []),
        "required_downstream_rejection_terms": requirements.get("required_rejection_terms", []),
        "required_route_boundaries": requirements.get("required_route_boundaries", {}),
        "rollback_policy": requirements.get("rollback_policy"),
        "handoff_acceptance_status": "not_accepted",
        "downstream_implementation_status": "not_created",
    }
    hostess_boundary_handoff = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "downstream_descriptor_owner": "rusty.manifold",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "handoff_result": "hostess_prepared_as_boundary_descriptor_only",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/package_manifold_response_handoff.py --preflight fixtures/valid/manifold-response-implementation-preflight.synthetic.json --now 2026-06-04T23:36:00Z --output fixtures/valid/manifold-response-handoff-package.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_response_slice_handoff_acceptance_and_implementation",
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

    source_results = [
        validate_repo.validate_json_file(repo_root / artifact["path"])
        for artifact in source_chain_artifacts
        if (repo_root / artifact["path"]).exists()
    ]
    required_source_ids = {
        "artifact.public_lab_artifact_drift_review",
        "artifact.no_network_prototype_handoff_review",
        "artifact.configured_peer_rehearsal_plan",
        "artifact.manifold_adapter_contract_review",
        "artifact.manifold_contract_intake_request",
        "artifact.private_rehearsal_approval_request",
        "artifact.manifold_route_blueprint",
        "artifact.manifold_route_design_review_request",
        "artifact.manifold_route_design_response_expectation",
        "artifact.manifold_response_implementation_preflight",
        "artifact.integration_acceptance_scorecard",
    }
    required_artifact_kinds = {
        "schema",
        "route_handler",
        "decision_event_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "hostess_boundary_descriptor",
    }
    downstream_artifacts = handoff_manifest["required_downstream_artifacts"]
    route_boundaries = handoff_manifest["required_route_boundaries"]
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

    checks = [
        check(
            "manifold_response_handoff.source_preflight_ready",
            preflight_result.ok
            and preflight.get("schema") == PREFLIGHT_SCHEMA
            and preflight.get("preflight_status") == "ready_for_manifold_repo_slice_planning"
            and preflight.get("next_gate") == "manifold_repo_response_slice_or_operator_decision",
            {
                "schema": preflight.get("schema"),
                "preflight_status": preflight.get("preflight_status"),
                "next_gate": preflight.get("next_gate"),
            },
            {
                "schema": PREFLIGHT_SCHEMA,
                "preflight_status": "ready_for_manifold_repo_slice_planning",
                "next_gate": "manifold_repo_response_slice_or_operator_decision",
            },
            relative_output_path(preflight_path, repo_root),
        ),
        check(
            "manifold_response_handoff.no_repo_response_route_or_state",
            package_scope["repo_touch_status"] == "not_touched"
            and package_scope["branch_status"] == "not_created"
            and package_scope["implementation_status"] == "not_created"
            and package_scope["response_status"] == "not_created"
            and package_scope["decision_status"] == "not_decided"
            and package_scope["route_status"] == "not_created"
            and package_scope["accepted_state_status"] == "not_created"
            and package_scope["audit_record_status"] == "not_created"
            and package_scope["hostess_route_status"] == "not_created"
            and package_scope["live_evidence_status"] == "not_included",
            package_scope,
            {
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "implementation_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "live_evidence_status": "not_included",
            },
            "package does not touch Manifold, create a branch, response, decision, route, state, audit, Hostess route, or live evidence",
        ),
        check(
            "manifold_response_handoff.manifold_authority",
            authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["implementation_plan_owner"] == "rusty.manifold"
            and authority["response_owner"] == "rusty.manifold"
            and authority["decision_owner"] == "rusty.manifold"
            and authority["route_implementation_owner"] == "rusty.manifold"
            and authority["request_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["rollback_owner"] == "rusty.manifold"
            and authority["sidecar_role"] == "observer_proposer"
            and authority["proposal_status"] == "not_accepted",
            authority,
            {
                "handoff_acceptance_owner": "rusty.manifold",
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
                "proposal_status": "not_accepted",
            },
            "Manifold remains handoff acceptance, implementation, response, route, runtime, session, audit, state, and rollback owner",
        ),
        check(
            "manifold_response_handoff.source_chain_complete",
            required_source_ids <= {artifact["artifact_id"] for artifact in source_chain_artifacts}
            and len(source_results) == len(source_chain_artifacts)
            and all(result.ok for result in source_results),
            {
                "source_artifact_ids": [artifact["artifact_id"] for artifact in source_chain_artifacts],
                "validated_source_count": len(source_results),
                "invalid_sources": [str(result.path) for result in source_results if not result.ok],
            },
            {
                "source_artifact_ids": sorted(required_source_ids),
                "validated_source_count": len(source_chain_artifacts),
                "invalid_sources": [],
            },
            "handoff package binds the validated sidecar evidence chain without copying private evidence",
        ),
        check(
            "manifold_response_handoff.downstream_artifacts_from_preflight",
            bool(downstream_artifacts)
            and required_artifact_kinds <= {artifact.get("artifact_kind") for artifact in downstream_artifacts}
            and all(artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"} for artifact in downstream_artifacts)
            and all(artifact.get("status") == "not_created_by_sidecar" for artifact in downstream_artifacts)
            and handoff_manifest["handoff_acceptance_status"] == "not_accepted"
            and handoff_manifest["downstream_implementation_status"] == "not_created",
            {
                "artifact_kinds": sorted({artifact.get("artifact_kind") for artifact in downstream_artifacts}),
                "owners": sorted({artifact.get("owner") for artifact in downstream_artifacts}),
                "statuses": sorted({artifact.get("status") for artifact in downstream_artifacts}),
                "handoff_acceptance_status": handoff_manifest["handoff_acceptance_status"],
                "downstream_implementation_status": handoff_manifest["downstream_implementation_status"],
            },
            {
                "artifact_kinds": sorted(required_artifact_kinds),
                "owners": ["rusty.manifold", "rusty.manifold.audit"],
                "status": "not_created_by_sidecar",
                "handoff_acceptance_status": "not_accepted",
                "downstream_implementation_status": "not_created",
            },
            "required downstream artifacts are copied from the preflight as Manifold-owned work, not sidecar-created work",
        ),
        check(
            "manifold_response_handoff.validation_rejection_and_route_boundaries",
            required_validation_slots <= set(handoff_manifest["required_downstream_validation_slots"])
            and set(handoff_manifest["required_downstream_decisions"]) == {"accepted_for_manifold_slice", "revision_requested", "rejected"}
            and required_rejection_terms <= set(handoff_manifest["required_downstream_rejection_terms"])
            and route_boundaries.get("input_payload_class") == "low_rate_advisory_status"
            and route_boundaries.get("allows_endpoint_values") is False
            and route_boundaries.get("allows_commands") is False
            and route_boundaries.get("allows_adb") is False
            and route_boundaries.get("allows_high_rate_payloads") is False
            and route_boundaries.get("allows_sidecar_direct_hostess_input") is False
            and handoff_manifest["rollback_policy"] == "manifold_owned_disable_route_or_reject_source",
            {
                "validation_slots": handoff_manifest["required_downstream_validation_slots"],
                "decisions": handoff_manifest["required_downstream_decisions"],
                "rejection_terms": handoff_manifest["required_downstream_rejection_terms"],
                "route_boundaries": route_boundaries,
                "rollback_policy": handoff_manifest["rollback_policy"],
            },
            {
                "validation_slots": sorted(required_validation_slots),
                "decisions": ["accepted_for_manifold_slice", "revision_requested", "rejected"],
                "rejection_terms": sorted(required_rejection_terms),
                "route_boundaries": {
                    "input_payload_class": "low_rate_advisory_status",
                    "allows_endpoint_values": False,
                    "allows_commands": False,
                    "allows_adb": False,
                    "allows_high_rate_payloads": False,
                    "allows_sidecar_direct_hostess_input": False,
                },
                "rollback_policy": "manifold_owned_disable_route_or_reject_source",
            },
            "handoff package carries the Manifold validation, rejection, route, and rollback constraints forward",
        ),
        check(
            "manifold_response_handoff.hostess_deferred",
            hostess_boundary_handoff["status"] == "future_lane_not_requested"
            and hostess_boundary_handoff["route_status"] == "not_created"
            and hostess_boundary_handoff["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary_handoff["consumes_only"] == "manifold_accepted_state_or_operator_request_descriptor"
            and hostess_boundary_handoff["sidecar_direct_input_allowed"] is False
            and hostess_boundary_handoff["requires_manifold_accepted_state"] is True
            and hostess_boundary_handoff["requires_explicit_operator_request"] is True
            and hostess_boundary_handoff["downstream_descriptor_owner"] == "rusty.manifold"
            and hostess_boundary_handoff["handoff_result"] == "hostess_prepared_as_boundary_descriptor_only",
            hostess_boundary_handoff,
            {
                "status": "future_lane_not_requested",
                "route_status": "not_created",
                "device_action_authority": "not_in_sidecar",
                "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "downstream_descriptor_owner": "rusty.manifold",
                "handoff_result": "hostess_prepared_as_boundary_descriptor_only",
            },
            "Hostess remains prepared as a boundary descriptor only, not a sidecar-driven route",
        ),
        check(
            "manifold_response_handoff.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_response_slice_handoff_acceptance_and_implementation"
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
                "future_manifold_gate": "manifold_repo_owns_response_slice_handoff_acceptance_and_implementation",
                "future_hostess_gate": "hostess_route_requires_manifold_state_or_operator_request",
                "privacy_flags_all_false": True,
                "public_fixture_policy": "synthetic_descriptor_only",
            },
            "handoff package remains public-safe descriptor evidence with validation gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": PACKAGE_SCHEMA,
        "package_id": "package.manifold_response_slice_handoff.synthetic.001",
        "generated_at": now,
        "package_status": "response_handoff_package_ready" if fail_count == 0 else "blocked",
        "source_manifold_response_implementation_preflight": source_manifold_response_implementation_preflight,
        "package_scope": package_scope,
        "authority": authority,
        "handoff_manifest": handoff_manifest,
        "hostess_boundary_handoff": hostess_boundary_handoff,
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
            "The Manifold response handoff package is descriptor evidence only; it does not touch the Manifold repo, create a branch, create a response, decide the review, create schemas, create routes, create accepted state, create audit records, touch Hostess, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future handoff acceptance, implementation plan, response, decision, route implementation, request acceptance, command/session/audit, revision, lease, rollback, and accepted-state authority.",
            "Hostess remains a future operator-recovery lane after Manifold accepted state or explicit operator request; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "manifold_repo_response_slice_or_operator_decision",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", required=True, help="Generated Manifold response implementation preflight fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output response handoff package path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        package = build_package(Path(args.preflight), repo_root, args.now)
        write_json(Path(args.output), package)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"package_manifold_response_handoff failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": package["package_status"], "check_count": package["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
