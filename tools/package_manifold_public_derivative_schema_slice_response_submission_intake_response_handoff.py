#!/usr/bin/env python3
"""Generate a sidecar-owned handoff package for future Manifold submission intake response work."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


PACKAGE_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_handoff_package.v1"
PREFLIGHT_SCHEMA = "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.v1"
PREFLIGHT_READY = "ready_for_manifold_submission_intake_response_implementation_planning"
PREFLIGHT_NEXT_GATE = "manifold_submission_intake_response_handoff_or_manifold_repo_submission_intake_response"


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


SOURCE_ARTIFACTS = [
    (
        "fixtures/valid/public-lab-artifact-drift-review.synthetic.json",
        "rusty.quest.sidecar.public_lab_artifact_drift_review.v1",
        "sanitized_public_lab_drift_evidence",
    ),
    (
        "fixtures/valid/no-network-prototype-handoff-review.synthetic.json",
        "rusty.quest.sidecar.no_network_prototype_handoff_review.v1",
        "offline_agent_handoff_review",
    ),
    (
        "fixtures/valid/configured-peer-rehearsal-plan.synthetic.json",
        "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1",
        "operator_approval_gated_peer_plan",
    ),
    (
        "fixtures/valid/manifold-adapter-contract-review.synthetic.json",
        "rusty.quest.sidecar.manifold_adapter_contract_review.v1",
        "future_manifold_adapter_contract_review",
    ),
    (
        "fixtures/valid/manifold-contract-intake-request.synthetic.json",
        "rusty.quest.sidecar.manifold_contract_intake_request.v1",
        "future_manifold_contract_intake_request",
    ),
    (
        "fixtures/valid/private-rehearsal-approval-request.synthetic.json",
        "rusty.quest.sidecar.private_rehearsal_approval_request.v1",
        "operator_decision_packet",
    ),
    (
        "fixtures/valid/private-rehearsal-evidence-expectation.synthetic.json",
        "rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1",
        "future_private_evidence_expectation",
    ),
    (
        "fixtures/valid/private-rehearsal-public-derivative-expectation.synthetic.json",
        "rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1",
        "future_public_derivative_expectation",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-request.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_request.v1",
        "future_manifold_public_derivative_schema_request",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-response-expectation.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_response_expectation.v1",
        "future_manifold_public_derivative_schema_response_expectation",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-implementation-preflight.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_implementation_preflight.v1",
        "future_manifold_public_derivative_schema_implementation_preflight",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-handoff-package.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_handoff_package.v1",
        "future_manifold_public_derivative_schema_handoff_package",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-slice-response-expectation.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_expectation.v1",
        "future_manifold_public_derivative_schema_slice_response_expectation",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_implementation_preflight.v1",
        "future_manifold_public_derivative_schema_slice_response_implementation_preflight",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_handoff_package.v1",
        "future_manifold_public_derivative_schema_slice_response_handoff_package",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1",
        "future_operator_decision_request",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.v1",
        "future_operator_decision_record_expectation",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_envelope_expectation.v1",
        "future_operator_submission_envelope_expectation",
    ),
    (
        "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json",
        "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1",
        "future_manifold_submission_intake_response_expectation",
    ),
]


def build_package(preflight_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    preflight = load_json(preflight_path)
    preflight_result = validate_repo.validate_json_file(preflight_path)
    requirements = preflight.get("manifold_repo_submission_intake_response_requirements", {})

    source_preflight = {
        "path": relative_output_path(preflight_path, repo_root),
        "schema": preflight.get("schema"),
        "preflight_id": preflight.get("preflight_id"),
        "preflight_status": preflight.get("preflight_status"),
        "next_gate": preflight.get("next_gate"),
    }
    package_scope = {
        "package_class": "manifold_submission_intake_response_handoff_package",
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
        "package_owner": "rusty.quest.sidecar_mesh",
        "handoff_acceptance_owner": "rusty.manifold",
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
    source_chain_artifacts = [
        source_artifact(path, schema, role)
        for path, schema, role in SOURCE_ARTIFACTS
    ]
    source_chain_artifacts.extend(
        [
            source_artifact(
                relative_output_path(preflight_path, repo_root),
                PREFLIGHT_SCHEMA,
                "future_manifold_submission_intake_response_implementation_preflight",
            ),
            source_artifact(
                "fixtures/valid/integration-acceptance-scorecard.synthetic.json",
                "rusty.quest.sidecar.integration_acceptance_scorecard.v1",
                "local_acceptance_summary",
            ),
        ]
    )
    handoff_manifest = {
        "manifest_id": "manifest.manifold_submission_intake_response_handoff.synthetic.001",
        "status": "candidate",
        "target_repo": "rusty.manifold",
        "source_chain_artifacts": source_chain_artifacts,
        "required_downstream_artifacts": requirements.get("required_manifold_owned_artifacts", []),
        "required_downstream_validation_slots": requirements.get("required_validation_slots", []),
        "required_downstream_decisions": requirements.get("required_response_decisions", []),
        "required_downstream_rejection_terms": requirements.get("required_rejection_terms", []),
        "required_downstream_revision_terms": requirements.get("required_revision_terms", []),
        "required_downstream_audit_terms": requirements.get("required_audit_terms", []),
        "required_route_boundaries": requirements.get("required_route_boundaries", {}),
        "rollback_policy": requirements.get("rollback_policy"),
        "handoff_acceptance_status": "not_accepted",
        "downstream_implementation_plan_status": "not_created",
        "downstream_submission_envelope_status": "not_created",
        "downstream_submission_status": "not_submitted",
        "downstream_intake_response_status": "not_created",
        "downstream_decision_status": "not_decided",
        "downstream_response_schema_status": "not_created",
        "downstream_route_status": "not_created",
        "downstream_accepted_state_status": "not_created",
        "downstream_audit_status": "not_created",
        "downstream_validation_report_status": "not_created",
        "downstream_hostess_boundary_status": "not_created",
    }
    hostess_boundary_handoff = {
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
        "handoff_result": "hostess_deferred_until_manifold_submission_intake_acceptance",
    }
    validation_evidence = {
        "local_validation_status": "expected_pass",
        "required_commands": [
            "python tools/package_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff.py --preflight fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json --now 2026-06-05T01:44:00Z --output fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-handoff-package.synthetic.json",
            "python tools/evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures/valid/integration-acceptance-scorecard.synthetic.json",
            "python tools/validate_repo.py --repo-root .",
            "python -m unittest discover -s tests -p test_*.py",
            "git diff --check",
        ],
        "damaged_fixture_policy": "must_fail_validation",
        "future_manifold_gate": "manifold_repo_owns_submission_intake_response_handoff_acceptance_and_implementation",
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

    source_results = [
        validate_repo.validate_json_file(repo_root / artifact["path"])
        for artifact in source_chain_artifacts
        if (repo_root / artifact["path"]).exists()
    ]
    required_source_ids = {source_artifact(path, schema, role)["artifact_id"] for path, schema, role in SOURCE_ARTIFACTS}
    required_source_ids.add("artifact.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight")
    required_source_ids.add("artifact.integration_acceptance_scorecard")
    route_boundaries = handoff_manifest["required_route_boundaries"]
    checks = [
        check(
            "submission_intake_response_handoff.source_preflight_ready",
            preflight_result.ok
            and preflight.get("schema") == PREFLIGHT_SCHEMA
            and preflight.get("preflight_status") == PREFLIGHT_READY
            and preflight.get("next_gate") == PREFLIGHT_NEXT_GATE,
            {
                "schema": preflight.get("schema"),
                "preflight_status": preflight.get("preflight_status"),
                "next_gate": preflight.get("next_gate"),
            },
            {
                "schema": PREFLIGHT_SCHEMA,
                "preflight_status": PREFLIGHT_READY,
                "next_gate": PREFLIGHT_NEXT_GATE,
            },
            relative_output_path(preflight_path, repo_root),
        ),
        check(
            "submission_intake_response_handoff.no_repo_submission_response_state_or_hostess",
            all(value in {"not_touched", "not_created", "not_submitted", "not_decided", "not_included", "not_used", "no_commands", "synthetic_fixture", "rusty.manifold", "manifold_submission_intake_response_handoff_package"} for value in package_scope.values()),
            package_scope,
            "no Manifold repo touch, branch, submission, response, state, audit, Hostess input, ADB, or command",
            "package scope remains descriptor-only",
        ),
        check(
            "submission_intake_response_handoff.manifold_authority",
            authority["handoff_acceptance_owner"] == "rusty.manifold"
            and authority["submission_envelope_owner"] == "operator"
            and authority["intake_response_implementation_owner"] == "rusty.manifold"
            and authority["intake_response_owner"] == "rusty.manifold"
            and authority["submission_acceptance_owner"] == "rusty.manifold"
            and authority["runtime_authority_owner"] == "rusty.manifold"
            and authority["session_authority_owner"] == "rusty.manifold"
            and authority["audit_owner"] == "rusty.manifold.audit"
            and authority["accepted_state_owner"] == "rusty.manifold"
            and authority["validation_report_owner"] == "rusty.manifold"
            and authority["hostess_device_action_authority"] == "not_in_sidecar"
            and authority["sidecar_role"] == "observer_proposer"
            and authority["proposal_status"] == "not_accepted",
            authority,
            "operator envelope; Manifold response, session, audit, state, validation; sidecar proposal only",
            "authority map",
        ),
        check(
            "submission_intake_response_handoff.source_chain_complete",
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
            "handoff package binds validated descriptor evidence without copying private evidence",
        ),
        check(
            "submission_intake_response_handoff.downstream_artifacts_from_preflight",
            bool(handoff_manifest["required_downstream_artifacts"])
            and all(artifact.get("status") == "not_created_by_sidecar" for artifact in handoff_manifest["required_downstream_artifacts"])
            and all(artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"} for artifact in handoff_manifest["required_downstream_artifacts"])
            and handoff_manifest["handoff_acceptance_status"] == "not_accepted"
            and handoff_manifest["downstream_intake_response_status"] == "not_created"
            and handoff_manifest["downstream_accepted_state_status"] == "not_created"
            and handoff_manifest["downstream_audit_status"] == "not_created"
            and handoff_manifest["downstream_validation_report_status"] == "not_created",
            handoff_manifest,
            "Manifold-owned downstream artifacts and not-created downstream state",
            "preflight requirements copied into handoff manifest",
        ),
        check(
            "submission_intake_response_handoff.validation_rejection_revision_audit_and_route_boundaries",
            set(handoff_manifest["required_downstream_decisions"]) == {"received_for_review", "request_submission_revision", "reject_submission_envelope"}
            and route_boundaries.get("input_payload_class") == "low_rate_descriptor"
            and route_boundaries.get("accepts_sanitized_summary_only") is True
            and route_boundaries.get("requires_operator_submission_envelope") is True
            and route_boundaries.get("requires_source_chain_digest") is True
            and route_boundaries.get("requires_redaction_review") is True
            and route_boundaries.get("allows_endpoint_values") is False
            and route_boundaries.get("allows_commands") is False
            and route_boundaries.get("allows_adb") is False
            and route_boundaries.get("allows_raw_logs") is False
            and route_boundaries.get("allows_visual_captures") is False
            and route_boundaries.get("allows_private_device_ids") is False
            and route_boundaries.get("allows_sidecar_direct_hostess_input") is False
            and route_boundaries.get("creates_response_by_sidecar") is False
            and route_boundaries.get("creates_accepted_state_by_sidecar") is False
            and route_boundaries.get("creates_audit_by_sidecar") is False
            and route_boundaries.get("creates_validation_report_by_sidecar") is False
            and route_boundaries.get("creates_hostess_input") is False
            and handoff_manifest["rollback_policy"] == "manifold_owned_reject_submission_or_request_revision",
            {
                "decisions": handoff_manifest["required_downstream_decisions"],
                "route_boundaries": route_boundaries,
                "rollback_policy": handoff_manifest["rollback_policy"],
            },
            "low-rate sanitized descriptor route with Manifold-owned reject/revision/rollback",
            "handoff package carries preflight route constraints forward",
        ),
        check(
            "submission_intake_response_handoff.hostess_deferred",
            hostess_boundary_handoff["status"] == "future_lane_not_requested"
            and hostess_boundary_handoff["route_status"] == "not_created"
            and hostess_boundary_handoff["input_status"] == "not_created"
            and hostess_boundary_handoff["device_action_authority"] == "not_in_sidecar"
            and hostess_boundary_handoff["consumes_only"] == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and hostess_boundary_handoff["sidecar_direct_input_allowed"] is False
            and hostess_boundary_handoff["requires_manifold_accepted_state"] is True
            and hostess_boundary_handoff["requires_explicit_operator_request"] is True,
            hostess_boundary_handoff,
            "Hostess deferred until Manifold accepted state or explicit operator request descriptor",
            "Hostess remains downstream boundary only",
        ),
        check(
            "submission_intake_response_handoff.privacy_and_validation_boundary",
            validation_evidence["local_validation_status"] == "expected_pass"
            and validation_evidence["damaged_fixture_policy"] == "must_fail_validation"
            and validation_evidence["future_manifold_gate"] == "manifold_repo_owns_submission_intake_response_handoff_acceptance_and_implementation"
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
            ),
            {
                "validation_evidence": validation_evidence,
                "privacy_boundary": privacy_boundary,
            },
            "public-safe synthetic descriptor with damaged fixture validation",
            "privacy and validation boundary",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": PACKAGE_SCHEMA,
        "package_id": "package.manifold_submission_intake_response_handoff.synthetic.001",
        "generated_at": now,
        "package_status": "submission_intake_response_handoff_package_ready" if fail_count == 0 else "blocked",
        "source_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight": source_preflight,
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
            "The submission intake response handoff package is descriptor evidence only; it does not touch the Manifold repo, create a branch, create an implementation plan, create a submission envelope, submit a package, create an intake response, decide the submission, create schemas, create routes, create accepted state, create audit records, create validation reports, create public derivative artifacts, touch Hostess, create Hostess input, start live Quest work, use ADB, open sockets, select endpoints, install, launch, recover, copy files, or execute commands.",
            "Manifold remains the future handoff acceptance, intake response implementation, submission acceptance, decision, route, command/session/audit, validation-report, rollback, source-chain, redaction-validation, and accepted-state authority.",
            "The operator remains responsible for any future submission envelope and redaction inputs before Manifold can receive, accept, reject, or revise the submission.",
            "Hostess remains a future operator/recovery lane after Manifold accepted state or a separate explicit operator request descriptor; sidecar agents cannot supply direct Hostess device-action input.",
        ],
        "next_gate": "manifold_repo_submission_intake_response_or_operator_submission_envelope",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", required=True, help="Generated submission intake response implementation preflight fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output submission intake response handoff package path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        package = build_package(Path(args.preflight), repo_root, args.now)
        write_json(Path(args.output), package)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"package_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": package["package_status"], "check_count": package["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
