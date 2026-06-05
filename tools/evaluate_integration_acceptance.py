#!/usr/bin/env python3
"""Generate the sidecar integration acceptance scorecard from local fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=2)
        handle.write("\n")


def check(check_id: str, passed: bool, observed: Any, expected: Any, evidence: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "pass" if passed else "fail",
        "observed": observed,
        "expected": expected,
        "evidence": evidence,
    }


def build_scorecard(repo_root: Path, now: str) -> dict[str, Any]:
    intake = load_json(repo_root / "fixtures" / "valid" / "public-lab-artifact-intake-report.synthetic.json")
    intake_drift_review = load_json(repo_root / "fixtures" / "valid" / "public-lab-artifact-drift-review.synthetic.json")
    adapter = load_json(repo_root / "fixtures" / "valid" / "manifold-adapter-proposal.synthetic.json")
    handoff = load_json(repo_root / "fixtures" / "valid" / "mesh-handoff.with-public-lab-intake.synthetic.json")
    recipe = load_json(repo_root / "fixtures" / "valid" / "no-network-agent-recipe.synthetic.json")
    recipe_review = load_json(repo_root / "fixtures" / "valid" / "no-network-agent-recipe-review.synthetic.json")
    prototype_run = load_json(repo_root / "fixtures" / "valid" / "no-network-agent-run.synthetic.json")
    prototype_observation = load_json(repo_root / "fixtures" / "valid" / "no-network-agent-observation.synthetic.json")
    prototype_handoff_review = load_json(repo_root / "fixtures" / "valid" / "no-network-prototype-handoff-review.synthetic.json")
    peer_rehearsal_plan = load_json(repo_root / "fixtures" / "valid" / "configured-peer-rehearsal-plan.synthetic.json")
    manifold_contract_review = load_json(repo_root / "fixtures" / "valid" / "manifold-adapter-contract-review.synthetic.json")
    manifold_handoff_package = load_json(repo_root / "fixtures" / "valid" / "manifold-handoff-package.synthetic.json")
    manifold_contract_intake_request = load_json(repo_root / "fixtures" / "valid" / "manifold-contract-intake-request.synthetic.json")
    private_rehearsal_approval_request = load_json(repo_root / "fixtures" / "valid" / "private-rehearsal-approval-request.synthetic.json")
    manifold_route_blueprint = load_json(repo_root / "fixtures" / "valid" / "manifold-route-blueprint.synthetic.json")
    manifold_route_design_review_request = load_json(repo_root / "fixtures" / "valid" / "manifold-route-design-review-request.synthetic.json")
    manifold_route_design_response_expectation = load_json(repo_root / "fixtures" / "valid" / "manifold-route-design-response-expectation.synthetic.json")
    manifold_response_implementation_preflight = load_json(repo_root / "fixtures" / "valid" / "manifold-response-implementation-preflight.synthetic.json")
    manifold_response_handoff_package = load_json(repo_root / "fixtures" / "valid" / "manifold-response-handoff-package.synthetic.json")
    hostess_boundary_descriptor_expectation = load_json(repo_root / "fixtures" / "valid" / "hostess-boundary-descriptor-expectation.synthetic.json")
    private_rehearsal_evidence_expectation = load_json(repo_root / "fixtures" / "valid" / "private-rehearsal-evidence-expectation.synthetic.json")
    private_rehearsal_public_derivative_expectation = load_json(repo_root / "fixtures" / "valid" / "private-rehearsal-public-derivative-expectation.synthetic.json")
    manifold_public_derivative_schema_request = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-request.synthetic.json")
    manifold_public_derivative_schema_response_expectation = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-response-expectation.synthetic.json")
    manifold_public_derivative_schema_implementation_preflight = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-implementation-preflight.synthetic.json")
    manifold_public_derivative_schema_handoff_package = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-handoff-package.synthetic.json")
    manifold_public_derivative_schema_slice_response_expectation = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-expectation.synthetic.json")
    manifold_public_derivative_schema_slice_response_implementation_preflight = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json")
    manifold_public_derivative_schema_slice_response_handoff_package = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json")
    manifold_public_derivative_schema_slice_response_operator_decision_request = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json")
    manifold_public_derivative_schema_slice_response_operator_decision_record_expectation = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json")
    manifold_public_derivative_schema_slice_response_submission_envelope_expectation = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json")
    manifold_public_derivative_schema_slice_response_submission_intake_response_expectation = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json")
    manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight = load_json(repo_root / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json")
    missing, valid_results, damaged_results = validate_repo.validate_repo(repo_root)

    intake_summary = intake.get("summary", {})
    authority = adapter.get("authority", {})
    adapter_surfaces = adapter.get("adapter_surfaces", [])
    handoff_required = set(handoff.get("approval", {}).get("required_by", []))
    damaged_failures = [result for result in damaged_results if not result.ok]
    valid_failures = [result for result in valid_results if not result.ok]
    public_derivative_preflight_requirements = manifold_public_derivative_schema_implementation_preflight.get("manifold_repo_slice_requirements", {})
    public_derivative_preflight_artifacts = public_derivative_preflight_requirements.get("required_manifold_owned_artifacts", [])
    public_derivative_preflight_route_boundaries = public_derivative_preflight_requirements.get("required_route_boundaries", {})
    public_derivative_handoff_manifest = manifold_public_derivative_schema_handoff_package.get("handoff_manifest", {})
    public_derivative_handoff_artifacts = public_derivative_handoff_manifest.get("required_downstream_artifacts", [])
    public_derivative_handoff_route_boundaries = public_derivative_handoff_manifest.get("required_route_boundaries", {})
    public_derivative_slice_response = manifold_public_derivative_schema_slice_response_expectation.get("expected_manifold_slice_response", {})
    public_derivative_slice_response_preflight_requirements = manifold_public_derivative_schema_slice_response_implementation_preflight.get("manifold_repo_slice_response_requirements", {})
    public_derivative_slice_response_preflight_artifacts = public_derivative_slice_response_preflight_requirements.get("required_manifold_owned_artifacts", [])
    public_derivative_slice_response_preflight_route_boundaries = public_derivative_slice_response_preflight_requirements.get("required_route_boundaries", {})
    public_derivative_slice_response_handoff_manifest = manifold_public_derivative_schema_slice_response_handoff_package.get("handoff_manifest", {})
    public_derivative_slice_response_handoff_artifacts = public_derivative_slice_response_handoff_manifest.get("required_downstream_artifacts", [])
    public_derivative_slice_response_handoff_route_boundaries = public_derivative_slice_response_handoff_manifest.get("required_route_boundaries", {})
    public_derivative_slice_response_operator_decision_scope = manifold_public_derivative_schema_slice_response_operator_decision_request.get("decision_request_scope", {})
    public_derivative_slice_response_operator_decision_manifold_gate = manifold_public_derivative_schema_slice_response_operator_decision_request.get("manifold_submission_gate", {})
    public_derivative_slice_response_operator_decision_hostess_gate = manifold_public_derivative_schema_slice_response_operator_decision_request.get("hostess_boundary_gate", {})
    public_derivative_slice_response_operator_record_scope = manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("expectation_scope", {})
    public_derivative_slice_response_operator_record = manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("expected_operator_decision_record", {})
    public_derivative_slice_response_operator_record_manifold_gate = manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("manifold_submission_after_decision", {})
    public_derivative_slice_response_operator_record_hostess_gate = manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("hostess_boundary_after_decision", {})
    public_derivative_slice_response_submission_envelope_scope = manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("expectation_scope", {})
    public_derivative_slice_response_submission_envelope = manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("expected_submission_envelope", {})
    public_derivative_slice_response_submission_envelope_manifold_gate = manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("manifold_intake_after_envelope", {})
    public_derivative_slice_response_submission_envelope_hostess_gate = manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("hostess_boundary_after_envelope", {})
    public_derivative_slice_response_submission_intake_scope = manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("expectation_scope", {})
    public_derivative_slice_response_submission_intake_response = manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("expected_manifold_intake_response", {})
    public_derivative_slice_response_submission_intake_manifold_gate = manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("manifold_acceptance_after_response", {})
    public_derivative_slice_response_submission_intake_hostess_gate = manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("hostess_boundary_after_response", {})
    public_derivative_slice_response_submission_intake_preflight_scope = manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("implementation_preflight_scope", {})
    public_derivative_slice_response_submission_intake_preflight_requirements = manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("manifold_repo_submission_intake_response_requirements", {})
    public_derivative_slice_response_submission_intake_preflight_artifacts = public_derivative_slice_response_submission_intake_preflight_requirements.get("required_manifold_owned_artifacts", [])
    public_derivative_slice_response_submission_intake_preflight_route_boundaries = public_derivative_slice_response_submission_intake_preflight_requirements.get("required_route_boundaries", {})
    public_derivative_slice_response_submission_intake_preflight_hostess_gate = manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("hostess_boundary_preflight", {})

    checks = [
        check(
            "intake.overall_status",
            intake.get("overall_status") == "intake_ready",
            intake.get("overall_status"),
            "intake_ready",
            "fixtures/valid/public-lab-artifact-intake-report.synthetic.json",
        ),
        check(
            "intake.expected_blocked_artifacts",
            intake_summary.get("expected_blocked_artifact_count", 0) >= 1,
            intake_summary.get("expected_blocked_artifact_count", 0),
            ">=1",
            "public lab intake preserves blocked private-result and baseline scorecard lanes as expected blocked evidence",
        ),
        check(
            "intake.ready_artifacts",
            intake_summary.get("ready_artifact_count", 0) >= 3,
            intake_summary.get("ready_artifact_count", 0),
            ">=3",
            "public lab intake carries package, review, file-drop copy, and inbox intake ready lanes",
        ),
        check(
            "intake.drift_review_clear",
            intake_drift_review.get("drift_status") == "drift_clear"
            and intake_drift_review.get("summary", {}).get("drifted_artifact_count") == 0
            and intake_drift_review.get("summary", {}).get("fail_count") == 0
            and intake_drift_review.get("summary", {}).get("artifact_count") == intake_summary.get("artifact_count"),
            {
                "drift_status": intake_drift_review.get("drift_status"),
                "drifted_artifact_count": intake_drift_review.get("summary", {}).get("drifted_artifact_count"),
                "fail_count": intake_drift_review.get("summary", {}).get("fail_count"),
                "review_artifact_count": intake_drift_review.get("summary", {}).get("artifact_count"),
                "intake_artifact_count": intake_summary.get("artifact_count"),
            },
            {
                "drift_status": "drift_clear",
                "drifted_artifact_count": 0,
                "fail_count": 0,
                "review_artifact_count": intake_summary.get("artifact_count"),
            },
            "public lab artifact drift review confirms stored intake still matches current sanitized source artifacts",
        ),
        check(
            "intake.drift_review_preserves_sanitized_boundary",
            intake_drift_review.get("source_access_policy", {}).get("copy_raw_artifact") is False
            and intake_drift_review.get("source_access_policy", {}).get("execute_source_validation") is False
            and intake_drift_review.get("source_access_policy", {}).get("read_private_evidence") is False
            and intake_drift_review.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and intake_drift_review.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and not any(
                intake_drift_review.get("privacy_boundary", {}).get(key)
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
                "source_access_policy": intake_drift_review.get("source_access_policy", {}),
                "handoff_acceptance_owner": intake_drift_review.get("authority", {}).get("handoff_acceptance_owner"),
                "audit_owner": intake_drift_review.get("authority", {}).get("audit_owner"),
                "privacy_boundary": intake_drift_review.get("privacy_boundary", {}),
            },
            {
                "copy_raw_artifact": False,
                "execute_source_validation": False,
                "read_private_evidence": False,
                "handoff_acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "privacy_flags_all_false": True,
            },
            "public lab drift review preserves the sanitized source-intake boundary and Manifold authority",
        ),
        check(
            "adapter.proposal_status",
            authority.get("proposal_status") == "not_accepted",
            authority.get("proposal_status"),
            "not_accepted",
            "fixtures/valid/manifold-adapter-proposal.synthetic.json",
        ),
        check(
            "adapter.acceptance_owner",
            bool(adapter_surfaces) and all(surface.get("acceptance_owner") == "rusty.manifold" for surface in adapter_surfaces),
            "rusty.manifold" if adapter_surfaces and all(surface.get("acceptance_owner") == "rusty.manifold" for surface in adapter_surfaces) else "mixed",
            "rusty.manifold",
            "all adapter surfaces declare Manifold acceptance ownership",
        ),
        check(
            "handoff.manifold_required",
            "rusty.manifold" in handoff_required,
            "required" if "rusty.manifold" in handoff_required else "missing",
            "required",
            "handoff fixtures require rusty.manifold approval",
        ),
        check(
            "damaged.boundary_fixtures",
            len(damaged_failures) >= 3 and not [result for result in damaged_results if result.ok],
            len(damaged_failures),
            ">=3",
            "damaged fixtures are expected validation failures",
        ),
        check(
            "authority.no_runtime_route",
            not missing and not valid_failures and authority.get("proposal_status") == "not_accepted" and handoff.get("audit", {}).get("accepted_mutation_record") == "not_created",
            "proposal_only",
            "proposal_only",
            "no fixture marks sidecar, adapter proposal, or handoff as accepted live state",
        ),
        check(
            "recipe.no_network_boundary",
            recipe.get("execution", {}).get("network_policy") == "no_inbound_listener"
            and recipe.get("execution", {}).get("adb_policy") == "no_adb"
            and recipe.get("execution", {}).get("command_policy") == "no_commands",
            "no_network_no_adb_no_commands",
            "no_network_no_adb_no_commands",
            "no-network agent recipe is a recipe-only observation-file boundary",
        ),
        check(
            "recipe.review_ready",
            recipe_review.get("review_status") == "ready_for_no_network_prototype"
            and recipe_review.get("summary", {}).get("fail_count") == 0
            and recipe_review.get("next_gate") == "private_no_network_termux_agent_prototype_without_transport_or_adb",
            {
                "review_status": recipe_review.get("review_status"),
                "fail_count": recipe_review.get("summary", {}).get("fail_count"),
                "next_gate": recipe_review.get("next_gate"),
            },
            {
                "review_status": "ready_for_no_network_prototype",
                "fail_count": 0,
                "next_gate": "private_no_network_termux_agent_prototype_without_transport_or_adb",
            },
            "no-network recipe review is generated and keeps the next gate no-network/no-ADB",
        ),
        check(
            "prototype.no_network_run_complete",
            prototype_run.get("prototype_status") == "prototype_complete"
            and prototype_run.get("summary", {}).get("fail_count") == 0
            and prototype_run.get("runtime", {}).get("network_policy") == "no_inbound_listener"
            and prototype_run.get("runtime", {}).get("adb_policy") == "no_adb"
            and prototype_run.get("runtime", {}).get("command_policy") == "no_commands",
            {
                "prototype_status": prototype_run.get("prototype_status"),
                "fail_count": prototype_run.get("summary", {}).get("fail_count"),
                "network_policy": prototype_run.get("runtime", {}).get("network_policy"),
                "adb_policy": prototype_run.get("runtime", {}).get("adb_policy"),
                "command_policy": prototype_run.get("runtime", {}).get("command_policy"),
            },
            {
                "prototype_status": "prototype_complete",
                "fail_count": 0,
                "network_policy": "no_inbound_listener",
                "adb_policy": "no_adb",
                "command_policy": "no_commands",
            },
            "no-network prototype generated local observation evidence only",
        ),
        check(
            "prototype.handoff_prepared_for_manifold_hostess",
            prototype_run.get("handoff_readiness", {}).get("manifold_observation_intake", {}).get("authority_owner") == "rusty.manifold"
            and prototype_run.get("handoff_readiness", {}).get("manifold_observation_intake", {}).get("audit_owner") == "rusty.manifold.audit"
            and prototype_run.get("handoff_readiness", {}).get("hostess_operator_recovery", {}).get("status") == "future_lane_not_requested"
            and prototype_run.get("handoff_readiness", {}).get("hostess_operator_recovery", {}).get("device_action_authority") == "not_in_sidecar",
            {
                "manifold_authority_owner": prototype_run.get("handoff_readiness", {}).get("manifold_observation_intake", {}).get("authority_owner"),
                "manifold_audit_owner": prototype_run.get("handoff_readiness", {}).get("manifold_observation_intake", {}).get("audit_owner"),
                "hostess_status": prototype_run.get("handoff_readiness", {}).get("hostess_operator_recovery", {}).get("status"),
                "hostess_device_action_authority": prototype_run.get("handoff_readiness", {}).get("hostess_operator_recovery", {}).get("device_action_authority"),
            },
            {
                "manifold_authority_owner": "rusty.manifold",
                "manifold_audit_owner": "rusty.manifold.audit",
                "hostess_status": "future_lane_not_requested",
                "hostess_device_action_authority": "not_in_sidecar",
            },
            "prototype report carries future Manifold intake/audit and Hostess operator-recovery routing without live integration",
        ),
        check(
            "prototype.observation_valid",
            prototype_observation.get("schema") == "rusty.quest.sidecar.observation.v1"
            and prototype_observation.get("advisory", {}).get("truth_level") == "advisory_cached_view"
            and prototype_observation.get("redaction", {}).get("contains_endpoint_values") is False,
            {
                "schema": prototype_observation.get("schema"),
                "truth_level": prototype_observation.get("advisory", {}).get("truth_level"),
                "contains_endpoint_values": prototype_observation.get("redaction", {}).get("contains_endpoint_values"),
            },
            {
                "schema": "rusty.quest.sidecar.observation.v1",
                "truth_level": "advisory_cached_view",
                "contains_endpoint_values": False,
            },
            "generated prototype observation remains advisory and redacted",
        ),
        check(
            "prototype.handoff_review_ready",
            prototype_handoff_review.get("review_status") == "handoff_review_ready"
            and prototype_handoff_review.get("summary", {}).get("fail_count") == 0
            and prototype_handoff_review.get("next_gate") == "private_configured_peer_rehearsal_requires_operator_approval",
            {
                "review_status": prototype_handoff_review.get("review_status"),
                "fail_count": prototype_handoff_review.get("summary", {}).get("fail_count"),
                "next_gate": prototype_handoff_review.get("next_gate"),
            },
            {
                "review_status": "handoff_review_ready",
                "fail_count": 0,
                "next_gate": "private_configured_peer_rehearsal_requires_operator_approval",
            },
            "no-network prototype handoff review maps future Manifold/Hostess fields before peer rehearsal",
        ),
        check(
            "prototype.handoff_review_no_live_integration",
            not any(prototype_handoff_review.get("integration_status", {}).values())
            and prototype_handoff_review.get("manifold_mapping", {}).get("authority_owner") == "rusty.manifold"
            and prototype_handoff_review.get("hostess_mapping", {}).get("device_action_authority") == "not_in_sidecar",
            {
                "integration_status": prototype_handoff_review.get("integration_status", {}),
                "manifold_authority_owner": prototype_handoff_review.get("manifold_mapping", {}).get("authority_owner"),
                "hostess_device_action_authority": prototype_handoff_review.get("hostess_mapping", {}).get("device_action_authority"),
            },
            {
                "integration_status_all_false": True,
                "manifold_authority_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
            },
            "handoff review proves Hostess/Manifold readiness metadata without touching live repos or sidecar authority",
        ),
        check(
            "peer_rehearsal.plan_requires_operator_approval",
            peer_rehearsal_plan.get("plan_status") == "operator_approval_required"
            and peer_rehearsal_plan.get("summary", {}).get("fail_count") == 0
            and peer_rehearsal_plan.get("authority", {}).get("operator_approval_required") is True
            and peer_rehearsal_plan.get("transport_policy", {}).get("route_started") is False
            and peer_rehearsal_plan.get("next_gate") == "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract",
            {
                "plan_status": peer_rehearsal_plan.get("plan_status"),
                "fail_count": peer_rehearsal_plan.get("summary", {}).get("fail_count"),
                "operator_approval_required": peer_rehearsal_plan.get("authority", {}).get("operator_approval_required"),
                "route_started": peer_rehearsal_plan.get("transport_policy", {}).get("route_started"),
                "next_gate": peer_rehearsal_plan.get("next_gate"),
            },
            {
                "plan_status": "operator_approval_required",
                "fail_count": 0,
                "operator_approval_required": True,
                "route_started": False,
                "next_gate": "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract",
            },
            "configured peer rehearsal is prepared as an approval-gated descriptor, not a started route",
        ),
        check(
            "peer_rehearsal.prepared_for_manifold_hostess_without_authority_drift",
            peer_rehearsal_plan.get("manifold_readiness", {}).get("authority_owner") == "rusty.manifold"
            and peer_rehearsal_plan.get("manifold_readiness", {}).get("audit_owner") == "rusty.manifold.audit"
            and peer_rehearsal_plan.get("manifold_readiness", {}).get("acceptance_status") == "not_implemented"
            and peer_rehearsal_plan.get("hostess_readiness", {}).get("status") == "future_lane_not_requested"
            and peer_rehearsal_plan.get("hostess_readiness", {}).get("device_action_authority") == "not_in_sidecar"
            and peer_rehearsal_plan.get("transport_policy", {}).get("fixture_contains_endpoint_values") is False
            and peer_rehearsal_plan.get("transport_policy", {}).get("commands_allowed") is False
            and peer_rehearsal_plan.get("transport_policy", {}).get("adb_allowed") is False,
            {
                "manifold_authority_owner": peer_rehearsal_plan.get("manifold_readiness", {}).get("authority_owner"),
                "manifold_audit_owner": peer_rehearsal_plan.get("manifold_readiness", {}).get("audit_owner"),
                "manifold_acceptance_status": peer_rehearsal_plan.get("manifold_readiness", {}).get("acceptance_status"),
                "hostess_status": peer_rehearsal_plan.get("hostess_readiness", {}).get("status"),
                "hostess_device_action_authority": peer_rehearsal_plan.get("hostess_readiness", {}).get("device_action_authority"),
                "fixture_contains_endpoint_values": peer_rehearsal_plan.get("transport_policy", {}).get("fixture_contains_endpoint_values"),
                "commands_allowed": peer_rehearsal_plan.get("transport_policy", {}).get("commands_allowed"),
                "adb_allowed": peer_rehearsal_plan.get("transport_policy", {}).get("adb_allowed"),
            },
            {
                "manifold_authority_owner": "rusty.manifold",
                "manifold_audit_owner": "rusty.manifold.audit",
                "manifold_acceptance_status": "not_implemented",
                "hostess_status": "future_lane_not_requested",
                "hostess_device_action_authority": "not_in_sidecar",
                "fixture_contains_endpoint_values": False,
                "commands_allowed": False,
                "adb_allowed": False,
            },
            "configured peer rehearsal prepares Manifold/Hostess integration fields while preserving sidecar observer scope",
        ),
        check(
            "manifold_contract.review_ready",
            manifold_contract_review.get("review_status") == "contract_ready"
            and manifold_contract_review.get("summary", {}).get("fail_count") == 0
            and manifold_contract_review.get("contract_scope", {}).get("implementation_status") == "not_implemented"
            and manifold_contract_review.get("contract_scope", {}).get("route_status") == "not_created"
            and manifold_contract_review.get("contract_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_contract_review.get("next_gate") == "manifold_owned_adapter_contract_or_operator_approved_private_rehearsal_evidence",
            {
                "review_status": manifold_contract_review.get("review_status"),
                "fail_count": manifold_contract_review.get("summary", {}).get("fail_count"),
                "implementation_status": manifold_contract_review.get("contract_scope", {}).get("implementation_status"),
                "route_status": manifold_contract_review.get("contract_scope", {}).get("route_status"),
                "accepted_state_status": manifold_contract_review.get("contract_scope", {}).get("accepted_state_status"),
                "next_gate": manifold_contract_review.get("next_gate"),
            },
            {
                "review_status": "contract_ready",
                "fail_count": 0,
                "implementation_status": "not_implemented",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "next_gate": "manifold_owned_adapter_contract_or_operator_approved_private_rehearsal_evidence",
            },
            "Manifold adapter contract review is ready as descriptor evidence only",
        ),
        check(
            "manifold_contract.preserves_manifold_hostess_boundaries",
            not any(manifold_contract_review.get("integration_status", {}).values())
            and manifold_contract_review.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_contract_review.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_contract_review.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_contract_review.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_contract_review.get("hostess_boundary", {}).get("status") == "future_lane_not_requested"
            and manifold_contract_review.get("hostess_boundary", {}).get("device_action_authority") == "not_in_sidecar"
            and "commands_rejected" in manifold_contract_review.get("proposed_manifold_contract", {}).get("required_rejection_terms", [])
            and "adb_rejected" in manifold_contract_review.get("proposed_manifold_contract", {}).get("required_rejection_terms", []),
            {
                "integration_status": manifold_contract_review.get("integration_status", {}),
                "runtime_authority_owner": manifold_contract_review.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_contract_review.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_contract_review.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_contract_review.get("authority", {}).get("accepted_state_owner"),
                "hostess_status": manifold_contract_review.get("hostess_boundary", {}).get("status"),
                "hostess_device_action_authority": manifold_contract_review.get("hostess_boundary", {}).get("device_action_authority"),
                "required_rejection_terms": manifold_contract_review.get("proposed_manifold_contract", {}).get("required_rejection_terms", []),
            },
            {
                "integration_status_all_false": True,
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_status": "future_lane_not_requested",
                "hostess_device_action_authority": "not_in_sidecar",
                "requires_commands_and_adb_rejection": True,
            },
            "Manifold adapter contract review preserves Manifold authority and Hostess descriptor-only recovery boundary",
        ),
        check(
            "manifold_handoff_package.ready",
            manifold_handoff_package.get("package_status") == "handoff_package_ready"
            and manifold_handoff_package.get("summary", {}).get("fail_count") == 0
            and manifold_handoff_package.get("package_scope", {}).get("route_status") == "not_created"
            and manifold_handoff_package.get("package_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_handoff_package.get("package_scope", {}).get("live_evidence_status") == "not_included"
            and manifold_handoff_package.get("next_gate") == "manifold_repo_contract_intake_or_operator_approved_private_rehearsal_evidence",
            {
                "package_status": manifold_handoff_package.get("package_status"),
                "fail_count": manifold_handoff_package.get("summary", {}).get("fail_count"),
                "route_status": manifold_handoff_package.get("package_scope", {}).get("route_status"),
                "accepted_state_status": manifold_handoff_package.get("package_scope", {}).get("accepted_state_status"),
                "live_evidence_status": manifold_handoff_package.get("package_scope", {}).get("live_evidence_status"),
                "next_gate": manifold_handoff_package.get("next_gate"),
            },
            {
                "package_status": "handoff_package_ready",
                "fail_count": 0,
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "live_evidence_status": "not_included",
                "next_gate": "manifold_repo_contract_intake_or_operator_approved_private_rehearsal_evidence",
            },
            "Manifold handoff package is ready as descriptor evidence only",
        ),
        check(
            "manifold_handoff_package.preserves_authority_and_privacy",
            manifold_handoff_package.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_handoff_package.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_handoff_package.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_handoff_package.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_handoff_package.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_handoff_package.get("hostess_boundary", {}).get("device_action_authority") == "not_in_sidecar"
            and not any(
                manifold_handoff_package.get("privacy_boundary", {}).get(key)
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
                "handoff_acceptance_owner": manifold_handoff_package.get("authority", {}).get("handoff_acceptance_owner"),
                "runtime_authority_owner": manifold_handoff_package.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_handoff_package.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_handoff_package.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_handoff_package.get("authority", {}).get("accepted_state_owner"),
                "hostess_device_action_authority": manifold_handoff_package.get("hostess_boundary", {}).get("device_action_authority"),
                "privacy_boundary": manifold_handoff_package.get("privacy_boundary", {}),
            },
            {
                "handoff_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "privacy_flags_all_false": True,
            },
            "Manifold handoff package preserves Manifold authority, Hostess boundary, and public-safe privacy",
        ),
        check(
            "manifold_contract_intake_request.ready",
            manifold_contract_intake_request.get("request_status") == "ready_for_manifold_contract_intake"
            and manifold_contract_intake_request.get("summary", {}).get("fail_count") == 0
            and manifold_contract_intake_request.get("request_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_contract_intake_request.get("request_scope", {}).get("route_status") == "not_created"
            and manifold_contract_intake_request.get("request_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_contract_intake_request.get("request_scope", {}).get("live_evidence_status") == "not_included"
            and manifold_contract_intake_request.get("next_gate") == "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence",
            {
                "request_status": manifold_contract_intake_request.get("request_status"),
                "fail_count": manifold_contract_intake_request.get("summary", {}).get("fail_count"),
                "repo_touch_status": manifold_contract_intake_request.get("request_scope", {}).get("repo_touch_status"),
                "route_status": manifold_contract_intake_request.get("request_scope", {}).get("route_status"),
                "accepted_state_status": manifold_contract_intake_request.get("request_scope", {}).get("accepted_state_status"),
                "live_evidence_status": manifold_contract_intake_request.get("request_scope", {}).get("live_evidence_status"),
                "next_gate": manifold_contract_intake_request.get("next_gate"),
            },
            {
                "request_status": "ready_for_manifold_contract_intake",
                "fail_count": 0,
                "repo_touch_status": "not_touched",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "live_evidence_status": "not_included",
                "next_gate": "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence",
            },
            "Manifold contract intake request is ready as descriptor evidence only",
        ),
        check(
            "manifold_contract_intake_request.preserves_authority_and_privacy",
            manifold_contract_intake_request.get("authority", {}).get("intake_acceptance_owner") == "rusty.manifold"
            and manifold_contract_intake_request.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_contract_intake_request.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_contract_intake_request.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_contract_intake_request.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_contract_intake_request.get("hostess_boundary", {}).get("device_action_authority") == "not_in_sidecar"
            and not any(
                manifold_contract_intake_request.get("privacy_boundary", {}).get(key)
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
                "intake_acceptance_owner": manifold_contract_intake_request.get("authority", {}).get("intake_acceptance_owner"),
                "runtime_authority_owner": manifold_contract_intake_request.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_contract_intake_request.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_contract_intake_request.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_contract_intake_request.get("authority", {}).get("accepted_state_owner"),
                "hostess_device_action_authority": manifold_contract_intake_request.get("hostess_boundary", {}).get("device_action_authority"),
                "privacy_boundary": manifold_contract_intake_request.get("privacy_boundary", {}),
            },
            {
                "intake_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "privacy_flags_all_false": True,
            },
            "Manifold contract intake request preserves Manifold authority, Hostess boundary, and public-safe privacy",
        ),
        check(
            "private_rehearsal_approval_request.requires_operator_decision",
            private_rehearsal_approval_request.get("request_status") == "operator_approval_required"
            and private_rehearsal_approval_request.get("summary", {}).get("fail_count") == 0
            and private_rehearsal_approval_request.get("approval_scope", {}).get("operator_approval_status") == "not_recorded"
            and private_rehearsal_approval_request.get("approval_scope", {}).get("route_status") == "not_started"
            and private_rehearsal_approval_request.get("approval_scope", {}).get("accepted_state_status") == "not_created"
            and private_rehearsal_approval_request.get("operator_packet", {}).get("approval_decision") == "not_recorded"
            and private_rehearsal_approval_request.get("next_gate") == "operator_decision_or_manifold_repo_owned_contract_schema",
            {
                "request_status": private_rehearsal_approval_request.get("request_status"),
                "fail_count": private_rehearsal_approval_request.get("summary", {}).get("fail_count"),
                "operator_approval_status": private_rehearsal_approval_request.get("approval_scope", {}).get("operator_approval_status"),
                "route_status": private_rehearsal_approval_request.get("approval_scope", {}).get("route_status"),
                "accepted_state_status": private_rehearsal_approval_request.get("approval_scope", {}).get("accepted_state_status"),
                "approval_decision": private_rehearsal_approval_request.get("operator_packet", {}).get("approval_decision"),
                "next_gate": private_rehearsal_approval_request.get("next_gate"),
            },
            {
                "request_status": "operator_approval_required",
                "fail_count": 0,
                "operator_approval_status": "not_recorded",
                "route_status": "not_started",
                "accepted_state_status": "not_created",
                "approval_decision": "not_recorded",
                "next_gate": "operator_decision_or_manifold_repo_owned_contract_schema",
            },
            "private rehearsal approval request is a descriptor requiring an operator decision before route start",
        ),
        check(
            "private_rehearsal_approval_request.preserves_manifold_hostess_boundaries",
            private_rehearsal_approval_request.get("authority", {}).get("approval_owner") == "operator"
            and private_rehearsal_approval_request.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and private_rehearsal_approval_request.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and private_rehearsal_approval_request.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and private_rehearsal_approval_request.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and private_rehearsal_approval_request.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and private_rehearsal_approval_request.get("hostess_boundary", {}).get("status") == "future_lane_not_requested"
            and private_rehearsal_approval_request.get("hostess_boundary", {}).get("route_status") == "not_created"
            and private_rehearsal_approval_request.get("hostess_boundary", {}).get("device_action_authority") == "not_in_sidecar"
            and private_rehearsal_approval_request.get("requested_rehearsal", {}).get("commands_allowed") is False
            and private_rehearsal_approval_request.get("requested_rehearsal", {}).get("adb_allowed") is False
            and private_rehearsal_approval_request.get("requested_rehearsal", {}).get("public_fixture_contains_endpoint_values") is False
            and not any(
                private_rehearsal_approval_request.get("privacy_boundary", {}).get(key)
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
                "approval_owner": private_rehearsal_approval_request.get("authority", {}).get("approval_owner"),
                "handoff_acceptance_owner": private_rehearsal_approval_request.get("authority", {}).get("handoff_acceptance_owner"),
                "runtime_authority_owner": private_rehearsal_approval_request.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": private_rehearsal_approval_request.get("authority", {}).get("session_authority_owner"),
                "audit_owner": private_rehearsal_approval_request.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": private_rehearsal_approval_request.get("authority", {}).get("accepted_state_owner"),
                "hostess_status": private_rehearsal_approval_request.get("hostess_boundary", {}).get("status"),
                "hostess_route_status": private_rehearsal_approval_request.get("hostess_boundary", {}).get("route_status"),
                "hostess_device_action_authority": private_rehearsal_approval_request.get("hostess_boundary", {}).get("device_action_authority"),
                "commands_allowed": private_rehearsal_approval_request.get("requested_rehearsal", {}).get("commands_allowed"),
                "adb_allowed": private_rehearsal_approval_request.get("requested_rehearsal", {}).get("adb_allowed"),
                "public_fixture_contains_endpoint_values": private_rehearsal_approval_request.get("requested_rehearsal", {}).get("public_fixture_contains_endpoint_values"),
                "privacy_boundary": private_rehearsal_approval_request.get("privacy_boundary", {}),
            },
            {
                "approval_owner": "operator",
                "handoff_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_device_action_authority": "not_in_sidecar",
                "commands_allowed": False,
                "adb_allowed": False,
                "public_fixture_contains_endpoint_values": False,
                "privacy_flags_all_false": True,
            },
            "private rehearsal approval request preserves operator, Manifold, Hostess, and privacy boundaries",
        ),
        check(
            "manifold_route_blueprint.ready_for_design_review",
            manifold_route_blueprint.get("blueprint_status") == "ready_for_manifold_repo_design_review"
            and manifold_route_blueprint.get("summary", {}).get("fail_count") == 0
            and manifold_route_blueprint.get("blueprint_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_route_blueprint.get("blueprint_scope", {}).get("route_status") == "not_created"
            and manifold_route_blueprint.get("blueprint_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_route_blueprint.get("proposed_manifold_route", {}).get("route_creation_status") == "not_created"
            and manifold_route_blueprint.get("audit_contract", {}).get("audit_record_status") == "not_created"
            and manifold_route_blueprint.get("next_gate") == "manifold_repo_design_review_or_operator_decision",
            {
                "blueprint_status": manifold_route_blueprint.get("blueprint_status"),
                "fail_count": manifold_route_blueprint.get("summary", {}).get("fail_count"),
                "repo_touch_status": manifold_route_blueprint.get("blueprint_scope", {}).get("repo_touch_status"),
                "route_status": manifold_route_blueprint.get("blueprint_scope", {}).get("route_status"),
                "accepted_state_status": manifold_route_blueprint.get("blueprint_scope", {}).get("accepted_state_status"),
                "route_creation_status": manifold_route_blueprint.get("proposed_manifold_route", {}).get("route_creation_status"),
                "audit_record_status": manifold_route_blueprint.get("audit_contract", {}).get("audit_record_status"),
                "next_gate": manifold_route_blueprint.get("next_gate"),
            },
            {
                "blueprint_status": "ready_for_manifold_repo_design_review",
                "fail_count": 0,
                "repo_touch_status": "not_touched",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "route_creation_status": "not_created",
                "audit_record_status": "not_created",
                "next_gate": "manifold_repo_design_review_or_operator_decision",
            },
            "Manifold route blueprint is ready for design review without touching route, state, or audit records",
        ),
        check(
            "manifold_route_blueprint.preserves_manifold_hostess_boundaries",
            manifold_route_blueprint.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_route_blueprint.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_route_blueprint.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_route_blueprint.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_route_blueprint.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_route_blueprint.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_route_blueprint.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_route_blueprint.get("hostess_boundary", {}).get("status") == "future_lane_not_requested"
            and manifold_route_blueprint.get("hostess_boundary", {}).get("route_status") == "not_created"
            and manifold_route_blueprint.get("hostess_boundary", {}).get("device_action_authority") == "not_in_sidecar"
            and manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_endpoint_values") is False
            and manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_commands") is False
            and manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_adb") is False
            and manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_high_rate_payloads") is False
            and not any(
                manifold_route_blueprint.get("privacy_boundary", {}).get(key)
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
                "route_implementation_owner": manifold_route_blueprint.get("authority", {}).get("route_implementation_owner"),
                "request_acceptance_owner": manifold_route_blueprint.get("authority", {}).get("request_acceptance_owner"),
                "runtime_authority_owner": manifold_route_blueprint.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_route_blueprint.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_route_blueprint.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_route_blueprint.get("authority", {}).get("accepted_state_owner"),
                "rollback_owner": manifold_route_blueprint.get("authority", {}).get("rollback_owner"),
                "hostess_status": manifold_route_blueprint.get("hostess_boundary", {}).get("status"),
                "hostess_route_status": manifold_route_blueprint.get("hostess_boundary", {}).get("route_status"),
                "hostess_device_action_authority": manifold_route_blueprint.get("hostess_boundary", {}).get("device_action_authority"),
                "allows_endpoint_values": manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_endpoint_values"),
                "allows_commands": manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_commands"),
                "allows_adb": manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_adb"),
                "allows_high_rate_payloads": manifold_route_blueprint.get("proposed_manifold_route", {}).get("allows_high_rate_payloads"),
                "privacy_boundary": manifold_route_blueprint.get("privacy_boundary", {}),
            },
            {
                "route_implementation_owner": "rusty.manifold",
                "request_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "rollback_owner": "rusty.manifold",
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_device_action_authority": "not_in_sidecar",
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "privacy_flags_all_false": True,
            },
            "Manifold route blueprint keeps route/session/audit authority in Manifold and leaves Hostess as a future explicit lane",
        ),
        check(
            "manifold_route_design_review_request.ready_for_review",
            manifold_route_design_review_request.get("request_status") == "ready_for_manifold_route_design_review"
            and manifold_route_design_review_request.get("summary", {}).get("fail_count") == 0
            and manifold_route_design_review_request.get("request_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_route_design_review_request.get("request_scope", {}).get("route_status") == "not_created"
            and manifold_route_design_review_request.get("request_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_route_design_review_request.get("request_scope", {}).get("audit_record_status") == "not_created"
            and manifold_route_design_review_request.get("request_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_route_design_review_request.get("next_gate") == "manifold_repo_design_review_or_operator_decision",
            {
                "request_status": manifold_route_design_review_request.get("request_status"),
                "fail_count": manifold_route_design_review_request.get("summary", {}).get("fail_count"),
                "repo_touch_status": manifold_route_design_review_request.get("request_scope", {}).get("repo_touch_status"),
                "route_status": manifold_route_design_review_request.get("request_scope", {}).get("route_status"),
                "accepted_state_status": manifold_route_design_review_request.get("request_scope", {}).get("accepted_state_status"),
                "audit_record_status": manifold_route_design_review_request.get("request_scope", {}).get("audit_record_status"),
                "hostess_route_status": manifold_route_design_review_request.get("request_scope", {}).get("hostess_route_status"),
                "next_gate": manifold_route_design_review_request.get("next_gate"),
            },
            {
                "request_status": "ready_for_manifold_route_design_review",
                "fail_count": 0,
                "repo_touch_status": "not_touched",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "next_gate": "manifold_repo_design_review_or_operator_decision",
            },
            "Manifold route design review request is ready without touching Manifold, Hostess, routes, state, or audit records",
        ),
        check(
            "manifold_route_design_review_request.preserves_manifold_hostess_boundaries",
            manifold_route_design_review_request.get("authority", {}).get("design_review_owner") == "rusty.manifold"
            and manifold_route_design_review_request.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_route_design_review_request.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_route_design_review_request.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_route_design_review_request.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_route_design_review_request.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_route_design_review_request.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_route_design_review_request.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("status") == "future_lane_not_requested"
            and manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("route_status") == "not_created"
            and manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("device_action_authority") == "not_in_sidecar"
            and manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("requires_manifold_accepted_state") is True
            and manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("requires_explicit_operator_request") is True
            and all(
                item.get("owner") == "rusty.manifold" and item.get("status") == "not_created" and item.get("acceptance_required") is True
                for item in manifold_route_design_review_request.get("proposed_manifold_work_items", [])
            )
            and not any(
                manifold_route_design_review_request.get("privacy_boundary", {}).get(key)
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
                "design_review_owner": manifold_route_design_review_request.get("authority", {}).get("design_review_owner"),
                "route_implementation_owner": manifold_route_design_review_request.get("authority", {}).get("route_implementation_owner"),
                "request_acceptance_owner": manifold_route_design_review_request.get("authority", {}).get("request_acceptance_owner"),
                "runtime_authority_owner": manifold_route_design_review_request.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_route_design_review_request.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_route_design_review_request.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_route_design_review_request.get("authority", {}).get("accepted_state_owner"),
                "rollback_owner": manifold_route_design_review_request.get("authority", {}).get("rollback_owner"),
                "hostess_status": manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("status"),
                "hostess_route_status": manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("route_status"),
                "hostess_device_action_authority": manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("device_action_authority"),
                "requires_manifold_accepted_state": manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("requires_manifold_accepted_state"),
                "requires_explicit_operator_request": manifold_route_design_review_request.get("hostess_integration_preconditions", {}).get("requires_explicit_operator_request"),
                "work_item_owners": sorted({item.get("owner") for item in manifold_route_design_review_request.get("proposed_manifold_work_items", [])}),
                "work_item_statuses": sorted({item.get("status") for item in manifold_route_design_review_request.get("proposed_manifold_work_items", [])}),
                "privacy_boundary": manifold_route_design_review_request.get("privacy_boundary", {}),
            },
            {
                "design_review_owner": "rusty.manifold",
                "route_implementation_owner": "rusty.manifold",
                "request_acceptance_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "rollback_owner": "rusty.manifold",
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_device_action_authority": "not_in_sidecar",
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "work_items_manifold_owned_not_created": True,
                "privacy_flags_all_false": True,
            },
            "Manifold route design review request keeps design review and work items in Manifold and leaves Hostess gated",
        ),
        check(
            "manifold_route_design_response_expectation.ready_for_manifold_response",
            manifold_route_design_response_expectation.get("expectation_status") == "ready_for_manifold_owned_response"
            and manifold_route_design_response_expectation.get("summary", {}).get("fail_count") == 0
            and manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("response_status") == "not_created"
            and manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("decision_status") == "not_decided"
            and manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("route_status") == "not_created"
            and manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("audit_record_status") == "not_created"
            and manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_route_design_response_expectation.get("next_gate") == "manifold_owned_response_or_operator_decision",
            {
                "expectation_status": manifold_route_design_response_expectation.get("expectation_status"),
                "fail_count": manifold_route_design_response_expectation.get("summary", {}).get("fail_count"),
                "repo_touch_status": manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("repo_touch_status"),
                "response_status": manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("response_status"),
                "decision_status": manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("decision_status"),
                "route_status": manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("route_status"),
                "accepted_state_status": manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("accepted_state_status"),
                "audit_record_status": manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("audit_record_status"),
                "hostess_route_status": manifold_route_design_response_expectation.get("response_expectation_scope", {}).get("hostess_route_status"),
                "next_gate": manifold_route_design_response_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_manifold_owned_response",
                "fail_count": 0,
                "repo_touch_status": "not_touched",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "next_gate": "manifold_owned_response_or_operator_decision",
            },
            "Manifold route design response expectation is ready without creating a response, decision, route, accepted state, audit record, or Hostess route",
        ),
        check(
            "manifold_route_design_response_expectation.preserves_manifold_hostess_boundaries",
            manifold_route_design_response_expectation.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_route_design_response_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_route_design_response_expectation.get("expected_manifold_response", {}).get("response_status") == "not_created"
            and manifold_route_design_response_expectation.get("expected_manifold_response", {}).get("decision_status") == "not_decided"
            and set(manifold_route_design_response_expectation.get("expected_manifold_response", {}).get("allowed_decisions", []))
            == {"accepted_for_manifold_slice", "revision_requested", "rejected"}
            and manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("status") == "future_lane_not_requested"
            and manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("route_status") == "not_created"
            and manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("device_action_authority") == "not_in_sidecar"
            and manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("sidecar_direct_input_allowed") is False
            and manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("requires_manifold_accepted_state") is True
            and manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("requires_explicit_operator_request") is True
            and not any(
                manifold_route_design_response_expectation.get("privacy_boundary", {}).get(key)
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
                "response_owner": manifold_route_design_response_expectation.get("authority", {}).get("response_owner"),
                "decision_owner": manifold_route_design_response_expectation.get("authority", {}).get("decision_owner"),
                "route_implementation_owner": manifold_route_design_response_expectation.get("authority", {}).get("route_implementation_owner"),
                "request_acceptance_owner": manifold_route_design_response_expectation.get("authority", {}).get("request_acceptance_owner"),
                "runtime_authority_owner": manifold_route_design_response_expectation.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_route_design_response_expectation.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_route_design_response_expectation.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_route_design_response_expectation.get("authority", {}).get("accepted_state_owner"),
                "rollback_owner": manifold_route_design_response_expectation.get("authority", {}).get("rollback_owner"),
                "response_status": manifold_route_design_response_expectation.get("expected_manifold_response", {}).get("response_status"),
                "decision_status": manifold_route_design_response_expectation.get("expected_manifold_response", {}).get("decision_status"),
                "allowed_decisions": manifold_route_design_response_expectation.get("expected_manifold_response", {}).get("allowed_decisions", []),
                "hostess_status": manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("status"),
                "hostess_route_status": manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("route_status"),
                "hostess_device_action_authority": manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("device_action_authority"),
                "sidecar_direct_input_allowed": manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("sidecar_direct_input_allowed"),
                "requires_manifold_accepted_state": manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("requires_manifold_accepted_state"),
                "requires_explicit_operator_request": manifold_route_design_response_expectation.get("hostess_response_gate", {}).get("requires_explicit_operator_request"),
                "privacy_boundary": manifold_route_design_response_expectation.get("privacy_boundary", {}),
            },
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
                "response_status": "not_created",
                "decision_status": "not_decided",
                "allowed_decisions": ["accepted_for_manifold_slice", "revision_requested", "rejected"],
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold route design response expectation keeps response decisions in Manifold and Hostess behind accepted state or operator request",
        ),
        check(
            "manifold_response_implementation_preflight.ready_for_manifold_repo_slice_planning",
            manifold_response_implementation_preflight.get("preflight_status") == "ready_for_manifold_repo_slice_planning"
            and manifold_response_implementation_preflight.get("summary", {}).get("fail_count") == 0
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("branch_status") == "not_created"
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("response_status") == "not_created"
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("decision_status") == "not_decided"
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("route_status") == "not_created"
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("audit_record_status") == "not_created"
            and manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_response_implementation_preflight.get("next_gate") == "manifold_repo_response_slice_or_operator_decision",
            {
                "preflight_status": manifold_response_implementation_preflight.get("preflight_status"),
                "fail_count": manifold_response_implementation_preflight.get("summary", {}).get("fail_count"),
                "repo_touch_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("repo_touch_status"),
                "branch_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("branch_status"),
                "response_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("response_status"),
                "decision_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("decision_status"),
                "route_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("route_status"),
                "accepted_state_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("accepted_state_status"),
                "audit_record_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("audit_record_status"),
                "hostess_route_status": manifold_response_implementation_preflight.get("implementation_preflight_scope", {}).get("hostess_route_status"),
                "next_gate": manifold_response_implementation_preflight.get("next_gate"),
            },
            {
                "preflight_status": "ready_for_manifold_repo_slice_planning",
                "fail_count": 0,
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "next_gate": "manifold_repo_response_slice_or_operator_decision",
            },
            "Manifold response implementation preflight is ready without touching repos, creating branches, response, decision, route, accepted state, audit, or Hostess route",
        ),
        check(
            "manifold_response_implementation_preflight.preserves_manifold_hostess_boundaries",
            manifold_response_implementation_preflight.get("authority", {}).get("implementation_plan_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_response_implementation_preflight.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_response_implementation_preflight.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and all(
                artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"}
                and artifact.get("status") == "not_created_by_sidecar"
                for artifact in manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_manifold_owned_artifacts", [])
            )
            and manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_route_boundaries", {}).get("allows_endpoint_values") is False
            and manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_route_boundaries", {}).get("allows_commands") is False
            and manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_route_boundaries", {}).get("allows_adb") is False
            and manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_route_boundaries", {}).get("allows_sidecar_direct_hostess_input") is False
            and manifold_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("status") == "future_lane_not_requested"
            and manifold_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("route_status") == "not_created"
            and manifold_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("device_action_authority") == "not_in_sidecar"
            and manifold_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("sidecar_direct_input_allowed") is False
            and manifold_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("requires_manifold_accepted_state") is True
            and manifold_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("requires_explicit_operator_request") is True
            and not any(
                manifold_response_implementation_preflight.get("privacy_boundary", {}).get(key)
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
                "implementation_plan_owner": manifold_response_implementation_preflight.get("authority", {}).get("implementation_plan_owner"),
                "response_owner": manifold_response_implementation_preflight.get("authority", {}).get("response_owner"),
                "decision_owner": manifold_response_implementation_preflight.get("authority", {}).get("decision_owner"),
                "route_implementation_owner": manifold_response_implementation_preflight.get("authority", {}).get("route_implementation_owner"),
                "request_acceptance_owner": manifold_response_implementation_preflight.get("authority", {}).get("request_acceptance_owner"),
                "runtime_authority_owner": manifold_response_implementation_preflight.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_response_implementation_preflight.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_response_implementation_preflight.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_response_implementation_preflight.get("authority", {}).get("accepted_state_owner"),
                "rollback_owner": manifold_response_implementation_preflight.get("authority", {}).get("rollback_owner"),
                "artifact_owners": sorted({artifact.get("owner") for artifact in manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_manifold_owned_artifacts", [])}),
                "artifact_statuses": sorted({artifact.get("status") for artifact in manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_manifold_owned_artifacts", [])}),
                "route_boundaries": manifold_response_implementation_preflight.get("manifold_repo_slice_requirements", {}).get("required_route_boundaries", {}),
                "hostess_boundary_preflight": manifold_response_implementation_preflight.get("hostess_boundary_preflight", {}),
                "privacy_boundary": manifold_response_implementation_preflight.get("privacy_boundary", {}),
            },
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
                "artifacts_manifold_owned_not_created": True,
                "route_boundaries_reject_endpoint_command_adb_hostess_direct": True,
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold response implementation preflight keeps implementation artifacts in Manifold and Hostess deferred",
        ),
        check(
            "manifold_response_handoff_package.ready_for_manifold_repo_handoff",
            manifold_response_handoff_package.get("package_status") == "response_handoff_package_ready"
            and manifold_response_handoff_package.get("summary", {}).get("fail_count") == 0
            and manifold_response_handoff_package.get("package_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_response_handoff_package.get("package_scope", {}).get("branch_status") == "not_created"
            and manifold_response_handoff_package.get("package_scope", {}).get("implementation_status") == "not_created"
            and manifold_response_handoff_package.get("package_scope", {}).get("response_status") == "not_created"
            and manifold_response_handoff_package.get("package_scope", {}).get("decision_status") == "not_decided"
            and manifold_response_handoff_package.get("package_scope", {}).get("route_status") == "not_created"
            and manifold_response_handoff_package.get("package_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_response_handoff_package.get("package_scope", {}).get("audit_record_status") == "not_created"
            and manifold_response_handoff_package.get("package_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_response_handoff_package.get("handoff_manifest", {}).get("handoff_acceptance_status") == "not_accepted"
            and manifold_response_handoff_package.get("handoff_manifest", {}).get("downstream_implementation_status") == "not_created"
            and manifold_response_handoff_package.get("next_gate") == "manifold_repo_response_slice_or_operator_decision",
            {
                "package_status": manifold_response_handoff_package.get("package_status"),
                "fail_count": manifold_response_handoff_package.get("summary", {}).get("fail_count"),
                "repo_touch_status": manifold_response_handoff_package.get("package_scope", {}).get("repo_touch_status"),
                "branch_status": manifold_response_handoff_package.get("package_scope", {}).get("branch_status"),
                "implementation_status": manifold_response_handoff_package.get("package_scope", {}).get("implementation_status"),
                "response_status": manifold_response_handoff_package.get("package_scope", {}).get("response_status"),
                "decision_status": manifold_response_handoff_package.get("package_scope", {}).get("decision_status"),
                "route_status": manifold_response_handoff_package.get("package_scope", {}).get("route_status"),
                "accepted_state_status": manifold_response_handoff_package.get("package_scope", {}).get("accepted_state_status"),
                "audit_record_status": manifold_response_handoff_package.get("package_scope", {}).get("audit_record_status"),
                "hostess_route_status": manifold_response_handoff_package.get("package_scope", {}).get("hostess_route_status"),
                "handoff_acceptance_status": manifold_response_handoff_package.get("handoff_manifest", {}).get("handoff_acceptance_status"),
                "downstream_implementation_status": manifold_response_handoff_package.get("handoff_manifest", {}).get("downstream_implementation_status"),
                "next_gate": manifold_response_handoff_package.get("next_gate"),
            },
            {
                "package_status": "response_handoff_package_ready",
                "fail_count": 0,
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "implementation_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "handoff_acceptance_status": "not_accepted",
                "downstream_implementation_status": "not_created",
                "next_gate": "manifold_repo_response_slice_or_operator_decision",
            },
            "Manifold response handoff package is ready without touching repos, creating branches, response, decision, route, accepted state, audit, or Hostess route",
        ),
        check(
            "manifold_response_handoff_package.preserves_manifold_hostess_boundaries",
            manifold_response_handoff_package.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("implementation_plan_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_response_handoff_package.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_response_handoff_package.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and all(
                artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"}
                and artifact.get("status") == "not_created_by_sidecar"
                for artifact in manifold_response_handoff_package.get("handoff_manifest", {}).get("required_downstream_artifacts", [])
            )
            and manifold_response_handoff_package.get("handoff_manifest", {}).get("required_route_boundaries", {}).get("allows_endpoint_values") is False
            and manifold_response_handoff_package.get("handoff_manifest", {}).get("required_route_boundaries", {}).get("allows_commands") is False
            and manifold_response_handoff_package.get("handoff_manifest", {}).get("required_route_boundaries", {}).get("allows_adb") is False
            and manifold_response_handoff_package.get("handoff_manifest", {}).get("required_route_boundaries", {}).get("allows_sidecar_direct_hostess_input") is False
            and manifold_response_handoff_package.get("hostess_boundary_handoff", {}).get("status") == "future_lane_not_requested"
            and manifold_response_handoff_package.get("hostess_boundary_handoff", {}).get("route_status") == "not_created"
            and manifold_response_handoff_package.get("hostess_boundary_handoff", {}).get("device_action_authority") == "not_in_sidecar"
            and manifold_response_handoff_package.get("hostess_boundary_handoff", {}).get("sidecar_direct_input_allowed") is False
            and manifold_response_handoff_package.get("hostess_boundary_handoff", {}).get("requires_manifold_accepted_state") is True
            and manifold_response_handoff_package.get("hostess_boundary_handoff", {}).get("requires_explicit_operator_request") is True
            and not any(
                manifold_response_handoff_package.get("privacy_boundary", {}).get(key)
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
                "handoff_acceptance_owner": manifold_response_handoff_package.get("authority", {}).get("handoff_acceptance_owner"),
                "implementation_plan_owner": manifold_response_handoff_package.get("authority", {}).get("implementation_plan_owner"),
                "response_owner": manifold_response_handoff_package.get("authority", {}).get("response_owner"),
                "decision_owner": manifold_response_handoff_package.get("authority", {}).get("decision_owner"),
                "route_implementation_owner": manifold_response_handoff_package.get("authority", {}).get("route_implementation_owner"),
                "request_acceptance_owner": manifold_response_handoff_package.get("authority", {}).get("request_acceptance_owner"),
                "runtime_authority_owner": manifold_response_handoff_package.get("authority", {}).get("runtime_authority_owner"),
                "session_authority_owner": manifold_response_handoff_package.get("authority", {}).get("session_authority_owner"),
                "audit_owner": manifold_response_handoff_package.get("authority", {}).get("audit_owner"),
                "accepted_state_owner": manifold_response_handoff_package.get("authority", {}).get("accepted_state_owner"),
                "rollback_owner": manifold_response_handoff_package.get("authority", {}).get("rollback_owner"),
                "artifact_owners": sorted({artifact.get("owner") for artifact in manifold_response_handoff_package.get("handoff_manifest", {}).get("required_downstream_artifacts", [])}),
                "artifact_statuses": sorted({artifact.get("status") for artifact in manifold_response_handoff_package.get("handoff_manifest", {}).get("required_downstream_artifacts", [])}),
                "route_boundaries": manifold_response_handoff_package.get("handoff_manifest", {}).get("required_route_boundaries", {}),
                "hostess_boundary_handoff": manifold_response_handoff_package.get("hostess_boundary_handoff", {}),
                "privacy_boundary": manifold_response_handoff_package.get("privacy_boundary", {}),
            },
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
                "artifacts_manifold_owned_not_created": True,
                "route_boundaries_reject_endpoint_command_adb_hostess_direct": True,
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold response handoff package keeps response slice work in Manifold and Hostess deferred as a boundary descriptor",
        ),
        check(
            "hostess_boundary_descriptor_expectation.ready_without_route_or_state",
            hostess_boundary_descriptor_expectation.get("expectation_status") == "ready_for_future_hostess_boundary_descriptor"
            and hostess_boundary_descriptor_expectation.get("summary", {}).get("fail_count") == 0
            and hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("manifold_repo_touch_status") == "not_touched"
            and hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("hostess_repo_touch_status") == "not_touched"
            and hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("hostess_route_status") == "not_created"
            and hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("manifold_accepted_state_status") == "not_created"
            and hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("operator_request_status") == "not_recorded"
            and hostess_boundary_descriptor_expectation.get("manifold_acceptance_gate", {}).get("handoff_acceptance_status") == "not_accepted"
            and hostess_boundary_descriptor_expectation.get("manifold_acceptance_gate", {}).get("hostess_enablement_status") == "not_enabled"
            and hostess_boundary_descriptor_expectation.get("manifold_acceptance_gate", {}).get("gate_result") == "hostess_boundary_descriptor_not_ready_for_route_creation"
            and hostess_boundary_descriptor_expectation.get("next_gate") == "manifold_response_slice_or_operator_decision",
            {
                "expectation_status": hostess_boundary_descriptor_expectation.get("expectation_status"),
                "fail_count": hostess_boundary_descriptor_expectation.get("summary", {}).get("fail_count"),
                "manifold_repo_touch_status": hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("manifold_repo_touch_status"),
                "hostess_repo_touch_status": hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("hostess_repo_touch_status"),
                "hostess_route_status": hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("hostess_route_status"),
                "manifold_accepted_state_status": hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("manifold_accepted_state_status"),
                "operator_request_status": hostess_boundary_descriptor_expectation.get("expectation_scope", {}).get("operator_request_status"),
                "handoff_acceptance_status": hostess_boundary_descriptor_expectation.get("manifold_acceptance_gate", {}).get("handoff_acceptance_status"),
                "hostess_enablement_status": hostess_boundary_descriptor_expectation.get("manifold_acceptance_gate", {}).get("hostess_enablement_status"),
                "gate_result": hostess_boundary_descriptor_expectation.get("manifold_acceptance_gate", {}).get("gate_result"),
                "next_gate": hostess_boundary_descriptor_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_future_hostess_boundary_descriptor",
                "fail_count": 0,
                "manifold_repo_touch_status": "not_touched",
                "hostess_repo_touch_status": "not_touched",
                "hostess_route_status": "not_created",
                "manifold_accepted_state_status": "not_created",
                "operator_request_status": "not_recorded",
                "handoff_acceptance_status": "not_accepted",
                "hostess_enablement_status": "not_enabled",
                "gate_result": "hostess_boundary_descriptor_not_ready_for_route_creation",
                "next_gate": "manifold_response_slice_or_operator_decision",
            },
            "Hostess boundary descriptor expectation is ready as planning evidence while routes, accepted state, operator request, and enablement remain absent",
        ),
        check(
            "hostess_boundary_descriptor_expectation.preserves_manifold_hostess_split",
            hostess_boundary_descriptor_expectation.get("authority", {}).get("boundary_descriptor_owner") == "rusty.manifold"
            and hostess_boundary_descriptor_expectation.get("authority", {}).get("source_of_truth_owner") == "rusty.manifold"
            and hostess_boundary_descriptor_expectation.get("authority", {}).get("response_decision_owner") == "rusty.manifold"
            and hostess_boundary_descriptor_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and hostess_boundary_descriptor_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and hostess_boundary_descriptor_expectation.get("authority", {}).get("future_hostess_route_owner") == "rusty.hostess"
            and hostess_boundary_descriptor_expectation.get("authority", {}).get("future_hostess_route_enablement_owner") == "rusty.manifold"
            and hostess_boundary_descriptor_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}).get("sidecar_direct_input_allowed") is False
            and hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}).get("requires_manifold_accepted_state") is True
            and hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}).get("requires_explicit_operator_request") is True
            and hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}).get("allows_endpoint_values") is False
            and hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}).get("allows_commands") is False
            and hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}).get("allows_adb") is False
            and hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}).get("safe_to_create_hostess_route") is False
            and not any(
                hostess_boundary_descriptor_expectation.get("privacy_boundary", {}).get(key)
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
                "boundary_descriptor_owner": hostess_boundary_descriptor_expectation.get("authority", {}).get("boundary_descriptor_owner"),
                "source_of_truth_owner": hostess_boundary_descriptor_expectation.get("authority", {}).get("source_of_truth_owner"),
                "response_decision_owner": hostess_boundary_descriptor_expectation.get("authority", {}).get("response_decision_owner"),
                "accepted_state_owner": hostess_boundary_descriptor_expectation.get("authority", {}).get("accepted_state_owner"),
                "audit_owner": hostess_boundary_descriptor_expectation.get("authority", {}).get("audit_owner"),
                "future_hostess_route_owner": hostess_boundary_descriptor_expectation.get("authority", {}).get("future_hostess_route_owner"),
                "future_hostess_route_enablement_owner": hostess_boundary_descriptor_expectation.get("authority", {}).get("future_hostess_route_enablement_owner"),
                "hostess_device_action_authority": hostess_boundary_descriptor_expectation.get("authority", {}).get("hostess_device_action_authority"),
                "expected_hostess_boundary_descriptor": hostess_boundary_descriptor_expectation.get("expected_hostess_boundary_descriptor", {}),
                "privacy_boundary": hostess_boundary_descriptor_expectation.get("privacy_boundary", {}),
            },
            {
                "boundary_descriptor_owner": "rusty.manifold",
                "source_of_truth_owner": "rusty.manifold",
                "response_decision_owner": "rusty.manifold",
                "accepted_state_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "future_hostess_route_owner": "rusty.hostess",
                "future_hostess_route_enablement_owner": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "safe_to_create_hostess_route": False,
                "privacy_flags_all_false": True,
            },
            "Hostess boundary descriptor expectation keeps Manifold as source of truth and Hostess gated away from sidecar-direct device actions",
        ),
        check(
            "private_rehearsal_evidence_expectation.ready_for_operator_gated_private_plan",
            private_rehearsal_evidence_expectation.get("expectation_status") == "ready_for_operator_approved_private_evidence_plan"
            and private_rehearsal_evidence_expectation.get("summary", {}).get("fail_count") == 0
            and private_rehearsal_evidence_expectation.get("source_private_rehearsal_approval_request", {}).get("request_status") == "operator_approval_required"
            and private_rehearsal_evidence_expectation.get("source_hostess_boundary_descriptor_expectation", {}).get("expectation_status") == "ready_for_future_hostess_boundary_descriptor"
            and private_rehearsal_evidence_expectation.get("evidence_scope", {}).get("operator_approval_status") == "not_recorded"
            and private_rehearsal_evidence_expectation.get("evidence_scope", {}).get("rehearsal_route_status") == "not_started"
            and private_rehearsal_evidence_expectation.get("evidence_scope", {}).get("private_evidence_status") == "not_collected"
            and private_rehearsal_evidence_expectation.get("evidence_scope", {}).get("public_derivative_status") == "not_created"
            and private_rehearsal_evidence_expectation.get("evidence_scope", {}).get("manifold_intake_status") == "not_submitted"
            and private_rehearsal_evidence_expectation.get("evidence_scope", {}).get("hostess_route_status") == "not_created"
            and private_rehearsal_evidence_expectation.get("next_gate") == "operator_decision_or_manifold_response_slice",
            {
                "expectation_status": private_rehearsal_evidence_expectation.get("expectation_status"),
                "fail_count": private_rehearsal_evidence_expectation.get("summary", {}).get("fail_count"),
                "source_approval_status": private_rehearsal_evidence_expectation.get("source_private_rehearsal_approval_request", {}).get("request_status"),
                "source_hostess_status": private_rehearsal_evidence_expectation.get("source_hostess_boundary_descriptor_expectation", {}).get("expectation_status"),
                "evidence_scope": private_rehearsal_evidence_expectation.get("evidence_scope", {}),
                "next_gate": private_rehearsal_evidence_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_operator_approved_private_evidence_plan",
                "fail_count": 0,
                "source_approval_status": "operator_approval_required",
                "source_hostess_status": "ready_for_future_hostess_boundary_descriptor",
                "operator_approval_status": "not_recorded",
                "rehearsal_route_status": "not_started",
                "private_evidence_status": "not_collected",
                "public_derivative_status": "not_created",
                "manifold_intake_status": "not_submitted",
                "hostess_route_status": "not_created",
                "next_gate": "operator_decision_or_manifold_response_slice",
            },
            "private rehearsal evidence expectation prepares a future private run without approving, collecting, submitting, or creating routes",
        ),
        check(
            "private_rehearsal_evidence_expectation.preserves_sanitized_manifold_hostess_boundary",
            private_rehearsal_evidence_expectation.get("authority", {}).get("approval_owner") == "operator"
            and private_rehearsal_evidence_expectation.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and private_rehearsal_evidence_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and private_rehearsal_evidence_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and private_rehearsal_evidence_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and private_rehearsal_evidence_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and private_rehearsal_evidence_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and private_rehearsal_evidence_expectation.get("private_evidence_requirements", {}).get("public_fixture_may_include_private_values") is False
            and private_rehearsal_evidence_expectation.get("private_evidence_requirements", {}).get("route_start_allowed_by_this_fixture") is False
            and private_rehearsal_evidence_expectation.get("private_evidence_requirements", {}).get("allowed_message_class") == "status_only"
            and private_rehearsal_evidence_expectation.get("public_derivative_requirements", {}).get("contains_private_values") is False
            and private_rehearsal_evidence_expectation.get("public_derivative_requirements", {}).get("public_fixture_policy") == "synthetic_descriptor_only"
            and {
                "endpoint_values_removed",
                "pairing_material_removed",
                "commands_absent",
                "adb_absent",
                "raw_logs_not_copied",
                "visual_captures_not_copied",
                "private_device_ids_removed",
            }
            <= set(private_rehearsal_evidence_expectation.get("public_derivative_requirements", {}).get("required_redaction_results", []))
            and private_rehearsal_evidence_expectation.get("manifold_handoff_expectation", {}).get("submission_status") == "not_submitted"
            and private_rehearsal_evidence_expectation.get("manifold_handoff_expectation", {}).get("acceptance_owner") == "rusty.manifold"
            and private_rehearsal_evidence_expectation.get("hostess_escalation_boundary", {}).get("status") == "future_lane_not_requested"
            and private_rehearsal_evidence_expectation.get("hostess_escalation_boundary", {}).get("device_action_authority") == "not_in_sidecar"
            and private_rehearsal_evidence_expectation.get("hostess_escalation_boundary", {}).get("sidecar_direct_input_allowed") is False
            and private_rehearsal_evidence_expectation.get("hostess_escalation_boundary", {}).get("requires_manifold_accepted_state") is True
            and private_rehearsal_evidence_expectation.get("hostess_escalation_boundary", {}).get("requires_explicit_operator_request") is True
            and not any(
                private_rehearsal_evidence_expectation.get("privacy_boundary", {}).get(key)
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
                "authority": private_rehearsal_evidence_expectation.get("authority", {}),
                "private_evidence_requirements": private_rehearsal_evidence_expectation.get("private_evidence_requirements", {}),
                "public_derivative_requirements": private_rehearsal_evidence_expectation.get("public_derivative_requirements", {}),
                "manifold_handoff_expectation": private_rehearsal_evidence_expectation.get("manifold_handoff_expectation", {}),
                "hostess_escalation_boundary": private_rehearsal_evidence_expectation.get("hostess_escalation_boundary", {}),
                "privacy_boundary": private_rehearsal_evidence_expectation.get("privacy_boundary", {}),
            },
            {
                "approval_owner": "operator",
                "manifold_authority": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "public_fixture_may_include_private_values": False,
                "route_start_allowed_by_this_fixture": False,
                "allowed_message_class": "status_only",
                "contains_private_values": False,
                "public_fixture_policy": "synthetic_descriptor_only",
                "redaction_results_present": True,
                "submission_status": "not_submitted",
                "hostess_requires_manifold_state_and_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "private rehearsal evidence expectation preserves redaction, Manifold intake authority, and the future Hostess operator-recovery boundary",
        ),
        check(
            "private_rehearsal_public_derivative_expectation.ready_for_sanitized_contract",
            private_rehearsal_public_derivative_expectation.get("expectation_status") == "ready_for_sanitized_public_derivative_contract"
            and private_rehearsal_public_derivative_expectation.get("summary", {}).get("fail_count") == 0
            and private_rehearsal_public_derivative_expectation.get("source_private_rehearsal_evidence_expectation", {}).get("expectation_status") == "ready_for_operator_approved_private_evidence_plan"
            and private_rehearsal_public_derivative_expectation.get("derivative_scope", {}).get("operator_approval_status") == "not_recorded"
            and private_rehearsal_public_derivative_expectation.get("derivative_scope", {}).get("private_evidence_status") == "not_collected"
            and private_rehearsal_public_derivative_expectation.get("derivative_scope", {}).get("public_derivative_status") == "not_created"
            and private_rehearsal_public_derivative_expectation.get("derivative_scope", {}).get("derivative_schema_status") == "not_created"
            and private_rehearsal_public_derivative_expectation.get("derivative_scope", {}).get("manifold_intake_status") == "not_submitted"
            and private_rehearsal_public_derivative_expectation.get("derivative_scope", {}).get("hostess_route_status") == "not_created"
            and private_rehearsal_public_derivative_expectation.get("next_gate") == "operator_decision_or_manifold_public_derivative_schema_slice",
            {
                "expectation_status": private_rehearsal_public_derivative_expectation.get("expectation_status"),
                "fail_count": private_rehearsal_public_derivative_expectation.get("summary", {}).get("fail_count"),
                "source_status": private_rehearsal_public_derivative_expectation.get("source_private_rehearsal_evidence_expectation", {}).get("expectation_status"),
                "derivative_scope": private_rehearsal_public_derivative_expectation.get("derivative_scope", {}),
                "next_gate": private_rehearsal_public_derivative_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_sanitized_public_derivative_contract",
                "fail_count": 0,
                "source_status": "ready_for_operator_approved_private_evidence_plan",
                "operator_approval_status": "not_recorded",
                "private_evidence_status": "not_collected",
                "public_derivative_status": "not_created",
                "derivative_schema_status": "not_created",
                "manifold_intake_status": "not_submitted",
                "hostess_route_status": "not_created",
                "next_gate": "operator_decision_or_manifold_public_derivative_schema_slice",
            },
            "private rehearsal public derivative expectation prepares the sanitized contract without creating derivative evidence or Manifold intake",
        ),
        check(
            "private_rehearsal_public_derivative_expectation.preserves_sanitized_authority_boundary",
            private_rehearsal_public_derivative_expectation.get("authority", {}).get("redaction_review_owner") == "operator"
            and private_rehearsal_public_derivative_expectation.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and private_rehearsal_public_derivative_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and private_rehearsal_public_derivative_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and private_rehearsal_public_derivative_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and private_rehearsal_public_derivative_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and private_rehearsal_public_derivative_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}).get("contains_private_values") is False
            and private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}).get("input_policy") == "sanitized_summary_only"
            and private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}).get("allowed_message_class") == "status_only"
            and private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}).get("public_fixture_policy") == "synthetic_descriptor_only"
            and private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}).get("rejects_direct_hostess_input") is True
            and private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}).get("rejects_manifold_accepted_state") is True
            and {
                "endpoint_values_removed",
                "pairing_material_removed",
                "commands_absent",
                "adb_absent",
                "raw_logs_not_copied",
                "visual_captures_not_copied",
                "private_device_ids_removed",
            }
            <= set(private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}).get("required_redaction_results", []))
            and private_rehearsal_public_derivative_expectation.get("manifold_handoff_gate", {}).get("submission_status") == "not_submitted"
            and private_rehearsal_public_derivative_expectation.get("manifold_handoff_gate", {}).get("acceptance_owner") == "rusty.manifold"
            and private_rehearsal_public_derivative_expectation.get("hostess_escalation_boundary", {}).get("status") == "future_lane_not_requested"
            and private_rehearsal_public_derivative_expectation.get("hostess_escalation_boundary", {}).get("device_action_authority") == "not_in_sidecar"
            and private_rehearsal_public_derivative_expectation.get("hostess_escalation_boundary", {}).get("sidecar_direct_input_allowed") is False
            and not any(
                private_rehearsal_public_derivative_expectation.get("privacy_boundary", {}).get(key)
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
                "authority": private_rehearsal_public_derivative_expectation.get("authority", {}),
                "expected_public_derivative": private_rehearsal_public_derivative_expectation.get("expected_public_derivative", {}),
                "manifold_handoff_gate": private_rehearsal_public_derivative_expectation.get("manifold_handoff_gate", {}),
                "hostess_escalation_boundary": private_rehearsal_public_derivative_expectation.get("hostess_escalation_boundary", {}),
                "privacy_boundary": private_rehearsal_public_derivative_expectation.get("privacy_boundary", {}),
            },
            {
                "redaction_review_owner": "operator",
                "manifold_authority": "rusty.manifold",
                "hostess_device_action_authority": "not_in_sidecar",
                "contains_private_values": False,
                "input_policy": "sanitized_summary_only",
                "allowed_message_class": "status_only",
                "public_fixture_policy": "synthetic_descriptor_only",
                "rejects_direct_hostess_input": True,
                "rejects_manifold_accepted_state": True,
                "redaction_results_present": True,
                "submission_status": "not_submitted",
                "privacy_flags_all_false": True,
            },
            "private rehearsal public derivative expectation preserves redaction, Manifold authority, and Hostess deferral",
        ),
        check(
            "manifold_public_derivative_schema_request.ready_for_manifold_review",
            manifold_public_derivative_schema_request.get("request_status") == "ready_for_manifold_public_derivative_schema_review"
            and manifold_public_derivative_schema_request.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_request.get("source_public_derivative_expectation", {}).get("expectation_status") == "ready_for_sanitized_public_derivative_contract"
            and manifold_public_derivative_schema_request.get("request_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_public_derivative_schema_request.get("request_scope", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_request.get("request_scope", {}).get("route_handler_status") == "not_created"
            and manifold_public_derivative_schema_request.get("request_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_public_derivative_schema_request.get("request_scope", {}).get("audit_record_status") == "not_created"
            and manifold_public_derivative_schema_request.get("request_scope", {}).get("public_derivative_status") == "not_created"
            and manifold_public_derivative_schema_request.get("next_gate") == "manifold_repo_public_derivative_schema_review_or_operator_decision",
            {
                "request_status": manifold_public_derivative_schema_request.get("request_status"),
                "fail_count": manifold_public_derivative_schema_request.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_request.get("source_public_derivative_expectation", {}).get("expectation_status"),
                "request_scope": manifold_public_derivative_schema_request.get("request_scope", {}),
                "next_gate": manifold_public_derivative_schema_request.get("next_gate"),
            },
            {
                "request_status": "ready_for_manifold_public_derivative_schema_review",
                "fail_count": 0,
                "source_status": "ready_for_sanitized_public_derivative_contract",
                "repo_touch_status": "not_touched",
                "schema_status": "not_created",
                "route_handler_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "public_derivative_status": "not_created",
                "next_gate": "manifold_repo_public_derivative_schema_review_or_operator_decision",
            },
            "Manifold public derivative schema request is a sidecar proposal only and does not create a Manifold repo slice",
        ),
        check(
            "manifold_public_derivative_schema_request.preserves_manifold_and_hostess_authority",
            manifold_public_derivative_schema_request.get("authority", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("authority", {}).get("route_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("authority", {}).get("review_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_request.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("authority", {}).get("redaction_review_owner") == "operator"
            and manifold_public_derivative_schema_request.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}).get("input_policy") == "sanitized_summary_only"
            and manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}).get("allowed_message_class") == "status_only"
            and manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}).get("contains_private_values") is False
            and manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}).get("creates_accepted_state") is False
            and manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}).get("creates_hostess_input") is False
            and manifold_public_derivative_schema_request.get("proposed_manifold_route", {}).get("route_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("proposed_manifold_route", {}).get("route_status") == "not_created"
            and manifold_public_derivative_schema_request.get("manifold_review_gate", {}).get("review_status") == "not_submitted"
            and manifold_public_derivative_schema_request.get("manifold_review_gate", {}).get("acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_request.get("hostess_escalation_boundary", {}).get("status") == "future_lane_not_requested"
            and manifold_public_derivative_schema_request.get("hostess_escalation_boundary", {}).get("sidecar_direct_input_allowed") is False
            and manifold_public_derivative_schema_request.get("hostess_escalation_boundary", {}).get("requires_manifold_accepted_state") is True
            and not any(
                manifold_public_derivative_schema_request.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_request.get("authority", {}),
                "proposed_manifold_schema": manifold_public_derivative_schema_request.get("proposed_manifold_schema", {}),
                "proposed_manifold_route": manifold_public_derivative_schema_request.get("proposed_manifold_route", {}),
                "manifold_review_gate": manifold_public_derivative_schema_request.get("manifold_review_gate", {}),
                "hostess_escalation_boundary": manifold_public_derivative_schema_request.get("hostess_escalation_boundary", {}),
                "privacy_boundary": manifold_public_derivative_schema_request.get("privacy_boundary", {}),
            },
            {
                "schema_owner": "rusty.manifold",
                "route_owner": "rusty.manifold",
                "review_owner": "rusty.manifold",
                "manifold_authority": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "redaction_review_owner": "operator",
                "hostess_device_action_authority": "not_in_sidecar",
                "schema_status": "not_created",
                "route_status": "not_created",
                "input_policy": "sanitized_summary_only",
                "allowed_message_class": "status_only",
                "contains_private_values": False,
                "creates_accepted_state": False,
                "creates_hostess_input": False,
                "review_status": "not_submitted",
                "hostess_status": "future_lane_not_requested",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema request prepares future Manifold review while keeping Hostess behind accepted state or operator request",
        ),
        check(
            "manifold_public_derivative_schema_response_expectation.ready_for_manifold_response",
            manifold_public_derivative_schema_response_expectation.get("expectation_status") == "ready_for_manifold_public_derivative_schema_response"
            and manifold_public_derivative_schema_response_expectation.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_response_expectation.get("source_manifold_public_derivative_schema_request", {}).get("request_status") == "ready_for_manifold_public_derivative_schema_review"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("branch_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("response_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("decision_status") == "not_decided"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("route_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("audit_record_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("public_derivative_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("next_gate") == "manifold_public_derivative_schema_response_or_operator_decision",
            {
                "expectation_status": manifold_public_derivative_schema_response_expectation.get("expectation_status"),
                "fail_count": manifold_public_derivative_schema_response_expectation.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_response_expectation.get("source_manifold_public_derivative_schema_request", {}).get("request_status"),
                "response_expectation_scope": manifold_public_derivative_schema_response_expectation.get("response_expectation_scope", {}),
                "next_gate": manifold_public_derivative_schema_response_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_manifold_public_derivative_schema_response",
                "fail_count": 0,
                "source_status": "ready_for_manifold_public_derivative_schema_review",
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "schema_status": "not_created",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "public_derivative_status": "not_created",
                "hostess_route_status": "not_created",
                "next_gate": "manifold_public_derivative_schema_response_or_operator_decision",
            },
            "Manifold public derivative schema response expectation defines response semantics without creating Manifold or Hostess artifacts",
        ),
        check(
            "manifold_public_derivative_schema_response_expectation.preserves_manifold_and_hostess_authority",
            manifold_public_derivative_schema_response_expectation.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("redaction_review_owner") == "operator"
            and manifold_public_derivative_schema_response_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and manifold_public_derivative_schema_response_expectation.get("expected_manifold_response", {}).get("response_status") == "not_created"
            and manifold_public_derivative_schema_response_expectation.get("expected_manifold_response", {}).get("decision_status") == "not_decided"
            and manifold_public_derivative_schema_response_expectation.get("expected_manifold_response", {}).get("allowed_response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_response_expectation.get("expected_manifold_response", {}).get("accepted_state_policy") == "manifold_owned_monotonic_revision"
            and manifold_public_derivative_schema_response_expectation.get("expected_manifold_response", {}).get("public_derivative_policy") == "response_does_not_create_derivative_artifact"
            and manifold_public_derivative_schema_response_expectation.get("expected_manifold_response", {}).get("hostess_input_policy") == "response_does_not_create_hostess_input"
            and manifold_public_derivative_schema_response_expectation.get("hostess_response_gate", {}).get("status") == "future_lane_not_requested"
            and manifold_public_derivative_schema_response_expectation.get("hostess_response_gate", {}).get("sidecar_direct_input_allowed") is False
            and manifold_public_derivative_schema_response_expectation.get("hostess_response_gate", {}).get("requires_manifold_accepted_state") is True
            and not any(
                manifold_public_derivative_schema_response_expectation.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_response_expectation.get("authority", {}),
                "expected_manifold_response": manifold_public_derivative_schema_response_expectation.get("expected_manifold_response", {}),
                "hostess_response_gate": manifold_public_derivative_schema_response_expectation.get("hostess_response_gate", {}),
                "privacy_boundary": manifold_public_derivative_schema_response_expectation.get("privacy_boundary", {}),
            },
            {
                "response_owner": "rusty.manifold",
                "decision_owner": "rusty.manifold",
                "schema_owner": "rusty.manifold",
                "route_implementation_owner": "rusty.manifold",
                "runtime_authority_owner": "rusty.manifold",
                "session_authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "redaction_review_owner": "operator",
                "hostess_device_action_authority": "not_in_sidecar",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "allowed_response_owner": "rusty.manifold",
                "accepted_state_policy": "manifold_owned_monotonic_revision",
                "public_derivative_policy": "response_does_not_create_derivative_artifact",
                "hostess_input_policy": "response_does_not_create_hostess_input",
                "hostess_status": "future_lane_not_requested",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema response expectation preserves Manifold response authority and Hostess deferral",
        ),
        check(
            "manifold_public_derivative_schema_implementation_preflight.ready_for_manifold_slice_planning",
            manifold_public_derivative_schema_implementation_preflight.get("preflight_status") == "ready_for_manifold_public_derivative_schema_slice_planning"
            and manifold_public_derivative_schema_implementation_preflight.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_implementation_preflight.get("source_manifold_public_derivative_schema_response_expectation", {}).get("expectation_status") == "ready_for_manifold_public_derivative_schema_response"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("branch_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("response_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("decision_status") == "not_decided"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("route_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("audit_record_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("validation_report_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("public_derivative_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_public_derivative_schema_implementation_preflight.get("next_gate") == "manifold_public_derivative_schema_handoff_or_operator_decision",
            {
                "preflight_status": manifold_public_derivative_schema_implementation_preflight.get("preflight_status"),
                "fail_count": manifold_public_derivative_schema_implementation_preflight.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_implementation_preflight.get("source_manifold_public_derivative_schema_response_expectation", {}).get("expectation_status"),
                "implementation_preflight_scope": manifold_public_derivative_schema_implementation_preflight.get("implementation_preflight_scope", {}),
                "next_gate": manifold_public_derivative_schema_implementation_preflight.get("next_gate"),
            },
            {
                "preflight_status": "ready_for_manifold_public_derivative_schema_slice_planning",
                "fail_count": 0,
                "source_status": "ready_for_manifold_public_derivative_schema_response",
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "schema_status": "not_created",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "validation_report_status": "not_created",
                "public_derivative_status": "not_created",
                "hostess_route_status": "not_created",
                "next_gate": "manifold_public_derivative_schema_handoff_or_operator_decision",
            },
            "Manifold public derivative schema implementation preflight is ready for a future Manifold-owned slice without touching repo or Hostess state",
        ),
        check(
            "manifold_public_derivative_schema_implementation_preflight.preserves_manifold_and_hostess_authority",
            manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("implementation_plan_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("redaction_review_owner") == "operator"
            and manifold_public_derivative_schema_implementation_preflight.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_preflight_requirements.get("implementation_status") == "not_created_by_sidecar"
            and public_derivative_preflight_artifacts
            and all(artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"} for artifact in public_derivative_preflight_artifacts)
            and all(artifact.get("status") == "not_created_by_sidecar" for artifact in public_derivative_preflight_artifacts)
            and public_derivative_preflight_route_boundaries.get("input_payload_class") == "low_rate_advisory_status"
            and public_derivative_preflight_route_boundaries.get("accepts_sanitized_summary_only") is True
            and public_derivative_preflight_route_boundaries.get("requires_operator_approval") is True
            and public_derivative_preflight_route_boundaries.get("requires_redaction_review") is True
            and public_derivative_preflight_route_boundaries.get("allows_endpoint_values") is False
            and public_derivative_preflight_route_boundaries.get("allows_commands") is False
            and public_derivative_preflight_route_boundaries.get("allows_adb") is False
            and public_derivative_preflight_route_boundaries.get("allows_high_rate_payloads") is False
            and public_derivative_preflight_route_boundaries.get("allows_sidecar_direct_hostess_input") is False
            and manifold_public_derivative_schema_implementation_preflight.get("hostess_boundary_preflight", {}).get("status") == "future_lane_not_requested"
            and manifold_public_derivative_schema_implementation_preflight.get("hostess_boundary_preflight", {}).get("sidecar_direct_input_allowed") is False
            and manifold_public_derivative_schema_implementation_preflight.get("hostess_boundary_preflight", {}).get("requires_manifold_accepted_state") is True
            and not any(
                manifold_public_derivative_schema_implementation_preflight.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_implementation_preflight.get("authority", {}),
                "manifold_repo_slice_requirements": public_derivative_preflight_requirements,
                "hostess_boundary_preflight": manifold_public_derivative_schema_implementation_preflight.get("hostess_boundary_preflight", {}),
                "privacy_boundary": manifold_public_derivative_schema_implementation_preflight.get("privacy_boundary", {}),
            },
            {
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
                "implementation_status": "not_created_by_sidecar",
                "artifact_status": "not_created_by_sidecar",
                "input_payload_class": "low_rate_advisory_status",
                "accepts_sanitized_summary_only": True,
                "requires_operator_approval": True,
                "requires_redaction_review": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "allows_sidecar_direct_hostess_input": False,
                "hostess_status": "future_lane_not_requested",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema implementation preflight preserves Manifold implementation authority and Hostess deferral",
        ),
        check(
            "manifold_public_derivative_schema_handoff_package.ready_for_manifold_handoff",
            manifold_public_derivative_schema_handoff_package.get("package_status") == "public_derivative_schema_handoff_package_ready"
            and manifold_public_derivative_schema_handoff_package.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_handoff_package.get("source_manifold_public_derivative_schema_implementation_preflight", {}).get("preflight_status") == "ready_for_manifold_public_derivative_schema_slice_planning"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("branch_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("implementation_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("response_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("decision_status") == "not_decided"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("route_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("audit_record_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("validation_report_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("public_derivative_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("package_scope", {}).get("hostess_route_status") == "not_created"
            and public_derivative_handoff_manifest.get("handoff_acceptance_status") == "not_accepted"
            and public_derivative_handoff_manifest.get("downstream_implementation_status") == "not_created"
            and public_derivative_handoff_manifest.get("downstream_schema_status") == "not_created"
            and public_derivative_handoff_manifest.get("downstream_route_status") == "not_created"
            and public_derivative_handoff_manifest.get("downstream_validation_report_status") == "not_created"
            and public_derivative_handoff_manifest.get("downstream_hostess_boundary_status") == "not_created"
            and manifold_public_derivative_schema_handoff_package.get("next_gate") == "manifold_repo_public_derivative_schema_slice_or_operator_decision",
            {
                "package_status": manifold_public_derivative_schema_handoff_package.get("package_status"),
                "fail_count": manifold_public_derivative_schema_handoff_package.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_handoff_package.get("source_manifold_public_derivative_schema_implementation_preflight", {}).get("preflight_status"),
                "package_scope": manifold_public_derivative_schema_handoff_package.get("package_scope", {}),
                "handoff_manifest": public_derivative_handoff_manifest,
                "next_gate": manifold_public_derivative_schema_handoff_package.get("next_gate"),
            },
            {
                "package_status": "public_derivative_schema_handoff_package_ready",
                "fail_count": 0,
                "source_status": "ready_for_manifold_public_derivative_schema_slice_planning",
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
                "handoff_acceptance_status": "not_accepted",
                "downstream_implementation_status": "not_created",
                "downstream_schema_status": "not_created",
                "downstream_route_status": "not_created",
                "downstream_validation_report_status": "not_created",
                "downstream_hostess_boundary_status": "not_created",
                "next_gate": "manifold_repo_public_derivative_schema_slice_or_operator_decision",
            },
            "Manifold public derivative schema handoff package is ready as proposal evidence without touching Manifold or Hostess state",
        ),
        check(
            "manifold_public_derivative_schema_handoff_package.preserves_manifold_and_hostess_authority",
            manifold_public_derivative_schema_handoff_package.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("implementation_plan_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("redaction_review_owner") == "operator"
            and manifold_public_derivative_schema_handoff_package.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_handoff_artifacts
            and all(artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"} for artifact in public_derivative_handoff_artifacts)
            and all(artifact.get("status") == "not_created_by_sidecar" for artifact in public_derivative_handoff_artifacts)
            and public_derivative_handoff_route_boundaries.get("input_payload_class") == "low_rate_advisory_status"
            and public_derivative_handoff_route_boundaries.get("accepts_sanitized_summary_only") is True
            and public_derivative_handoff_route_boundaries.get("requires_operator_approval") is True
            and public_derivative_handoff_route_boundaries.get("requires_redaction_review") is True
            and public_derivative_handoff_route_boundaries.get("allows_endpoint_values") is False
            and public_derivative_handoff_route_boundaries.get("allows_commands") is False
            and public_derivative_handoff_route_boundaries.get("allows_adb") is False
            and public_derivative_handoff_route_boundaries.get("allows_high_rate_payloads") is False
            and public_derivative_handoff_route_boundaries.get("allows_sidecar_direct_hostess_input") is False
            and public_derivative_handoff_route_boundaries.get("creates_public_derivative_artifact") is False
            and public_derivative_handoff_route_boundaries.get("creates_hostess_input") is False
            and manifold_public_derivative_schema_handoff_package.get("hostess_boundary_handoff", {}).get("status") == "future_lane_not_requested"
            and manifold_public_derivative_schema_handoff_package.get("hostess_boundary_handoff", {}).get("sidecar_direct_input_allowed") is False
            and manifold_public_derivative_schema_handoff_package.get("hostess_boundary_handoff", {}).get("requires_manifold_accepted_state") is True
            and manifold_public_derivative_schema_handoff_package.get("hostess_boundary_handoff", {}).get("downstream_descriptor_owner") == "rusty.manifold"
            and not any(
                manifold_public_derivative_schema_handoff_package.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_handoff_package.get("authority", {}),
                "handoff_manifest": public_derivative_handoff_manifest,
                "hostess_boundary_handoff": manifold_public_derivative_schema_handoff_package.get("hostess_boundary_handoff", {}),
                "privacy_boundary": manifold_public_derivative_schema_handoff_package.get("privacy_boundary", {}),
            },
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
                "artifact_status": "not_created_by_sidecar",
                "input_payload_class": "low_rate_advisory_status",
                "accepts_sanitized_summary_only": True,
                "requires_operator_approval": True,
                "requires_redaction_review": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "allows_sidecar_direct_hostess_input": False,
                "creates_public_derivative_artifact": False,
                "creates_hostess_input": False,
                "hostess_status": "future_lane_not_requested",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "downstream_descriptor_owner": "rusty.manifold",
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema handoff package preserves Manifold acceptance/implementation authority and Hostess deferral",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_expectation.ready_for_manifold_response",
            manifold_public_derivative_schema_slice_response_expectation.get("expectation_status") == "ready_for_manifold_public_derivative_schema_slice_response"
            and manifold_public_derivative_schema_slice_response_expectation.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_expectation.get("source_manifold_public_derivative_schema_handoff_package", {}).get("package_status") == "public_derivative_schema_handoff_package_ready"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("branch_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("implementation_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("response_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("decision_status") == "not_decided"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("route_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("audit_record_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("validation_report_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("public_derivative_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_expectation.get("next_gate") == "manifold_public_derivative_schema_slice_response_or_operator_decision",
            {
                "expectation_status": manifold_public_derivative_schema_slice_response_expectation.get("expectation_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_expectation.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_expectation.get("source_manifold_public_derivative_schema_handoff_package", {}).get("package_status"),
                "response_expectation_scope": manifold_public_derivative_schema_slice_response_expectation.get("response_expectation_scope", {}),
                "next_gate": manifold_public_derivative_schema_slice_response_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_manifold_public_derivative_schema_slice_response",
                "fail_count": 0,
                "source_status": "public_derivative_schema_handoff_package_ready",
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
                "next_gate": "manifold_public_derivative_schema_slice_response_or_operator_decision",
            },
            "Manifold public derivative schema slice response expectation defines future response handling without touching Manifold or Hostess state",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_expectation.preserves_manifold_and_hostess_authority",
            manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("implementation_plan_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("redaction_review_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response.get("response_status") == "not_created"
            and public_derivative_slice_response.get("decision_status") == "not_decided"
            and public_derivative_slice_response.get("allowed_response_owner") == "rusty.manifold"
            and public_derivative_slice_response.get("accepted_state_policy") == "manifold_owned_monotonic_revision"
            and public_derivative_slice_response.get("implementation_policy") == "response_records_decision_only"
            and public_derivative_slice_response.get("rollback_policy") == "manifold_owned_disable_route_or_reject_source"
            and public_derivative_slice_response.get("public_derivative_policy") == "response_does_not_create_derivative_artifact"
            and public_derivative_slice_response.get("hostess_input_policy") == "response_does_not_create_hostess_input"
            and manifold_public_derivative_schema_slice_response_expectation.get("hostess_response_gate", {}).get("status") == "future_lane_not_requested"
            and manifold_public_derivative_schema_slice_response_expectation.get("hostess_response_gate", {}).get("sidecar_direct_input_allowed") is False
            and manifold_public_derivative_schema_slice_response_expectation.get("hostess_response_gate", {}).get("requires_manifold_accepted_state") is True
            and manifold_public_derivative_schema_slice_response_expectation.get("hostess_response_gate", {}).get("requires_explicit_operator_request") is True
            and not any(
                manifold_public_derivative_schema_slice_response_expectation.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_expectation.get("authority", {}),
                "expected_manifold_slice_response": public_derivative_slice_response,
                "hostess_response_gate": manifold_public_derivative_schema_slice_response_expectation.get("hostess_response_gate", {}),
                "privacy_boundary": manifold_public_derivative_schema_slice_response_expectation.get("privacy_boundary", {}),
            },
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
                "response_status": "not_created",
                "decision_status": "not_decided",
                "allowed_response_owner": "rusty.manifold",
                "accepted_state_policy": "manifold_owned_monotonic_revision",
                "implementation_policy": "response_records_decision_only",
                "rollback_policy": "manifold_owned_disable_route_or_reject_source",
                "public_derivative_policy": "response_does_not_create_derivative_artifact",
                "hostess_input_policy": "response_does_not_create_hostess_input",
                "hostess_status": "future_lane_not_requested",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response expectation preserves Manifold response authority and Hostess deferral",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_implementation_preflight.ready_for_manifold_slice_response_planning",
            manifold_public_derivative_schema_slice_response_implementation_preflight.get("preflight_status") == "ready_for_manifold_public_derivative_schema_slice_response_planning"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("source_manifold_public_derivative_schema_slice_response_expectation", {}).get("expectation_status") == "ready_for_manifold_public_derivative_schema_slice_response"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("branch_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("implementation_plan_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("response_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("decision_status") == "not_decided"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("route_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("audit_record_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("validation_report_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("public_derivative_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("next_gate") == "manifold_public_derivative_schema_slice_response_handoff_or_operator_decision",
            {
                "preflight_status": manifold_public_derivative_schema_slice_response_implementation_preflight.get("preflight_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_implementation_preflight.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_implementation_preflight.get("source_manifold_public_derivative_schema_slice_response_expectation", {}).get("expectation_status"),
                "implementation_preflight_scope": manifold_public_derivative_schema_slice_response_implementation_preflight.get("implementation_preflight_scope", {}),
                "next_gate": manifold_public_derivative_schema_slice_response_implementation_preflight.get("next_gate"),
            },
            {
                "preflight_status": "ready_for_manifold_public_derivative_schema_slice_response_planning",
                "fail_count": 0,
                "source_status": "ready_for_manifold_public_derivative_schema_slice_response",
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "implementation_plan_status": "not_created",
                "response_status": "not_created",
                "decision_status": "not_decided",
                "schema_status": "not_created",
                "route_status": "not_created",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "validation_report_status": "not_created",
                "public_derivative_status": "not_created",
                "hostess_route_status": "not_created",
                "next_gate": "manifold_public_derivative_schema_slice_response_handoff_or_operator_decision",
            },
            "Manifold public derivative schema slice response implementation preflight is ready as descriptor evidence without touching Manifold or Hostess state",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_implementation_preflight.preserves_manifold_and_hostess_authority",
            manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("implementation_plan_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("redaction_review_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_preflight_requirements.get("implementation_status") == "not_created_by_sidecar"
            and public_derivative_slice_response_preflight_artifacts
            and all(artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"} for artifact in public_derivative_slice_response_preflight_artifacts)
            and all(artifact.get("status") == "not_created_by_sidecar" for artifact in public_derivative_slice_response_preflight_artifacts)
            and public_derivative_slice_response_preflight_route_boundaries.get("input_payload_class") == "low_rate_advisory_status"
            and public_derivative_slice_response_preflight_route_boundaries.get("accepts_sanitized_summary_only") is True
            and public_derivative_slice_response_preflight_route_boundaries.get("requires_operator_approval") is True
            and public_derivative_slice_response_preflight_route_boundaries.get("requires_redaction_review") is True
            and public_derivative_slice_response_preflight_route_boundaries.get("requires_source_chain_digest") is True
            and public_derivative_slice_response_preflight_route_boundaries.get("allows_endpoint_values") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("allows_commands") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("allows_adb") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("allows_high_rate_payloads") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("allows_sidecar_direct_hostess_input") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("creates_public_derivative_artifact") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("creates_hostess_input") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("creates_accepted_state_by_sidecar") is False
            and public_derivative_slice_response_preflight_route_boundaries.get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("status") == "future_lane_not_requested"
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("sidecar_direct_input_allowed") is False
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("requires_manifold_accepted_state") is True
            and manifold_public_derivative_schema_slice_response_implementation_preflight.get("hostess_boundary_preflight", {}).get("requires_explicit_operator_request") is True
            and not any(
                manifold_public_derivative_schema_slice_response_implementation_preflight.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_implementation_preflight.get("authority", {}),
                "manifold_repo_slice_response_requirements": public_derivative_slice_response_preflight_requirements,
                "hostess_boundary_preflight": manifold_public_derivative_schema_slice_response_implementation_preflight.get("hostess_boundary_preflight", {}),
                "privacy_boundary": manifold_public_derivative_schema_slice_response_implementation_preflight.get("privacy_boundary", {}),
            },
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
                "implementation_status": "not_created_by_sidecar",
                "artifact_status": "not_created_by_sidecar",
                "input_payload_class": "low_rate_advisory_status",
                "accepts_sanitized_summary_only": True,
                "requires_operator_approval": True,
                "requires_redaction_review": True,
                "requires_source_chain_digest": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "allows_sidecar_direct_hostess_input": False,
                "creates_public_derivative_artifact": False,
                "creates_hostess_input": False,
                "creates_accepted_state_by_sidecar": False,
                "accepted_state_owner": "rusty.manifold",
                "hostess_status": "future_lane_not_requested",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response implementation preflight preserves Manifold response implementation authority and Hostess deferral",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_handoff_package.ready_for_manifold_slice_response_handoff",
            manifold_public_derivative_schema_slice_response_handoff_package.get("package_status") == "public_derivative_schema_slice_response_handoff_package_ready"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_handoff_package.get("source_manifold_public_derivative_schema_slice_response_implementation_preflight", {}).get("preflight_status") == "ready_for_manifold_public_derivative_schema_slice_response_planning"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("repo_touch_status") == "not_touched"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("branch_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("implementation_plan_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("implementation_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("response_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("decision_status") == "not_decided"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("schema_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("route_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("accepted_state_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("audit_record_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("validation_report_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("public_derivative_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("hostess_route_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}).get("hostess_input_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("next_gate") == "manifold_repo_public_derivative_schema_slice_response_or_operator_decision",
            {
                "package_status": manifold_public_derivative_schema_slice_response_handoff_package.get("package_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_handoff_package.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_handoff_package.get("source_manifold_public_derivative_schema_slice_response_implementation_preflight", {}).get("preflight_status"),
                "package_scope": manifold_public_derivative_schema_slice_response_handoff_package.get("package_scope", {}),
                "next_gate": manifold_public_derivative_schema_slice_response_handoff_package.get("next_gate"),
            },
            {
                "package_status": "public_derivative_schema_slice_response_handoff_package_ready",
                "fail_count": 0,
                "source_status": "ready_for_manifold_public_derivative_schema_slice_response_planning",
                "repo_touch_status": "not_touched",
                "branch_status": "not_created",
                "implementation_plan_status": "not_created",
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
                "hostess_input_status": "not_created",
                "next_gate": "manifold_repo_public_derivative_schema_slice_response_or_operator_decision",
            },
            "Manifold public derivative schema slice response handoff package is ready as descriptor evidence without touching Manifold or Hostess state",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_handoff_package.preserves_manifold_and_hostess_authority",
            manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("implementation_plan_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("request_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("rollback_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("redaction_review_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_handoff_artifacts
            and all(artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"} for artifact in public_derivative_slice_response_handoff_artifacts)
            and all(artifact.get("status") == "not_created_by_sidecar" for artifact in public_derivative_slice_response_handoff_artifacts)
            and public_derivative_slice_response_handoff_route_boundaries.get("input_payload_class") == "low_rate_advisory_status"
            and public_derivative_slice_response_handoff_route_boundaries.get("accepts_sanitized_summary_only") is True
            and public_derivative_slice_response_handoff_route_boundaries.get("requires_operator_approval") is True
            and public_derivative_slice_response_handoff_route_boundaries.get("requires_redaction_review") is True
            and public_derivative_slice_response_handoff_route_boundaries.get("requires_source_chain_digest") is True
            and public_derivative_slice_response_handoff_route_boundaries.get("allows_endpoint_values") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("allows_commands") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("allows_adb") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("allows_high_rate_payloads") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("allows_sidecar_direct_hostess_input") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("creates_public_derivative_artifact") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("creates_hostess_input") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("creates_accepted_state_by_sidecar") is False
            and public_derivative_slice_response_handoff_route_boundaries.get("accepted_state_owner") == "rusty.manifold"
            and public_derivative_slice_response_handoff_manifest.get("handoff_acceptance_status") == "not_accepted"
            and public_derivative_slice_response_handoff_manifest.get("downstream_response_status") == "not_created"
            and public_derivative_slice_response_handoff_manifest.get("downstream_accepted_state_status") == "not_created"
            and public_derivative_slice_response_handoff_manifest.get("downstream_audit_status") == "not_created"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("hostess_boundary_handoff", {}).get("status") == "future_lane_not_requested"
            and manifold_public_derivative_schema_slice_response_handoff_package.get("hostess_boundary_handoff", {}).get("sidecar_direct_input_allowed") is False
            and manifold_public_derivative_schema_slice_response_handoff_package.get("hostess_boundary_handoff", {}).get("requires_manifold_accepted_state") is True
            and manifold_public_derivative_schema_slice_response_handoff_package.get("hostess_boundary_handoff", {}).get("requires_explicit_operator_request") is True
            and not any(
                manifold_public_derivative_schema_slice_response_handoff_package.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_handoff_package.get("authority", {}),
                "handoff_manifest": public_derivative_slice_response_handoff_manifest,
                "hostess_boundary_handoff": manifold_public_derivative_schema_slice_response_handoff_package.get("hostess_boundary_handoff", {}),
                "privacy_boundary": manifold_public_derivative_schema_slice_response_handoff_package.get("privacy_boundary", {}),
            },
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
                "artifact_status": "not_created_by_sidecar",
                "input_payload_class": "low_rate_advisory_status",
                "accepts_sanitized_summary_only": True,
                "requires_operator_approval": True,
                "requires_redaction_review": True,
                "requires_source_chain_digest": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_high_rate_payloads": False,
                "allows_sidecar_direct_hostess_input": False,
                "creates_public_derivative_artifact": False,
                "creates_hostess_input": False,
                "creates_accepted_state_by_sidecar": False,
                "accepted_state_owner": "rusty.manifold",
                "handoff_acceptance_status": "not_accepted",
                "downstream_response_status": "not_created",
                "downstream_accepted_state_status": "not_created",
                "downstream_audit_status": "not_created",
                "hostess_status": "future_lane_not_requested",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response handoff package preserves Manifold response authority and Hostess deferral",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_operator_decision_request.ready_for_operator_decision",
            manifold_public_derivative_schema_slice_response_operator_decision_request.get("request_status") == "operator_decision_required"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("source_manifold_public_derivative_schema_slice_response_handoff_package", {}).get("package_status") == "public_derivative_schema_slice_response_handoff_package_ready"
            and public_derivative_slice_response_operator_decision_scope.get("operator_decision_status") == "not_recorded"
            and public_derivative_slice_response_operator_decision_scope.get("operator_decision_record_status") == "not_created"
            and public_derivative_slice_response_operator_decision_scope.get("manifold_submission_status") == "not_submitted"
            and public_derivative_slice_response_operator_decision_scope.get("manifold_repo_touch_status") == "not_touched"
            and public_derivative_slice_response_operator_decision_scope.get("manifold_response_status") == "not_created"
            and public_derivative_slice_response_operator_decision_scope.get("manifold_accepted_state_status") == "not_created"
            and public_derivative_slice_response_operator_decision_scope.get("manifold_audit_record_status") == "not_created"
            and public_derivative_slice_response_operator_decision_scope.get("hostess_route_status") == "not_created"
            and public_derivative_slice_response_operator_decision_scope.get("hostess_input_status") == "not_created"
            and public_derivative_slice_response_operator_decision_scope.get("adb_status") == "not_used"
            and public_derivative_slice_response_operator_decision_scope.get("command_status") == "no_commands"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("next_gate") == "operator_decision_or_manifold_repo_public_derivative_schema_slice_response",
            {
                "request_status": manifold_public_derivative_schema_slice_response_operator_decision_request.get("request_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_operator_decision_request.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_operator_decision_request.get("source_manifold_public_derivative_schema_slice_response_handoff_package", {}).get("package_status"),
                "decision_request_scope": public_derivative_slice_response_operator_decision_scope,
                "next_gate": manifold_public_derivative_schema_slice_response_operator_decision_request.get("next_gate"),
            },
            {
                "request_status": "operator_decision_required",
                "fail_count": 0,
                "source_status": "public_derivative_schema_slice_response_handoff_package_ready",
                "operator_decision_status": "not_recorded",
                "operator_decision_record_status": "not_created",
                "manifold_submission_status": "not_submitted",
                "manifold_repo_touch_status": "not_touched",
                "manifold_response_status": "not_created",
                "manifold_accepted_state_status": "not_created",
                "manifold_audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
                "next_gate": "operator_decision_or_manifold_repo_public_derivative_schema_slice_response",
            },
            "Manifold public derivative schema slice response operator decision request is ready without creating downstream submission, state, or Hostess input",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_operator_decision_request.preserves_hostess_manifold_integration_gate",
            manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("operator_decision_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("submission_request_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("hostess_boundary_descriptor_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("future_hostess_route_owner") == "rusty.hostess"
            and manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_operator_decision_manifold_gate.get("submission_status") == "not_submitted"
            and public_derivative_slice_response_operator_decision_manifold_gate.get("acceptance_owner") == "rusty.manifold"
            and public_derivative_slice_response_operator_decision_manifold_gate.get("sidecar_can_submit_directly") is False
            and public_derivative_slice_response_operator_decision_manifold_gate.get("sidecar_can_accept") is False
            and public_derivative_slice_response_operator_decision_manifold_gate.get("sidecar_can_create_state") is False
            and public_derivative_slice_response_operator_decision_manifold_gate.get("sidecar_can_create_response") is False
            and public_derivative_slice_response_operator_decision_hostess_gate.get("status") == "future_lane_not_requested"
            and public_derivative_slice_response_operator_decision_hostess_gate.get("route_status") == "not_created"
            and public_derivative_slice_response_operator_decision_hostess_gate.get("input_status") == "not_created"
            and public_derivative_slice_response_operator_decision_hostess_gate.get("device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_operator_decision_hostess_gate.get("consumes_only") == "manifold_accepted_state_or_operator_request_descriptor"
            and public_derivative_slice_response_operator_decision_hostess_gate.get("sidecar_direct_input_allowed") is False
            and public_derivative_slice_response_operator_decision_hostess_gate.get("requires_manifold_accepted_state") is True
            and public_derivative_slice_response_operator_decision_hostess_gate.get("requires_explicit_operator_request") is True
            and public_derivative_slice_response_operator_decision_hostess_gate.get("boundary_descriptor_owner") == "rusty.manifold"
            and public_derivative_slice_response_operator_decision_hostess_gate.get("future_route_owner") == "rusty.hostess"
            and not any(
                manifold_public_derivative_schema_slice_response_operator_decision_request.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_operator_decision_request.get("authority", {}),
                "manifold_submission_gate": public_derivative_slice_response_operator_decision_manifold_gate,
                "hostess_boundary_gate": public_derivative_slice_response_operator_decision_hostess_gate,
                "privacy_boundary": manifold_public_derivative_schema_slice_response_operator_decision_request.get("privacy_boundary", {}),
            },
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
                "submission_status": "not_submitted",
                "acceptance_owner": "rusty.manifold",
                "sidecar_can_submit_directly": False,
                "sidecar_can_accept": False,
                "sidecar_can_create_state": False,
                "sidecar_can_create_response": False,
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "hostess_consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response operator decision request preserves Manifold submission authority and future Hostess route ownership",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.ready_for_operator_decision_record",
            manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("expectation_status") == "ready_for_operator_decision_record"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("source_operator_decision_request", {}).get("request_status") == "operator_decision_required"
            and public_derivative_slice_response_operator_record_scope.get("operator_decision_record_status") == "not_created"
            and public_derivative_slice_response_operator_record_scope.get("operator_decision_status") == "not_recorded"
            and public_derivative_slice_response_operator_record_scope.get("manifold_submission_status") == "not_submitted"
            and public_derivative_slice_response_operator_record_scope.get("manifold_repo_touch_status") == "not_touched"
            and public_derivative_slice_response_operator_record_scope.get("manifold_response_status") == "not_created"
            and public_derivative_slice_response_operator_record_scope.get("manifold_accepted_state_status") == "not_created"
            and public_derivative_slice_response_operator_record_scope.get("manifold_audit_record_status") == "not_created"
            and public_derivative_slice_response_operator_record_scope.get("hostess_route_status") == "not_created"
            and public_derivative_slice_response_operator_record_scope.get("hostess_input_status") == "not_created"
            and public_derivative_slice_response_operator_record_scope.get("adb_status") == "not_used"
            and public_derivative_slice_response_operator_record_scope.get("command_status") == "no_commands"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("next_gate") == "operator_decision_record_or_manifold_repo_public_derivative_schema_slice_response",
            {
                "expectation_status": manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("expectation_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("source_operator_decision_request", {}).get("request_status"),
                "expectation_scope": public_derivative_slice_response_operator_record_scope,
                "next_gate": manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_operator_decision_record",
                "fail_count": 0,
                "source_status": "operator_decision_required",
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
                "next_gate": "operator_decision_record_or_manifold_repo_public_derivative_schema_slice_response",
            },
            "Manifold public derivative schema slice response operator decision record expectation is ready without creating the record, submission, state, audit, or Hostess input",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.preserves_operator_manifold_hostess_authority",
            manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("operator_decision_record_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("submission_request_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("hostess_boundary_descriptor_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("future_hostess_route_owner") == "rusty.hostess"
            and manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_operator_record.get("record_status") == "not_created"
            and public_derivative_slice_response_operator_record.get("allowed_record_owner") == "operator"
            and set(public_derivative_slice_response_operator_record.get("allowed_decisions", [])) == {"submit_to_manifold_review", "hold_for_revision", "reject_sidecar_handoff"}
            and public_derivative_slice_response_operator_record.get("default_without_record") == "hold"
            and public_derivative_slice_response_operator_record.get("creates_manifold_state") is False
            and public_derivative_slice_response_operator_record.get("creates_hostess_input") is False
            and public_derivative_slice_response_operator_record_manifold_gate.get("submission_status") == "not_submitted"
            and public_derivative_slice_response_operator_record_manifold_gate.get("submission_owner_after_operator_decision") == "operator"
            and public_derivative_slice_response_operator_record_manifold_gate.get("acceptance_owner") == "rusty.manifold"
            and public_derivative_slice_response_operator_record_manifold_gate.get("sidecar_can_submit_directly") is False
            and public_derivative_slice_response_operator_record_manifold_gate.get("sidecar_can_accept") is False
            and public_derivative_slice_response_operator_record_manifold_gate.get("sidecar_can_create_state") is False
            and public_derivative_slice_response_operator_record_hostess_gate.get("status") == "future_lane_not_requested"
            and public_derivative_slice_response_operator_record_hostess_gate.get("route_status") == "not_created"
            and public_derivative_slice_response_operator_record_hostess_gate.get("input_status") == "not_created"
            and public_derivative_slice_response_operator_record_hostess_gate.get("future_route_owner") == "rusty.hostess"
            and public_derivative_slice_response_operator_record_hostess_gate.get("boundary_descriptor_owner") == "rusty.manifold"
            and public_derivative_slice_response_operator_record_hostess_gate.get("consumes_only") == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and public_derivative_slice_response_operator_record_hostess_gate.get("device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_operator_record_hostess_gate.get("sidecar_direct_input_allowed") is False
            and public_derivative_slice_response_operator_record_hostess_gate.get("requires_manifold_accepted_state") is True
            and public_derivative_slice_response_operator_record_hostess_gate.get("requires_explicit_operator_request") is True
            and not any(
                manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("authority", {}),
                "expected_operator_decision_record": public_derivative_slice_response_operator_record,
                "manifold_submission_after_decision": public_derivative_slice_response_operator_record_manifold_gate,
                "hostess_boundary_after_decision": public_derivative_slice_response_operator_record_hostess_gate,
                "privacy_boundary": manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.get("privacy_boundary", {}),
            },
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
                "record_status": "not_created",
                "allowed_record_owner": "operator",
                "allowed_decisions": ["submit_to_manifold_review", "hold_for_revision", "reject_sidecar_handoff"],
                "default_without_record": "hold",
                "creates_manifold_state": False,
                "creates_hostess_input": False,
                "submission_status": "not_submitted",
                "sidecar_can_submit_directly": False,
                "sidecar_can_accept": False,
                "sidecar_can_create_state": False,
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "boundary_descriptor_owner": "rusty.manifold",
                "hostess_consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
                "hostess_device_action_authority": "not_in_sidecar",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response operator decision record expectation preserves operator-owned records, Manifold submission authority, and future Hostess route ownership",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_submission_envelope_expectation.ready_for_manifold_submission_envelope",
            manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("expectation_status") == "ready_for_manifold_submission_envelope"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("source_operator_decision_record_expectation", {}).get("expectation_status") == "ready_for_operator_decision_record"
            and public_derivative_slice_response_submission_envelope_scope.get("operator_decision_record_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_scope.get("operator_decision_status") == "not_recorded"
            and public_derivative_slice_response_submission_envelope_scope.get("submission_envelope_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_scope.get("manifold_submission_status") == "not_submitted"
            and public_derivative_slice_response_submission_envelope_scope.get("manifold_repo_touch_status") == "not_touched"
            and public_derivative_slice_response_submission_envelope_scope.get("manifold_response_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_scope.get("manifold_accepted_state_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_scope.get("manifold_audit_record_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_scope.get("hostess_route_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_scope.get("hostess_input_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_scope.get("adb_status") == "not_used"
            and public_derivative_slice_response_submission_envelope_scope.get("command_status") == "no_commands"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("next_gate") == "operator_submission_envelope_or_manifold_repo_public_derivative_schema_slice_response",
            {
                "expectation_status": manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("expectation_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("source_operator_decision_record_expectation", {}).get("expectation_status"),
                "expectation_scope": public_derivative_slice_response_submission_envelope_scope,
                "next_gate": manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_manifold_submission_envelope",
                "fail_count": 0,
                "source_status": "ready_for_operator_decision_record",
                "operator_decision_record_status": "not_created",
                "operator_decision_status": "not_recorded",
                "submission_envelope_status": "not_created",
                "manifold_submission_status": "not_submitted",
                "manifold_repo_touch_status": "not_touched",
                "manifold_response_status": "not_created",
                "manifold_accepted_state_status": "not_created",
                "manifold_audit_record_status": "not_created",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
                "next_gate": "operator_submission_envelope_or_manifold_repo_public_derivative_schema_slice_response",
            },
            "Manifold public derivative schema slice response submission envelope expectation is ready without creating an envelope, submission, state, audit, or Hostess input",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_submission_envelope_expectation.preserves_operator_manifold_hostess_authority",
            manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("submission_envelope_owner_after_operator_decision") == "operator"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("submission_request_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("submission_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("hostess_boundary_descriptor_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("future_hostess_route_owner") == "rusty.hostess"
            and manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_submission_envelope.get("envelope_status") == "not_created"
            and public_derivative_slice_response_submission_envelope.get("allowed_envelope_owner") == "operator"
            and public_derivative_slice_response_submission_envelope.get("target_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_envelope.get("submit_decision_required") == "submit_to_manifold_review"
            and public_derivative_slice_response_submission_envelope.get("accepted_input_policy") == "sanitized_summary_only"
            and public_derivative_slice_response_submission_envelope.get("creates_manifold_state") is False
            and public_derivative_slice_response_submission_envelope.get("creates_hostess_input") is False
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("submission_status") == "not_submitted"
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("intake_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("acceptance_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("response_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("accepted_state_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("audit_owner") == "rusty.manifold.audit"
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("requires_operator_decision_record") is True
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("requires_submit_decision_value") == "submit_to_manifold_review"
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("sidecar_can_submit_directly") is False
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("sidecar_can_accept") is False
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("sidecar_can_create_state") is False
            and public_derivative_slice_response_submission_envelope_manifold_gate.get("sidecar_can_create_response") is False
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("status") == "future_lane_not_requested"
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("route_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("input_status") == "not_created"
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("future_route_owner") == "rusty.hostess"
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("boundary_descriptor_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("consumes_only") == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("sidecar_direct_input_allowed") is False
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("requires_manifold_accepted_state") is True
            and public_derivative_slice_response_submission_envelope_hostess_gate.get("requires_explicit_operator_request") is True
            and not any(
                manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("authority", {}),
                "expected_submission_envelope": public_derivative_slice_response_submission_envelope,
                "manifold_intake_after_envelope": public_derivative_slice_response_submission_envelope_manifold_gate,
                "hostess_boundary_after_envelope": public_derivative_slice_response_submission_envelope_hostess_gate,
                "privacy_boundary": manifold_public_derivative_schema_slice_response_submission_envelope_expectation.get("privacy_boundary", {}),
            },
            {
                "submission_envelope_owner_after_operator_decision": "operator",
                "submission_request_owner": "operator",
                "submission_acceptance_owner": "rusty.manifold",
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
                "envelope_status": "not_created",
                "allowed_envelope_owner": "operator",
                "target_owner": "rusty.manifold",
                "submit_decision_required": "submit_to_manifold_review",
                "accepted_input_policy": "sanitized_summary_only",
                "creates_manifold_state": False,
                "creates_hostess_input": False,
                "submission_status": "not_submitted",
                "sidecar_can_submit_directly": False,
                "sidecar_can_accept": False,
                "sidecar_can_create_state": False,
                "sidecar_can_create_response": False,
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "hostess_consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response submission envelope expectation preserves operator-owned envelope, Manifold intake authority, and future Hostess route ownership",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.ready_for_manifold_submission_intake_response",
            manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("expectation_status") == "ready_for_manifold_submission_intake_response"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("source_submission_envelope_expectation", {}).get("expectation_status") == "ready_for_manifold_submission_envelope"
            and public_derivative_slice_response_submission_intake_scope.get("operator_decision_record_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("operator_decision_status") == "not_recorded"
            and public_derivative_slice_response_submission_intake_scope.get("submission_envelope_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("manifold_submission_status") == "not_submitted"
            and public_derivative_slice_response_submission_intake_scope.get("manifold_repo_touch_status") == "not_touched"
            and public_derivative_slice_response_submission_intake_scope.get("manifold_intake_response_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("manifold_decision_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("manifold_accepted_state_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("manifold_audit_record_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("hostess_route_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("hostess_input_status") == "not_created"
            and public_derivative_slice_response_submission_intake_scope.get("adb_status") == "not_used"
            and public_derivative_slice_response_submission_intake_scope.get("command_status") == "no_commands"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("next_gate") == "operator_submission_envelope_or_manifold_repo_submission_intake_response",
            {
                "expectation_status": manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("expectation_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("source_submission_envelope_expectation", {}).get("expectation_status"),
                "expectation_scope": public_derivative_slice_response_submission_intake_scope,
                "next_gate": manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("next_gate"),
            },
            {
                "expectation_status": "ready_for_manifold_submission_intake_response",
                "fail_count": 0,
                "source_status": "ready_for_manifold_submission_envelope",
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
                "next_gate": "operator_submission_envelope_or_manifold_repo_submission_intake_response",
            },
            "Manifold public derivative schema slice response submission intake response expectation is ready without creating a submission, response, state, audit, or Hostess input",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.preserves_operator_manifold_hostess_authority",
            manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("submission_envelope_owner_after_operator_decision") == "operator"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("submission_request_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("intake_response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("submission_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("handoff_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("hostess_boundary_descriptor_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("future_hostess_route_owner") == "rusty.hostess"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_submission_intake_response.get("response_status") == "not_created"
            and public_derivative_slice_response_submission_intake_response.get("allowed_response_owner") == "rusty.manifold"
            and set(public_derivative_slice_response_submission_intake_response.get("allowed_decisions", [])) == {"received_for_review", "request_submission_revision", "reject_submission_envelope"}
            and public_derivative_slice_response_submission_intake_response.get("default_without_response") == "hold"
            and public_derivative_slice_response_submission_intake_response.get("creates_accepted_state") is False
            and public_derivative_slice_response_submission_intake_response.get("creates_hostess_input") is False
            and public_derivative_slice_response_submission_intake_manifold_gate.get("response_status") == "not_created"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("submission_status") == "not_submitted"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("acceptance_status") == "not_accepted"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("accepted_state_status") == "not_created"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("audit_record_status") == "not_created"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("validation_report_status") == "not_created"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("response_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("acceptance_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("accepted_state_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("audit_owner") == "rusty.manifold.audit"
            and public_derivative_slice_response_submission_intake_manifold_gate.get("requires_operator_submission_envelope") is True
            and public_derivative_slice_response_submission_intake_manifold_gate.get("sidecar_can_create_response") is False
            and public_derivative_slice_response_submission_intake_manifold_gate.get("sidecar_can_accept") is False
            and public_derivative_slice_response_submission_intake_manifold_gate.get("sidecar_can_create_state") is False
            and public_derivative_slice_response_submission_intake_manifold_gate.get("sidecar_can_create_audit") is False
            and public_derivative_slice_response_submission_intake_hostess_gate.get("status") == "future_lane_not_requested"
            and public_derivative_slice_response_submission_intake_hostess_gate.get("route_status") == "not_created"
            and public_derivative_slice_response_submission_intake_hostess_gate.get("input_status") == "not_created"
            and public_derivative_slice_response_submission_intake_hostess_gate.get("device_action_authority") == "not_in_sidecar"
            and public_derivative_slice_response_submission_intake_hostess_gate.get("future_route_owner") == "rusty.hostess"
            and public_derivative_slice_response_submission_intake_hostess_gate.get("boundary_descriptor_owner") == "rusty.manifold"
            and public_derivative_slice_response_submission_intake_hostess_gate.get("consumes_only") == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and public_derivative_slice_response_submission_intake_hostess_gate.get("sidecar_direct_input_allowed") is False
            and public_derivative_slice_response_submission_intake_hostess_gate.get("requires_manifold_accepted_state") is True
            and public_derivative_slice_response_submission_intake_hostess_gate.get("requires_explicit_operator_request") is True
            and not any(
                manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("authority", {}),
                "expected_manifold_intake_response": public_derivative_slice_response_submission_intake_response,
                "manifold_acceptance_after_response": public_derivative_slice_response_submission_intake_manifold_gate,
                "hostess_boundary_after_response": public_derivative_slice_response_submission_intake_hostess_gate,
                "privacy_boundary": manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.get("privacy_boundary", {}),
            },
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
                "response_status": "not_created",
                "allowed_response_owner": "rusty.manifold",
                "allowed_decisions": ["received_for_review", "request_submission_revision", "reject_submission_envelope"],
                "default_without_response": "hold",
                "creates_accepted_state": False,
                "creates_hostess_input": False,
                "submission_status": "not_submitted",
                "acceptance_status": "not_accepted",
                "accepted_state_status": "not_created",
                "audit_record_status": "not_created",
                "validation_report_status": "not_created",
                "sidecar_can_create_response": False,
                "sidecar_can_accept": False,
                "sidecar_can_create_state": False,
                "sidecar_can_create_audit": False,
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "hostess_consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "requires_manifold_accepted_state": True,
                "requires_explicit_operator_request": True,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response submission intake response expectation preserves Manifold-owned response, accepted-state, audit, and future Hostess route ownership",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.ready_for_manifold_planning",
            manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("preflight_status") == "ready_for_manifold_submission_intake_response_implementation_planning"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("summary", {}).get("fail_count") == 0
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("source_submission_intake_response_expectation", {}).get("expectation_status") == "ready_for_manifold_submission_intake_response"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("repo_touch_status") == "not_touched"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("branch_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("implementation_plan_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("submission_envelope_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("submission_status") == "not_submitted"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("intake_response_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("decision_status") == "not_decided"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("response_schema_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("route_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("accepted_state_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("audit_record_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("validation_report_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("hostess_boundary_descriptor_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("hostess_route_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("hostess_input_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("adb_status") == "not_used"
            and public_derivative_slice_response_submission_intake_preflight_scope.get("command_status") == "no_commands"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("next_gate") == "manifold_submission_intake_response_handoff_or_manifold_repo_submission_intake_response",
            {
                "preflight_status": manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("preflight_status"),
                "fail_count": manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("summary", {}).get("fail_count"),
                "source_status": manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("source_submission_intake_response_expectation", {}).get("expectation_status"),
                "implementation_preflight_scope": public_derivative_slice_response_submission_intake_preflight_scope,
                "next_gate": manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("next_gate"),
            },
            {
                "preflight_status": "ready_for_manifold_submission_intake_response_implementation_planning",
                "fail_count": 0,
                "source_status": "ready_for_manifold_submission_intake_response",
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
                "hostess_boundary_descriptor_status": "not_created",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "adb_status": "not_used",
                "command_status": "no_commands",
                "next_gate": "manifold_submission_intake_response_handoff_or_manifold_repo_submission_intake_response",
            },
            "Manifold public derivative schema slice response submission intake response implementation preflight is ready without creating response implementation, state, audit, validation report, Hostess input, ADB, or commands",
        ),
        check(
            "manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.preserves_manifold_hostess_authority",
            manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("submission_envelope_owner") == "operator"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("intake_response_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("intake_response_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("submission_acceptance_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("decision_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("response_schema_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("route_implementation_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("runtime_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("session_authority_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("audit_owner") == "rusty.manifold.audit"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("accepted_state_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("validation_report_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("hostess_boundary_descriptor_owner") == "rusty.manifold"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("future_hostess_route_owner") == "rusty.hostess"
            and manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}).get("hostess_device_action_authority") == "not_in_sidecar"
            and set(public_derivative_slice_response_submission_intake_preflight_requirements.get("required_response_decisions", [])) == {"received_for_review", "request_submission_revision", "reject_submission_envelope"}
            and {"response_schema", "route_handler", "decision_event_schema", "submission_envelope_schema_binding", "accepted_state_candidate_fixture", "audit_fixture", "validation_report_fixture", "rejection_fixture", "revision_fixture", "hostess_boundary_descriptor", "rollback_descriptor"} <= {artifact.get("artifact_kind") for artifact in public_derivative_slice_response_submission_intake_preflight_artifacts}
            and all(artifact.get("status") == "not_created_by_sidecar" for artifact in public_derivative_slice_response_submission_intake_preflight_artifacts)
            and all(artifact.get("owner") in {"rusty.manifold", "rusty.manifold.audit"} for artifact in public_derivative_slice_response_submission_intake_preflight_artifacts)
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("accepts_sanitized_summary_only") is True
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("requires_operator_submission_envelope") is True
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("allows_endpoint_values") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("allows_commands") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("allows_adb") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("allows_sidecar_direct_hostess_input") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("creates_response_by_sidecar") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("creates_accepted_state_by_sidecar") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("creates_audit_by_sidecar") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("creates_validation_report_by_sidecar") is False
            and public_derivative_slice_response_submission_intake_preflight_route_boundaries.get("creates_hostess_input") is False
            and public_derivative_slice_response_submission_intake_preflight_hostess_gate.get("status") == "future_lane_not_requested"
            and public_derivative_slice_response_submission_intake_preflight_hostess_gate.get("route_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_hostess_gate.get("input_status") == "not_created"
            and public_derivative_slice_response_submission_intake_preflight_hostess_gate.get("consumes_only") == "manifold_accepted_state_or_explicit_operator_request_descriptor"
            and public_derivative_slice_response_submission_intake_preflight_hostess_gate.get("sidecar_direct_input_allowed") is False
            and not any(
                manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("privacy_boundary", {}).get(key)
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
                "authority": manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("authority", {}),
                "artifact_kinds": sorted({artifact.get("artifact_kind") for artifact in public_derivative_slice_response_submission_intake_preflight_artifacts}),
                "artifact_owners": sorted({artifact.get("owner") for artifact in public_derivative_slice_response_submission_intake_preflight_artifacts}),
                "artifact_statuses": sorted({artifact.get("status") for artifact in public_derivative_slice_response_submission_intake_preflight_artifacts}),
                "required_route_boundaries": public_derivative_slice_response_submission_intake_preflight_route_boundaries,
                "hostess_boundary_preflight": public_derivative_slice_response_submission_intake_preflight_hostess_gate,
                "privacy_boundary": manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.get("privacy_boundary", {}),
            },
            {
                "submission_envelope_owner": "operator",
                "intake_response_implementation_owner": "rusty.manifold",
                "intake_response_owner": "rusty.manifold",
                "submission_acceptance_owner": "rusty.manifold",
                "decision_owner": "rusty.manifold",
                "response_schema_owner": "rusty.manifold",
                "route_implementation_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "accepted_state_owner": "rusty.manifold",
                "validation_report_owner": "rusty.manifold",
                "hostess_boundary_descriptor_owner": "rusty.manifold",
                "future_hostess_route_owner": "rusty.hostess",
                "hostess_device_action_authority": "not_in_sidecar",
                "required_response_decisions": ["received_for_review", "request_submission_revision", "reject_submission_envelope"],
                "artifacts_manifold_owned_not_created": True,
                "accepts_sanitized_summary_only": True,
                "requires_operator_submission_envelope": True,
                "allows_endpoint_values": False,
                "allows_commands": False,
                "allows_adb": False,
                "allows_sidecar_direct_hostess_input": False,
                "creates_response_by_sidecar": False,
                "creates_accepted_state_by_sidecar": False,
                "creates_audit_by_sidecar": False,
                "creates_validation_report_by_sidecar": False,
                "creates_hostess_input": False,
                "hostess_status": "future_lane_not_requested",
                "hostess_route_status": "not_created",
                "hostess_input_status": "not_created",
                "hostess_consumes_only": "manifold_accepted_state_or_explicit_operator_request_descriptor",
                "sidecar_direct_input_allowed": False,
                "privacy_flags_all_false": True,
            },
            "Manifold public derivative schema slice response submission intake response implementation preflight preserves Manifold-owned implementation artifacts and Hostess deferral",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    manual_review_count = sum(1 for row in checks if row["status"] == "manual_review")
    overall_status = "acceptance_ready" if fail_count == 0 and manual_review_count == 0 else "acceptance_blocked"

    return {
        "schema": "rusty.quest.sidecar.integration_acceptance_scorecard.v1",
        "scorecard_id": "scorecard.sidecar_integration.synthetic.001",
        "generated_at": now,
        "scope": {
            "repo": "rusty-quest-sidecar-mesh",
            "slice": "integration_acceptance_scorecard",
            "implementation_profile": "termux",
            "source_mode": "fixtures_only",
        },
        "overall_status": overall_status,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": sum(1 for row in checks if row["status"] == "pass"),
            "manual_review_count": manual_review_count,
            "fail_count": fail_count,
            "damaged_expected_failure_count": len(damaged_failures),
            "valid_fixture_count": len(valid_results),
        },
        "authority_boundary": [
            "Integration acceptance scorecards summarize local fixture evidence only.",
            "Integration acceptance scorecards do not approve live work, select endpoints, open sockets, use ADB, install apps, launch apps, execute commands, or mutate Manifold state.",
            "Integration acceptance scorecards are proposal evidence; Manifold remains the future owner of acceptance, rejection, revision, lease, and audit records.",
        ],
        "next_gate": "manifold_submission_intake_response_handoff_or_manifold_repo_submission_intake_response",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output scorecard path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        scorecard = build_scorecard(repo_root, args.now)
        write_json(Path(args.output), scorecard)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"evaluate_integration_acceptance failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": scorecard["overall_status"], "check_count": scorecard["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
