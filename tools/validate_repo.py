#!/usr/bin/env python3
"""Validate the private Rusty Quest sidecar mesh contract scaffold."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA_IDS = {
    "rusty.quest.sidecar.hostess_boundary_descriptor_expectation.v1": "schemas/rusty.quest.sidecar.hostess_boundary_descriptor_expectation.v1.schema.json",
    "rusty.quest.sidecar.agent_profile.v1": "schemas/rusty.quest.sidecar.agent_profile.v1.schema.json",
    "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1": "schemas/rusty.quest.sidecar.configured_peer_rehearsal_plan.v1.schema.json",
    "rusty.quest.sidecar.integration_acceptance_scorecard.v1": "schemas/rusty.quest.sidecar.integration_acceptance_scorecard.v1.schema.json",
    "rusty.quest.sidecar.no_network_agent_run.v1": "schemas/rusty.quest.sidecar.no_network_agent_run.v1.schema.json",
    "rusty.quest.sidecar.no_network_agent_recipe.v1": "schemas/rusty.quest.sidecar.no_network_agent_recipe.v1.schema.json",
    "rusty.quest.sidecar.no_network_agent_recipe_review.v1": "schemas/rusty.quest.sidecar.no_network_agent_recipe_review.v1.schema.json",
    "rusty.quest.sidecar.no_network_prototype_handoff_review.v1": "schemas/rusty.quest.sidecar.no_network_prototype_handoff_review.v1.schema.json",
    "rusty.quest.sidecar.observation.v1": "schemas/rusty.quest.sidecar.observation.v1.schema.json",
    "rusty.quest.sidecar.mesh_handoff.v1": "schemas/rusty.quest.sidecar.mesh_handoff.v1.schema.json",
    "rusty.quest.sidecar.manifold_adapter_contract_review.v1": "schemas/rusty.quest.sidecar.manifold_adapter_contract_review.v1.schema.json",
    "rusty.quest.sidecar.manifold_adapter_proposal.v1": "schemas/rusty.quest.sidecar.manifold_adapter_proposal.v1.schema.json",
    "rusty.quest.sidecar.manifold_contract_intake_request.v1": "schemas/rusty.quest.sidecar.manifold_contract_intake_request.v1.schema.json",
    "rusty.quest.sidecar.manifold_handoff_package.v1": "schemas/rusty.quest.sidecar.manifold_handoff_package.v1.schema.json",
    "rusty.quest.sidecar.manifold_response_implementation_preflight.v1": "schemas/rusty.quest.sidecar.manifold_response_implementation_preflight.v1.schema.json",
    "rusty.quest.sidecar.manifold_response_handoff_package.v1": "schemas/rusty.quest.sidecar.manifold_response_handoff_package.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_handoff_package.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_handoff_package.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_implementation_preflight.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_implementation_preflight.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_response_expectation.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_response_expectation.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_expectation.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_expectation.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_handoff_package.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_handoff_package.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_implementation_preflight.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_implementation_preflight.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_envelope_expectation.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_envelope_expectation.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_handoff_package.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_handoff_package.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.v1.schema.json",
    "rusty.quest.sidecar.manifold_public_derivative_schema_request.v1": "schemas/rusty.quest.sidecar.manifold_public_derivative_schema_request.v1.schema.json",
    "rusty.quest.sidecar.manifold_route_blueprint.v1": "schemas/rusty.quest.sidecar.manifold_route_blueprint.v1.schema.json",
    "rusty.quest.sidecar.manifold_route_design_response_expectation.v1": "schemas/rusty.quest.sidecar.manifold_route_design_response_expectation.v1.schema.json",
    "rusty.quest.sidecar.manifold_route_design_review_request.v1": "schemas/rusty.quest.sidecar.manifold_route_design_review_request.v1.schema.json",
    "rusty.quest.sidecar.private_rehearsal_approval_request.v1": "schemas/rusty.quest.sidecar.private_rehearsal_approval_request.v1.schema.json",
    "rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1": "schemas/rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1.schema.json",
    "rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1": "schemas/rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1.schema.json",
    "rusty.quest.sidecar.public_lab_artifact_drift_review.v1": "schemas/rusty.quest.sidecar.public_lab_artifact_drift_review.v1.schema.json",
    "rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1": "schemas/rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1.schema.json",
    "rusty.quest.sidecar.public_lab_artifact_intake_report.v1": "schemas/rusty.quest.sidecar.public_lab_artifact_intake_report.v1.schema.json",
    "rusty.quest.sidecar.validation_scorecard.v1": "schemas/rusty.quest.sidecar.validation_scorecard.v1.schema.json",
}

REQUIRED_FILES = [
    "AGENTS.md",
    "README.md",
    "docs/ARCHITECTURE.md",
    "docs/CONFIGURED_PEER_REHEARSAL_PLAN.md",
    "docs/HOSTESS_BOUNDARY_DESCRIPTOR_EXPECTATION.md",
    "docs/INTEGRATION_ROADMAP.md",
    "docs/INTEGRATION_ACCEPTANCE_SCORECARD.md",
    "docs/TERMUX_CAPABILITY_MAP.md",
    "docs/MANIFOLD_HANDOFF.md",
    "docs/MANIFOLD_ADAPTER_CONTRACT_REVIEW.md",
    "docs/MANIFOLD_ADAPTER_PROPOSAL.md",
    "docs/MANIFOLD_CONTRACT_INTAKE_REQUEST.md",
    "docs/MANIFOLD_HANDOFF_PACKAGE.md",
    "docs/MANIFOLD_RESPONSE_IMPLEMENTATION_PREFLIGHT.md",
    "docs/MANIFOLD_RESPONSE_HANDOFF_PACKAGE.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_HANDOFF_PACKAGE.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_IMPLEMENTATION_PREFLIGHT.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_RESPONSE_EXPECTATION.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_REQUEST.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_EXPECTATION.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_HANDOFF_PACKAGE.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_IMPLEMENTATION_PREFLIGHT.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_OPERATOR_DECISION_RECORD_EXPECTATION.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_OPERATOR_DECISION_REQUEST.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_ENVELOPE_EXPECTATION.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_INTAKE_RESPONSE_EXPECTATION.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_INTAKE_RESPONSE_HANDOFF_PACKAGE.md",
    "docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_INTAKE_RESPONSE_IMPLEMENTATION_PREFLIGHT.md",
    "docs/MANIFOLD_ROUTE_BLUEPRINT.md",
    "docs/MANIFOLD_ROUTE_DESIGN_RESPONSE_EXPECTATION.md",
    "docs/MANIFOLD_ROUTE_DESIGN_REVIEW_REQUEST.md",
    "docs/NO_NETWORK_AGENT_PROTOTYPE.md",
    "docs/NO_NETWORK_AGENT_RECIPE.md",
    "docs/NO_NETWORK_AGENT_RECIPE_REVIEW.md",
    "docs/NO_NETWORK_PROTOTYPE_HANDOFF_REVIEW.md",
    "docs/PRIVATE_REHEARSAL_APPROVAL_REQUEST.md",
    "docs/PRIVATE_REHEARSAL_EVIDENCE_EXPECTATION.md",
    "docs/PRIVATE_REHEARSAL_PUBLIC_DERIVATIVE_EXPECTATION.md",
    "docs/PUBLIC_LAB_ARTIFACT_DRIFT_REVIEW.md",
    "docs/PUBLIC_LAB_ARTIFACT_INTAKE.md",
    "fixtures/README.md",
    *SCHEMA_IDS.values(),
    "fixtures/valid/termux-agent-profile.synthetic.json",
    "fixtures/valid/configured-peer-rehearsal-plan.synthetic.json",
    "fixtures/valid/hostess-boundary-descriptor-expectation.synthetic.json",
    "fixtures/valid/integration-acceptance-scorecard.synthetic.json",
    "fixtures/valid/no-network-agent-observation.synthetic.json",
    "fixtures/valid/no-network-agent-run.synthetic.json",
    "fixtures/valid/no-network-agent-recipe.synthetic.json",
    "fixtures/valid/no-network-agent-recipe-review.synthetic.json",
    "fixtures/valid/no-network-prototype-handoff-review.synthetic.json",
    "fixtures/valid/termux-observation.synthetic.json",
    "fixtures/valid/mesh-handoff.synthetic.json",
    "fixtures/valid/mesh-handoff.with-public-lab-intake.synthetic.json",
    "fixtures/valid/manifold-adapter-contract-review.synthetic.json",
    "fixtures/valid/manifold-adapter-proposal.synthetic.json",
    "fixtures/valid/manifold-contract-intake-request.synthetic.json",
    "fixtures/valid/manifold-handoff-package.synthetic.json",
    "fixtures/valid/manifold-response-implementation-preflight.synthetic.json",
    "fixtures/valid/manifold-response-handoff-package.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-handoff-package.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-implementation-preflight.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-response-expectation.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-expectation.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-handoff-package.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json",
    "fixtures/valid/manifold-public-derivative-schema-request.synthetic.json",
    "fixtures/valid/manifold-route-blueprint.synthetic.json",
    "fixtures/valid/manifold-route-design-response-expectation.synthetic.json",
    "fixtures/valid/manifold-route-design-review-request.synthetic.json",
    "fixtures/valid/private-rehearsal-approval-request.synthetic.json",
    "fixtures/valid/private-rehearsal-evidence-expectation.synthetic.json",
    "fixtures/valid/private-rehearsal-public-derivative-expectation.synthetic.json",
    "fixtures/valid/public-lab-artifact-intake-manifest.synthetic.json",
    "fixtures/valid/public-lab-artifact-intake-report.synthetic.json",
    "fixtures/valid/public-lab-artifact-drift-review.synthetic.json",
    "fixtures/valid/sidecar-validation-scorecard.synthetic.json",
    "fixtures/damaged/configured-peer-rehearsal-plan-endpoint-command.damaged.json",
    "fixtures/damaged/hostess-boundary-descriptor-expectation-direct-sidecar.damaged.json",
    "fixtures/damaged/mesh-handoff-command-authority.damaged.json",
    "fixtures/damaged/integration-acceptance-scorecard-live-authority.damaged.json",
    "fixtures/damaged/manifold-adapter-proposal-sidecar-authority.damaged.json",
    "fixtures/damaged/manifold-adapter-contract-review-authority-command.damaged.json",
    "fixtures/damaged/manifold-contract-intake-request-live-route.damaged.json",
    "fixtures/damaged/manifold-handoff-package-live-accepted.damaged.json",
    "fixtures/damaged/manifold-response-handoff-package-sidecar-accepted.damaged.json",
    "fixtures/damaged/manifold-response-implementation-preflight-sidecar-implementation.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-handoff-package-sidecar-accepted.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-implementation-preflight-sidecar-implementation.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-response-expectation-sidecar-response.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-expectation-sidecar-response.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-handoff-package-sidecar-accepted.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-implementation-preflight-sidecar-implementation.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-operator-decision-record-expectation-sidecar-record.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-operator-decision-request-sidecar-decision.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-submission-envelope-expectation-sidecar-submission.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-submission-intake-response-handoff-package-sidecar-accepted.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-submission-intake-response-expectation-sidecar-response.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight-sidecar-implementation.damaged.json",
    "fixtures/damaged/manifold-public-derivative-schema-request-sidecar-owned.damaged.json",
    "fixtures/damaged/manifold-route-blueprint-sidecar-route.damaged.json",
    "fixtures/damaged/manifold-route-design-response-expectation-sidecar-response.damaged.json",
    "fixtures/damaged/manifold-route-design-review-request-sidecar-authority.damaged.json",
    "fixtures/damaged/no-network-agent-run-network-command.damaged.json",
    "fixtures/damaged/no-network-agent-recipe-network-adb.damaged.json",
    "fixtures/damaged/no-network-agent-recipe-review-runtime-authority.damaged.json",
    "fixtures/damaged/no-network-prototype-handoff-review-sidecar-authority.damaged.json",
    "fixtures/damaged/private-rehearsal-approval-request-endpoint-command.damaged.json",
    "fixtures/damaged/private-rehearsal-evidence-expectation-leaky-live.damaged.json",
    "fixtures/damaged/private-rehearsal-public-derivative-expectation-leaky-live.damaged.json",
    "fixtures/damaged/public-lab-artifact-drift-review-raw-copy.damaged.json",
    "fixtures/damaged/public-lab-artifact-intake-endpoint-leak.damaged.json",
    "tools/import_public_lab_status.py",
    "tools/evaluate_integration_acceptance.py",
    "tools/package_manifold_handoff.py",
    "tools/package_manifold_public_derivative_schema_handoff.py",
    "tools/package_manifold_response_handoff.py",
    "tools/plan_configured_peer_rehearsal.py",
    "tools/prepare_hostess_boundary_descriptor_expectation.py",
    "tools/prepare_manifold_contract_intake.py",
    "tools/prepare_manifold_response_implementation_preflight.py",
    "tools/prepare_manifold_public_derivative_schema_implementation_preflight.py",
    "tools/prepare_manifold_public_derivative_schema_response_expectation.py",
    "tools/prepare_manifold_public_derivative_schema_request.py",
    "tools/prepare_manifold_public_derivative_schema_slice_response_expectation.py",
    "tools/package_manifold_public_derivative_schema_slice_response_handoff.py",
    "tools/prepare_manifold_public_derivative_schema_slice_response_implementation_preflight.py",
    "tools/prepare_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.py",
    "tools/prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.py",
    "tools/prepare_manifold_public_derivative_schema_slice_response_submission_envelope_expectation.py",
    "tools/package_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff.py",
    "tools/prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.py",
    "tools/prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.py",
    "tools/prepare_manifold_route_blueprint.py",
    "tools/prepare_manifold_route_design_response_expectation.py",
    "tools/prepare_manifold_route_design_review.py",
    "tools/prepare_private_rehearsal_approval.py",
    "tools/prepare_private_rehearsal_evidence_expectation.py",
    "tools/prepare_private_rehearsal_public_derivative_expectation.py",
    "tools/review_public_lab_artifact_drift.py",
    "tools/review_manifold_adapter_contract.py",
    "tools/run_no_network_agent.py",
    "tools/review_no_network_prototype_handoff.py",
    "tools/review_no_network_recipe.py",
    "tools/validate_repo.py",
    "tests/test_evaluate_integration_acceptance.py",
    "tests/test_import_public_lab_status.py",
    "tests/test_package_manifold_handoff.py",
    "tests/test_package_manifold_public_derivative_schema_handoff.py",
    "tests/test_package_manifold_public_derivative_schema_slice_response_handoff.py",
    "tests/test_package_manifold_response_handoff.py",
    "tests/test_plan_configured_peer_rehearsal.py",
    "tests/test_prepare_hostess_boundary_descriptor_expectation.py",
    "tests/test_prepare_manifold_contract_intake.py",
    "tests/test_prepare_manifold_response_implementation_preflight.py",
    "tests/test_prepare_manifold_public_derivative_schema_implementation_preflight.py",
    "tests/test_prepare_manifold_public_derivative_schema_response_expectation.py",
    "tests/test_prepare_manifold_public_derivative_schema_request.py",
    "tests/test_prepare_manifold_public_derivative_schema_slice_response_expectation.py",
    "tests/test_prepare_manifold_public_derivative_schema_slice_response_implementation_preflight.py",
    "tests/test_prepare_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.py",
    "tests/test_prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.py",
    "tests/test_prepare_manifold_public_derivative_schema_slice_response_submission_envelope_expectation.py",
    "tests/test_package_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff.py",
    "tests/test_prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.py",
    "tests/test_prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.py",
    "tests/test_prepare_manifold_route_blueprint.py",
    "tests/test_prepare_manifold_route_design_response_expectation.py",
    "tests/test_prepare_manifold_route_design_review.py",
    "tests/test_prepare_private_rehearsal_approval.py",
    "tests/test_prepare_private_rehearsal_evidence_expectation.py",
    "tests/test_prepare_private_rehearsal_public_derivative_expectation.py",
    "tests/test_review_public_lab_artifact_drift.py",
    "tests/test_review_manifold_adapter_contract.py",
    "tests/test_run_no_network_agent.py",
    "tests/test_review_no_network_prototype_handoff.py",
    "tests/test_review_no_network_recipe.py",
    "tests/test_validate_repo.py",
]

FORBIDDEN_KEY_FRAGMENTS = {
    "adb_target",
    "adb_serial",
    "adb_pairing",
    "pairing_code",
    "shell_command",
    "command_payload",
    "install_apk",
    "launch_package",
    "package_name",
    "wifi_adb_endpoint",
    "headset_serial",
    "private_endpoint",
    "token",
    "password",
    "secret",
    "screenshot",
    "logcat",
}

FORBIDDEN_VALUES = {
    "execute_shell",
    "android_shell_authority_allowed",
    "cross_headset_adb_authority_allowed",
    "manifold_authority_allowed",
    "accepted_command",
    "created_by_sidecar",
}

STABLE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]*[a-z0-9]$")
IPV4_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


@dataclass
class ValidationResult:
    path: Path
    ok: bool
    errors: list[str]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_json_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.json") if ".git" not in path.parts)


def walk_json(value: Any, path: str = "$") -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = [(path, value)]
    if isinstance(value, dict):
        for key, child in value.items():
            rows.extend(walk_json(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            rows.extend(walk_json(child, f"{path}[{index}]"))
    return rows


def check_no_forbidden_fields(document: Any) -> list[str]:
    errors: list[str] = []
    for path, value in walk_json(document):
        key = path.rsplit(".", 1)[-1].lower()
        for fragment in FORBIDDEN_KEY_FRAGMENTS:
            if fragment in key:
                errors.append(f"forbidden key fragment '{fragment}' at {path}")
        if isinstance(value, str):
            value_lower = value.lower()
            if value_lower in FORBIDDEN_VALUES:
                errors.append(f"forbidden value '{value}' at {path}")
            for match in IPV4_PATTERN.findall(value):
                if not match.startswith("127."):
                    errors.append(f"non-loopback IPv4 endpoint '{match}' at {path}")
    return errors


def check_stable_ids(document: Any) -> list[str]:
    errors: list[str] = []
    for path, value in walk_json(document):
        key = path.rsplit(".", 1)[-1]
        if key.endswith("_id") and isinstance(value, str):
            if not STABLE_ID_PATTERN.match(value):
                errors.append(f"unstable id '{value}' at {path}")
    return errors


def validate_schema_file(path: Path, document: Any) -> list[str]:
    errors: list[str] = []
    schema_id = document.get("$id") if isinstance(document, dict) else None
    if schema_id not in SCHEMA_IDS:
        errors.append(f"unknown schema $id: {schema_id!r}")
    else:
        expected = SCHEMA_IDS[schema_id].replace("/", "\\")
        normalized = str(path).replace("/", "\\")
        if not normalized.endswith(expected):
            errors.append(f"schema {schema_id} is not in expected file {SCHEMA_IDS[schema_id]}")
    return errors


def validate_fixture(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["fixture root must be an object"]

    schema = document.get("schema")
    if schema not in SCHEMA_IDS:
        errors.append(f"unknown fixture schema: {schema!r}")
        return errors

    errors.extend(check_no_forbidden_fields(document))
    errors.extend(check_stable_ids(document))

    if schema == "rusty.quest.sidecar.agent_profile.v1":
        errors.extend(validate_agent_profile(document))
    elif schema == "rusty.quest.sidecar.hostess_boundary_descriptor_expectation.v1":
        errors.extend(validate_hostess_boundary_descriptor_expectation(document))
    elif schema == "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1":
        errors.extend(validate_configured_peer_rehearsal_plan(document))
    elif schema == "rusty.quest.sidecar.integration_acceptance_scorecard.v1":
        errors.extend(validate_integration_acceptance_scorecard(document))
    elif schema == "rusty.quest.sidecar.no_network_agent_run.v1":
        errors.extend(validate_no_network_agent_run(document))
    elif schema == "rusty.quest.sidecar.no_network_agent_recipe.v1":
        errors.extend(validate_no_network_agent_recipe(document))
    elif schema == "rusty.quest.sidecar.no_network_agent_recipe_review.v1":
        errors.extend(validate_no_network_agent_recipe_review(document))
    elif schema == "rusty.quest.sidecar.no_network_prototype_handoff_review.v1":
        errors.extend(validate_no_network_prototype_handoff_review(document))
    elif schema == "rusty.quest.sidecar.observation.v1":
        errors.extend(validate_observation(document))
    elif schema == "rusty.quest.sidecar.mesh_handoff.v1":
        errors.extend(validate_handoff(document))
    elif schema == "rusty.quest.sidecar.manifold_adapter_contract_review.v1":
        errors.extend(validate_manifold_adapter_contract_review(document))
    elif schema == "rusty.quest.sidecar.manifold_adapter_proposal.v1":
        errors.extend(validate_manifold_adapter_proposal(document))
    elif schema == "rusty.quest.sidecar.manifold_contract_intake_request.v1":
        errors.extend(validate_manifold_contract_intake_request(document))
    elif schema == "rusty.quest.sidecar.manifold_handoff_package.v1":
        errors.extend(validate_manifold_handoff_package(document))
    elif schema == "rusty.quest.sidecar.manifold_response_implementation_preflight.v1":
        errors.extend(validate_manifold_response_implementation_preflight(document))
    elif schema == "rusty.quest.sidecar.manifold_response_handoff_package.v1":
        errors.extend(validate_manifold_response_handoff_package(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_handoff_package.v1":
        errors.extend(validate_manifold_public_derivative_schema_handoff_package(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_implementation_preflight.v1":
        errors.extend(validate_manifold_public_derivative_schema_implementation_preflight(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_response_expectation.v1":
        errors.extend(validate_manifold_public_derivative_schema_response_expectation(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_expectation.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_expectation(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_handoff_package.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_handoff_package(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_implementation_preflight.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_implementation_preflight(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_operator_decision_request(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_envelope_expectation.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_submission_envelope_expectation(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_handoff_package.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff_package(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.v1":
        errors.extend(validate_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight(document))
    elif schema == "rusty.quest.sidecar.manifold_public_derivative_schema_request.v1":
        errors.extend(validate_manifold_public_derivative_schema_request(document))
    elif schema == "rusty.quest.sidecar.manifold_route_blueprint.v1":
        errors.extend(validate_manifold_route_blueprint(document))
    elif schema == "rusty.quest.sidecar.manifold_route_design_response_expectation.v1":
        errors.extend(validate_manifold_route_design_response_expectation(document))
    elif schema == "rusty.quest.sidecar.manifold_route_design_review_request.v1":
        errors.extend(validate_manifold_route_design_review_request(document))
    elif schema == "rusty.quest.sidecar.private_rehearsal_approval_request.v1":
        errors.extend(validate_private_rehearsal_approval_request(document))
    elif schema == "rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1":
        errors.extend(validate_private_rehearsal_evidence_expectation(document))
    elif schema == "rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1":
        errors.extend(validate_private_rehearsal_public_derivative_expectation(document))
    elif schema == "rusty.quest.sidecar.public_lab_artifact_drift_review.v1":
        errors.extend(validate_public_lab_artifact_drift_review(document))
    elif schema == "rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1":
        errors.extend(validate_public_lab_intake_manifest(document))
    elif schema == "rusty.quest.sidecar.public_lab_artifact_intake_report.v1":
        errors.extend(validate_public_lab_intake_report(document))
    elif schema == "rusty.quest.sidecar.validation_scorecard.v1":
        errors.extend(validate_scorecard(document))

    return errors


def validate_hostess_boundary_descriptor_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {"ready_for_future_hostess_boundary_descriptor", "manual_review", "blocked"}:
        errors.append("Hostess boundary descriptor expectation has invalid expectation_status")

    source = document.get("source_manifold_response_handoff_package", {})
    if source.get("path") != "fixtures/valid/manifold-response-handoff-package.synthetic.json":
        errors.append("Hostess boundary descriptor expectation must point at the response handoff package fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_response_handoff_package.v1":
        errors.append("Hostess boundary descriptor expectation source handoff schema is invalid")
    if source.get("package_status") != "response_handoff_package_ready":
        errors.append("Hostess boundary descriptor expectation source handoff must be ready")
    if source.get("next_gate") != "manifold_repo_response_slice_or_operator_decision":
        errors.append("Hostess boundary descriptor expectation source handoff next_gate is invalid")

    scope = document.get("expectation_scope", {})
    expected_scope = {
        "expectation_class": "hostess_boundary_descriptor_expectation",
        "source_mode": "synthetic_fixture",
        "target_descriptor_owner": "rusty.manifold",
        "future_consumer": "rusty.hostess",
        "manifold_repo_touch_status": "not_touched",
        "hostess_repo_touch_status": "not_touched",
        "hostess_route_status": "not_created",
        "manifold_accepted_state_status": "not_created",
        "operator_request_status": "not_recorded",
        "live_evidence_status": "not_included",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Hostess boundary descriptor expectation expectation_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "boundary_descriptor_owner": "rusty.manifold",
        "source_of_truth_owner": "rusty.manifold",
        "response_decision_owner": "rusty.manifold",
        "accepted_state_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "future_hostess_route_owner": "rusty.hostess",
        "future_hostess_route_enablement_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Hostess boundary descriptor expectation authority.{key} must be {expected}")

    descriptor = document.get("expected_hostess_boundary_descriptor", {})
    expected_descriptor = {
        "descriptor_status": "not_created",
        "descriptor_kind": "hostess_operator_recovery_boundary",
        "input_source_policy": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allows_endpoint_values": False,
        "allows_commands": False,
        "allows_adb": False,
        "allows_high_rate_payloads": False,
        "safe_to_create_hostess_route": False,
    }
    for key, expected in expected_descriptor.items():
        if descriptor.get(key) != expected:
            errors.append(f"Hostess boundary descriptor expectation descriptor {key} must be {expected}")

    required_fields = {
        "manifold_decision_id",
        "accepted_state_id",
        "source_handoff_package_id",
        "decision_status",
        "operator_request_status",
        "rejection_terms",
        "audit_record_id",
        "privacy_boundary",
    }
    missing_fields = sorted(required_fields - set(descriptor.get("required_descriptor_fields", [])))
    if missing_fields:
        errors.append(f"Hostess boundary descriptor expectation missing descriptor fields: {missing_fields}")

    required_slots = {
        "slot.hostess_boundary_descriptor_schema",
        "slot.hostess_rejects_sidecar_direct_input",
        "slot.hostess_requires_manifold_accepted_state",
        "slot.hostess_requires_operator_request_for_recovery",
        "slot.hostess_privacy_redaction_check",
        "slot.hostess_no_device_action_fixture",
    }
    missing_slots = sorted(required_slots - set(descriptor.get("required_hostess_validation_slots", [])))
    if missing_slots:
        errors.append(f"Hostess boundary descriptor expectation missing validation slots: {missing_slots}")

    allowed_actions = set(descriptor.get("allowed_action_classes", []))
    if allowed_actions != {"read_only_status_view_descriptor", "operator_recovery_request_descriptor"}:
        errors.append("Hostess boundary descriptor expectation allowed_action_classes are invalid")

    required_disallowed = {
        "sidecar_peer_message_direct",
        "endpoint_values",
        "commands",
        "adb",
        "high_rate_payloads",
        "raw_logs",
        "visual_captures",
        "pairing_material",
    }
    missing_disallowed = sorted(required_disallowed - set(descriptor.get("disallowed_input_classes", [])))
    if missing_disallowed:
        errors.append(f"Hostess boundary descriptor expectation missing disallowed input classes: {missing_disallowed}")

    gate = document.get("manifold_acceptance_gate", {})
    expected_gate = {
        "handoff_acceptance_status": "not_accepted",
        "response_decision_status": "not_decided",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "required_response_decision": "accepted_for_manifold_slice",
        "hostess_boundary_descriptor_status": "not_created",
        "hostess_route_status": "not_created",
        "hostess_enablement_status": "not_enabled",
        "gate_result": "hostess_boundary_descriptor_not_ready_for_route_creation",
    }
    for key, expected in expected_gate.items():
        if gate.get(key) != expected:
            errors.append(f"Hostess boundary descriptor expectation manifold_acceptance_gate.{key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Hostess boundary descriptor expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_hostess_boundary_descriptor_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Hostess boundary descriptor expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Hostess boundary descriptor expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_response_acceptance_before_hostess_descriptor_creation":
        errors.append("Hostess boundary descriptor expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Hostess boundary descriptor expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Hostess boundary descriptor expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Hostess boundary descriptor expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Hostess boundary descriptor expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Hostess boundary descriptor expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Hostess boundary descriptor expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Hostess boundary descriptor expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Hostess boundary descriptor expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Hostess boundary descriptor expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_future_hostess_boundary_descriptor" and fail_count != 0:
        errors.append("ready Hostess boundary descriptor expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Hostess boundary descriptor expectation must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_response_slice_or_operator_decision":
        errors.append("Hostess boundary descriptor expectation next_gate is invalid")
    return errors


def validate_agent_profile(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    profile = document.get("implementation_profile", {})
    authority = document.get("authority", {})
    if profile.get("runtime") != "termux":
        errors.append("agent profile must declare the initial runtime as termux")
    allowed_roles = set(authority.get("allowed_roles", []))
    forbidden_allowed = {
        "manifold_authority",
        "android_shell_authority",
        "recovery_authority",
        "cross_headset_adb_authority",
        "install_launch_authority",
    }
    overlap = sorted(allowed_roles & forbidden_allowed)
    if overlap:
        errors.append(f"forbidden roles appear in allowed_roles: {overlap}")
    if authority.get("mutation_policy") != "requests_only_through_manifold_handoff":
        errors.append("agent profile must keep mutation requests behind Manifold handoff")
    return errors


def validate_observation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    advisory = document.get("advisory", {})
    redaction = document.get("redaction", {})
    if advisory.get("truth_level") != "advisory_cached_view":
        errors.append("observation truth_level must be advisory_cached_view")
    if redaction.get("contains_endpoint_values") is not False:
        errors.append("observation must not contain endpoint values")
    if document.get("status") not in {"available", "degraded", "unavailable", "unknown"}:
        errors.append("observation status is not recognized")
    return errors


def validate_handoff(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    approval = document.get("approval", {})
    audit = document.get("audit", {})
    required_by = set(approval.get("required_by", []))
    if "rusty.manifold" not in required_by:
        errors.append("handoff approval must require rusty.manifold")
    if approval.get("status") == "approved":
        errors.append("sidecar handoff fixture must not pre-approve mutation")
    if audit.get("source_of_truth") != "rusty.manifold.audit":
        errors.append("handoff audit source_of_truth must be rusty.manifold.audit")
    for request in document.get("requests", []):
        if request.get("authority_required") != "rusty.manifold":
            errors.append(f"request {request.get('request_id', '<unknown>')} must require rusty.manifold")
        if request.get("status") not in {"proposed", "rejected", "accepted_by_manifold"}:
            errors.append(f"request {request.get('request_id', '<unknown>')} has invalid status")
    return errors


def validate_scorecard(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    summary = document.get("summary", {})
    checks = document.get("checks", [])
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if summary.get("status") not in {"contract_ready", "manual_review", "blocked"}:
        errors.append("scorecard summary status is not recognized")
    if "pass" not in statuses:
        errors.append("scorecard must include at least one passing check")
    if not document.get("next_gate"):
        errors.append("scorecard next_gate is required")
    return errors


def validate_integration_acceptance_scorecard(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("overall_status") not in {"acceptance_ready", "manual_review", "acceptance_blocked"}:
        errors.append("integration acceptance scorecard has invalid overall_status")
    checks = document.get("checks", [])
    if not checks:
        errors.append("integration acceptance scorecard must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("integration acceptance scorecard contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("integration acceptance scorecard check_count does not match checks")
    if document.get("overall_status") == "acceptance_ready" and summary.get("fail_count", 0) != 0:
        errors.append("acceptance_ready scorecard must not have failed checks")
    if summary.get("damaged_expected_failure_count", 0) < 3:
        errors.append("integration acceptance scorecard must cover at least three damaged expected failures")
    return errors


def validate_public_lab_intake_manifest(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    refs = document.get("artifact_refs", [])
    if not refs:
        errors.append("public lab intake manifest must declare artifact_refs")
    for ref in refs:
        path = ref.get("path", "")
        if not path or path.startswith("/") or "\\" in path:
            errors.append(f"artifact path must be relative slash form: {path!r}")
        if ".." in Path(path).parts:
            errors.append(f"artifact path must not escape source root: {path!r}")
        if not ref.get("expected_schema", "").startswith("quest-termux-lab."):
            errors.append(f"artifact {ref.get('artifact_id', '<unknown>')} must expect quest-termux-lab schema")
        if ref.get("expected_status_class") not in {"ready", "blocked", "manual_review"}:
            errors.append(f"artifact {ref.get('artifact_id', '<unknown>')} has invalid expected_status_class")
    policy = document.get("extraction_policy", {})
    if policy.get("copy_raw_artifact") is not False:
        errors.append("public lab intake must not copy raw artifacts")
    if policy.get("execute_source_validation") is not False:
        errors.append("public lab intake must not execute source validation")
    if policy.get("contains_endpoint_values") is not False:
        errors.append("public lab intake manifest must declare no endpoint values")
    return errors


def validate_no_network_agent_recipe(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    profile = document.get("implementation_profile", {})
    authority = document.get("authority", {})
    execution = document.get("execution", {})
    if profile.get("runtime") != "termux":
        errors.append("no-network recipe runtime must be termux")
    if authority.get("role") != "sidecar_observer":
        errors.append("no-network recipe role must be sidecar_observer")
    if authority.get("acceptance_owner") != "rusty.manifold":
        errors.append("no-network recipe acceptance_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("no-network recipe audit_owner must be rusty.manifold.audit")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("no-network recipe proposal_status must be not_accepted")
    if execution.get("network_policy") != "no_inbound_listener":
        errors.append("no-network recipe network_policy must be no_inbound_listener")
    if execution.get("outbound_transport_policy") != "disabled_for_recipe":
        errors.append("no-network recipe outbound transport must be disabled_for_recipe")
    if execution.get("adb_policy") != "no_adb":
        errors.append("no-network recipe adb_policy must be no_adb")
    if execution.get("command_policy") != "no_commands":
        errors.append("no-network recipe command_policy must be no_commands")
    emissions = document.get("emissions", [])
    if not emissions:
        errors.append("no-network recipe must declare at least one emission")
    for emission in emissions:
        if emission.get("schema") != "rusty.quest.sidecar.observation.v1":
            errors.append("no-network recipe emissions must use sidecar observation schema")
        if emission.get("rate_class") != "low_rate":
            errors.append("no-network recipe emissions must remain low_rate")
    return errors


def validate_no_network_agent_run(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("prototype_status") not in {"prototype_complete", "manual_review", "blocked"}:
        errors.append("no-network agent run has invalid prototype_status")

    source_recipe = document.get("source_recipe", {})
    if source_recipe.get("path") != "fixtures/valid/no-network-agent-recipe.synthetic.json":
        errors.append("no-network agent run must point at the synthetic no-network recipe fixture")
    if source_recipe.get("recipe_schema") != "rusty.quest.sidecar.no_network_agent_recipe.v1":
        errors.append("no-network agent run source recipe schema is invalid")

    source_review = document.get("source_review", {})
    if source_review.get("path") != "fixtures/valid/no-network-agent-recipe-review.synthetic.json":
        errors.append("no-network agent run must point at the synthetic no-network recipe review fixture")
    if source_review.get("review_schema") != "rusty.quest.sidecar.no_network_agent_recipe_review.v1":
        errors.append("no-network agent run source review schema is invalid")
    if source_review.get("review_status") != "ready_for_no_network_prototype":
        errors.append("no-network agent run requires a ready recipe review")

    runtime = document.get("runtime", {})
    if runtime.get("implementation_profile") != "termux_python_standard_library":
        errors.append("no-network agent run implementation profile must be termux_python_standard_library")
    if runtime.get("execution_mode") != "local_static_file_generation":
        errors.append("no-network agent run execution_mode must be local_static_file_generation")
    if runtime.get("network_policy") != "no_inbound_listener":
        errors.append("no-network agent run network_policy must be no_inbound_listener")
    if runtime.get("outbound_transport_policy") != "disabled":
        errors.append("no-network agent run outbound transport must be disabled")
    if runtime.get("adb_policy") != "no_adb":
        errors.append("no-network agent run adb_policy must be no_adb")
    if runtime.get("command_policy") != "no_commands":
        errors.append("no-network agent run command_policy must be no_commands")

    authority = document.get("authority", {})
    if authority.get("role") != "sidecar_observer":
        errors.append("no-network agent run role must be sidecar_observer")
    if authority.get("mutation_policy") != "write_observation_file_only":
        errors.append("no-network agent run mutation_policy must be write_observation_file_only")
    if authority.get("acceptance_owner") != "rusty.manifold":
        errors.append("no-network agent run acceptance_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("no-network agent run audit_owner must be rusty.manifold.audit")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("no-network agent run proposal_status must be not_accepted")

    handoff = document.get("handoff_readiness", {})
    manifold = handoff.get("manifold_observation_intake", {})
    if manifold.get("status") != "candidate":
        errors.append("Manifold handoff readiness must remain candidate")
    if manifold.get("authority_owner") != "rusty.manifold":
        errors.append("Manifold handoff readiness authority_owner must be rusty.manifold")
    if manifold.get("audit_owner") != "rusty.manifold.audit":
        errors.append("Manifold handoff readiness audit_owner must be rusty.manifold.audit")
    if manifold.get("input_schema") != "rusty.quest.sidecar.observation.v1":
        errors.append("Manifold handoff readiness input_schema must be sidecar observation")
    if manifold.get("input_role") != "proposal_input":
        errors.append("Manifold handoff readiness input_role must be proposal_input")

    hostess = handoff.get("hostess_operator_recovery", {})
    if hostess.get("status") != "future_lane_not_requested":
        errors.append("Hostess handoff readiness must remain future_lane_not_requested")
    if hostess.get("device_action_authority") != "not_in_sidecar":
        errors.append("Hostess handoff readiness device action authority must not be in sidecar")
    if hostess.get("input_role") != "manifold_accepted_state_or_operator_request":
        errors.append("Hostess handoff readiness input_role must require Manifold state or operator request")

    outputs = document.get("outputs", {})
    if outputs.get("observation_path") != "fixtures/valid/no-network-agent-observation.synthetic.json":
        errors.append("no-network agent run observation_path must point at the generated observation fixture")
    if outputs.get("observation_schema") != "rusty.quest.sidecar.observation.v1":
        errors.append("no-network agent run observation_schema must be sidecar observation")
    if outputs.get("emission_rate_class") != "low_rate":
        errors.append("no-network agent run emission_rate_class must be low_rate")

    checks = document.get("checks", [])
    if not checks:
        errors.append("no-network agent run must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("no-network agent run contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("no-network agent run check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("no-network agent run fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("no-network agent run manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("no-network agent run pass_count does not match checks")
    if document.get("prototype_status") == "prototype_complete" and fail_count != 0:
        errors.append("complete no-network agent run must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text:
        errors.append("no-network agent run must preserve Manifold acceptance authority")
    if document.get("next_gate") != "no_network_prototype_handoff_review_before_configured_peer_rehearsal":
        errors.append("no-network agent run next_gate must require prototype handoff review before peer rehearsal")
    return errors


def validate_no_network_agent_recipe_review(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("review_status") not in {"ready_for_no_network_prototype", "manual_review", "blocked"}:
        errors.append("no-network recipe review has invalid review_status")

    source = document.get("source_recipe", {})
    if source.get("path") != "fixtures/valid/no-network-agent-recipe.synthetic.json":
        errors.append("no-network recipe review must point at the synthetic no-network recipe fixture")
    if source.get("recipe_schema") != "rusty.quest.sidecar.no_network_agent_recipe.v1":
        errors.append("no-network recipe review source schema is invalid")
    if source.get("profile_status") != "recipe_only":
        errors.append("no-network recipe review source must remain recipe_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("no-network recipe review must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("no-network recipe review contains invalid check status")

    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("no-network recipe review check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("no-network recipe review fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("no-network recipe review manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("no-network recipe review pass_count does not match checks")
    if document.get("review_status") == "ready_for_no_network_prototype" and fail_count != 0:
        errors.append("ready no-network recipe review must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text:
        errors.append("no-network recipe review must preserve Manifold acceptance authority")
    if document.get("next_gate") != "private_no_network_termux_agent_prototype_without_transport_or_adb":
        errors.append("no-network recipe review next_gate must remain the no-network prototype gate")
    return errors


def validate_no_network_prototype_handoff_review(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("review_status") not in {"handoff_review_ready", "manual_review", "blocked"}:
        errors.append("no-network prototype handoff review has invalid review_status")

    source_observation = document.get("source_observation", {})
    if source_observation.get("path") != "fixtures/valid/no-network-agent-observation.synthetic.json":
        errors.append("handoff review must point at the generated no-network observation fixture")
    if source_observation.get("schema") != "rusty.quest.sidecar.observation.v1":
        errors.append("handoff review source observation schema is invalid")
    if source_observation.get("truth_level") != "advisory_cached_view":
        errors.append("handoff review source observation must remain advisory_cached_view")

    source_run = document.get("source_run", {})
    if source_run.get("path") != "fixtures/valid/no-network-agent-run.synthetic.json":
        errors.append("handoff review must point at the generated no-network run fixture")
    if source_run.get("schema") != "rusty.quest.sidecar.no_network_agent_run.v1":
        errors.append("handoff review source run schema is invalid")
    if source_run.get("prototype_status") != "prototype_complete":
        errors.append("handoff review requires a complete no-network prototype run")

    integration_status = document.get("integration_status", {})
    integration_flags = [
        "manifold_repo_touched",
        "hostess_repo_touched",
        "live_device_used",
        "runtime_route_created",
        "hostess_route_created",
    ]
    for flag in integration_flags:
        if integration_status.get(flag) is not False:
            errors.append(f"handoff review integration_status.{flag} must be false")

    manifold = document.get("manifold_mapping", {})
    if manifold.get("status") != "candidate":
        errors.append("handoff review Manifold mapping must remain candidate")
    if manifold.get("authority_owner") != "rusty.manifold":
        errors.append("handoff review Manifold authority_owner must be rusty.manifold")
    if manifold.get("audit_owner") != "rusty.manifold.audit":
        errors.append("handoff review Manifold audit_owner must be rusty.manifold.audit")
    if manifold.get("source_schema") != "rusty.quest.sidecar.observation.v1":
        errors.append("handoff review Manifold source_schema must be sidecar observation")
    if manifold.get("source_role") != "proposal_input":
        errors.append("handoff review Manifold source_role must be proposal_input")
    audit_fields = manifold.get("proposed_audit_fields", {})
    if audit_fields.get("acceptance_status") != "not_implemented":
        errors.append("handoff review Manifold acceptance_status must be not_implemented")
    if audit_fields.get("accepted_state_owner") != "rusty.manifold":
        errors.append("handoff review Manifold accepted_state_owner must be rusty.manifold")

    required_manifold_rejections = {
        "stale_observation",
        "untrusted_sidecar",
        "redaction_incomplete",
        "forbidden_authority",
        "operator_approval_missing",
    }
    observed_manifold_rejections = set(manifold.get("rejection_terms", []))
    missing_manifold_rejections = sorted(required_manifold_rejections - observed_manifold_rejections)
    if missing_manifold_rejections:
        errors.append(f"handoff review missing Manifold rejection terms: {missing_manifold_rejections}")

    hostess = document.get("hostess_mapping", {})
    if hostess.get("status") != "future_lane_not_requested":
        errors.append("handoff review Hostess mapping must remain future_lane_not_requested")
    if hostess.get("role") != "operator_recovery_after_manifold_acceptance":
        errors.append("handoff review Hostess role must be operator_recovery_after_manifold_acceptance")
    if hostess.get("device_action_authority") != "not_in_sidecar":
        errors.append("handoff review Hostess device_action_authority must be not_in_sidecar")
    if hostess.get("source_schema") != "rusty.quest.sidecar.no_network_agent_run.v1":
        errors.append("handoff review Hostess source_schema must be no-network run")
    if hostess.get("input_role") != "manifold_accepted_state_or_operator_request":
        errors.append("handoff review Hostess input_role must require Manifold state or operator request")
    descriptor = hostess.get("request_descriptor_fields", {})
    if descriptor.get("required_authority") != "rusty.manifold_or_operator":
        errors.append("handoff review Hostess request required_authority must be rusty.manifold_or_operator")
    if descriptor.get("implementation_status") != "not_implemented":
        errors.append("handoff review Hostess implementation_status must be not_implemented")

    required_hostess_rejections = {
        "manifold_acceptance_missing",
        "operator_request_missing",
        "sidecar_device_action_forbidden",
    }
    observed_hostess_rejections = set(hostess.get("rejection_terms", []))
    missing_hostess_rejections = sorted(required_hostess_rejections - observed_hostess_rejections)
    if missing_hostess_rejections:
        errors.append(f"handoff review missing Hostess rejection terms: {missing_hostess_rejections}")

    checks = document.get("checks", [])
    if not checks:
        errors.append("handoff review must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("handoff review contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("handoff review check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("handoff review fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("handoff review manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("handoff review pass_count does not match checks")
    if document.get("review_status") == "handoff_review_ready" and fail_count != 0:
        errors.append("ready handoff review must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("handoff review must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "private_configured_peer_rehearsal_requires_operator_approval":
        errors.append("handoff review next_gate must require operator approval before configured peer rehearsal")
    return errors


def validate_configured_peer_rehearsal_plan(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("plan_status") not in {"operator_approval_required", "manual_review", "blocked"}:
        errors.append("configured peer rehearsal plan has invalid plan_status")

    source = document.get("source_handoff_review", {})
    if source.get("path") != "fixtures/valid/no-network-prototype-handoff-review.synthetic.json":
        errors.append("configured peer rehearsal plan must point at the synthetic handoff review fixture")
    if source.get("schema") != "rusty.quest.sidecar.no_network_prototype_handoff_review.v1":
        errors.append("configured peer rehearsal source schema is invalid")
    if source.get("review_status") != "handoff_review_ready":
        errors.append("configured peer rehearsal requires a ready handoff review")
    if source.get("next_gate") != "private_configured_peer_rehearsal_requires_operator_approval":
        errors.append("configured peer rehearsal source next_gate must require operator approval")

    scope = document.get("rehearsal_scope", {})
    if scope.get("scope_class") != "configured_peer_status_rehearsal":
        errors.append("configured peer rehearsal scope_class must be configured_peer_status_rehearsal")
    if scope.get("source_mode") != "synthetic_fixture":
        errors.append("configured peer rehearsal source_mode must remain synthetic_fixture")
    if scope.get("live_exchange_status") != "not_started":
        errors.append("configured peer rehearsal must not mark live exchange as started")
    if scope.get("status_payload_class") != "low_rate_advisory_status":
        errors.append("configured peer rehearsal status_payload_class must be low_rate_advisory_status")
    if scope.get("operator_approval_required_before_route_start") is not True:
        errors.append("configured peer rehearsal must require operator approval before route start")

    authority = document.get("authority", {})
    if authority.get("sidecar_role") != "observer_proposer":
        errors.append("configured peer rehearsal sidecar_role must be observer_proposer")
    if authority.get("acceptance_owner") != "rusty.manifold":
        errors.append("configured peer rehearsal acceptance_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("configured peer rehearsal audit_owner must be rusty.manifold.audit")
    if authority.get("operator_approval_required") is not True:
        errors.append("configured peer rehearsal must require operator approval")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("configured peer rehearsal proposal_status must be not_accepted")
    if authority.get("sidecar_device_action_authority") != "forbidden":
        errors.append("configured peer rehearsal sidecar_device_action_authority must be forbidden")
    if authority.get("sidecar_command_authority") != "forbidden":
        errors.append("configured peer rehearsal sidecar_command_authority must be forbidden")

    peers = document.get("peer_set", [])
    if len(peers) < 2:
        errors.append("configured peer rehearsal must declare at least two synthetic peers")
    for peer in peers:
        peer_id = peer.get("peer_id", "<unknown>")
        if peer.get("configured_material_status") != "private_evidence_required_not_in_fixture":
            errors.append(f"peer {peer_id} configured material must remain private evidence not in fixture")
        if peer.get("contains_endpoint_values") is not False:
            errors.append(f"peer {peer_id} must not contain endpoint values")
        if peer.get("status_payload_class") != "low_rate_advisory_status":
            errors.append(f"peer {peer_id} status_payload_class must be low_rate_advisory_status")

    transport = document.get("transport_policy", {})
    if transport.get("route_policy") != "operator_approval_before_transport":
        errors.append("configured peer rehearsal route_policy must require operator approval before transport")
    if transport.get("status_payload_only") is not True:
        errors.append("configured peer rehearsal must remain status-payload-only")
    if transport.get("commands_allowed") is not False:
        errors.append("configured peer rehearsal must not allow commands")
    if transport.get("adb_allowed") is not False:
        errors.append("configured peer rehearsal must not allow ADB")
    if transport.get("remote_desktop_allowed") is not False:
        errors.append("configured peer rehearsal must not allow remote desktop")
    if transport.get("file_transfer_allowed") is not False:
        errors.append("configured peer rehearsal must not allow file transfer")
    if transport.get("fixture_contains_endpoint_values") is not False:
        errors.append("configured peer rehearsal fixture must not contain endpoint values")
    if transport.get("network_binding_created") is not False:
        errors.append("configured peer rehearsal must not create a network binding")
    if transport.get("route_started") is not False:
        errors.append("configured peer rehearsal route_started must be false")
    if transport.get("cleanup_evidence_required") is not True:
        errors.append("configured peer rehearsal must require cleanup evidence for private runs")

    manifold = document.get("manifold_readiness", {})
    if manifold.get("status") != "candidate":
        errors.append("configured peer rehearsal Manifold readiness must remain candidate")
    if manifold.get("authority_owner") != "rusty.manifold":
        errors.append("configured peer rehearsal Manifold authority_owner must be rusty.manifold")
    if manifold.get("audit_owner") != "rusty.manifold.audit":
        errors.append("configured peer rehearsal Manifold audit_owner must be rusty.manifold.audit")
    if manifold.get("source_role") != "proposal_input":
        errors.append("configured peer rehearsal Manifold source_role must be proposal_input")
    if manifold.get("acceptance_status") != "not_implemented":
        errors.append("configured peer rehearsal Manifold acceptance_status must be not_implemented")
    if manifold.get("accepted_state_owner") != "rusty.manifold":
        errors.append("configured peer rehearsal accepted_state_owner must be rusty.manifold")

    required_manifold_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "redaction_incomplete",
    }
    observed_manifold_rejections = set(manifold.get("rejection_terms", []))
    missing_manifold_rejections = sorted(required_manifold_rejections - observed_manifold_rejections)
    if missing_manifold_rejections:
        errors.append(f"configured peer rehearsal missing Manifold rejection terms: {missing_manifold_rejections}")

    hostess = document.get("hostess_readiness", {})
    if hostess.get("status") != "future_lane_not_requested":
        errors.append("configured peer rehearsal Hostess readiness must remain future_lane_not_requested")
    if hostess.get("role") != "operator_recovery_after_manifold_acceptance":
        errors.append("configured peer rehearsal Hostess role must be operator_recovery_after_manifold_acceptance")
    if hostess.get("device_action_authority") != "not_in_sidecar":
        errors.append("configured peer rehearsal Hostess device_action_authority must be not_in_sidecar")
    if hostess.get("input_role") != "manifold_accepted_state_or_operator_request":
        errors.append("configured peer rehearsal Hostess input_role must require Manifold state or operator request")
    if hostess.get("route_status") != "not_implemented":
        errors.append("configured peer rehearsal Hostess route_status must be not_implemented")
    descriptor = hostess.get("request_descriptor_fields", {})
    if descriptor.get("required_authority") != "rusty.manifold_or_operator":
        errors.append("configured peer rehearsal Hostess request required_authority must be rusty.manifold_or_operator")
    if descriptor.get("implementation_status") != "not_implemented":
        errors.append("configured peer rehearsal Hostess implementation_status must be not_implemented")

    required_hostess_rejections = {
        "manifold_acceptance_missing",
        "operator_request_missing",
        "sidecar_device_action_forbidden",
    }
    observed_hostess_rejections = set(hostess.get("rejection_terms", []))
    missing_hostess_rejections = sorted(required_hostess_rejections - observed_hostess_rejections)
    if missing_hostess_rejections:
        errors.append(f"configured peer rehearsal missing Hostess rejection terms: {missing_hostess_rejections}")

    evidence = document.get("evidence_policy", {})
    if evidence.get("contains_endpoint_values") is not False:
        errors.append("configured peer rehearsal evidence must not contain endpoint values")
    if evidence.get("contains_pairing_material") is not False:
        errors.append("configured peer rehearsal evidence must not contain pairing material")
    if evidence.get("contains_commands") is not False:
        errors.append("configured peer rehearsal evidence must not contain commands")
    if evidence.get("contains_raw_logs") is not False:
        errors.append("configured peer rehearsal evidence must not contain raw logs")
    if evidence.get("contains_visual_captures") is not False:
        errors.append("configured peer rehearsal evidence must not contain visual captures")
    if evidence.get("private_evidence_required_before_live_run") is not True:
        errors.append("configured peer rehearsal must require private evidence before live run")
    if evidence.get("sanitized_derivative_required") is not True:
        errors.append("configured peer rehearsal must require sanitized derivatives")
    if evidence.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("configured peer rehearsal public_fixture_policy must be synthetic_descriptor_only")

    steps = document.get("steps", [])
    if not steps:
        errors.append("configured peer rehearsal must declare planned steps")
    for step in steps:
        if step.get("status") != "planned":
            errors.append(f"step {step.get('step_id', '<unknown>')} must remain planned")

    checks = document.get("checks", [])
    if not checks:
        errors.append("configured peer rehearsal must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("configured peer rehearsal contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("configured peer rehearsal check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("configured peer rehearsal fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("configured peer rehearsal manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("configured peer rehearsal pass_count does not match checks")
    if document.get("plan_status") == "operator_approval_required" and fail_count != 0:
        errors.append("operator-approval-required peer rehearsal plan must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("configured peer rehearsal must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract":
        errors.append("configured peer rehearsal next_gate must require private evidence or Manifold adapter contract")
    return errors


def validate_manifold_adapter_contract_review(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("review_status") not in {"contract_ready", "manual_review", "blocked"}:
        errors.append("Manifold adapter contract review has invalid review_status")

    source = document.get("source_peer_rehearsal_plan", {})
    if source.get("path") != "fixtures/valid/configured-peer-rehearsal-plan.synthetic.json":
        errors.append("Manifold adapter contract review must point at the configured peer rehearsal plan fixture")
    if source.get("schema") != "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1":
        errors.append("Manifold adapter contract review source schema is invalid")
    if source.get("plan_status") != "operator_approval_required":
        errors.append("Manifold adapter contract review requires an operator-approval-gated peer plan")
    if source.get("next_gate") != "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract":
        errors.append("Manifold adapter contract review source next_gate is invalid")

    integration = document.get("integration_status", {})
    integration_flags = [
        "manifold_repo_touched",
        "hostess_repo_touched",
        "live_device_used",
        "runtime_route_created",
        "accepted_manifold_state_created",
        "hostess_route_created",
    ]
    for flag in integration_flags:
        if integration.get(flag) is not False:
            errors.append(f"Manifold adapter contract review integration_status.{flag} must be false")

    scope = document.get("contract_scope", {})
    if scope.get("contract_class") != "manifold_adapter_contract_review":
        errors.append("Manifold adapter contract review contract_class is invalid")
    if scope.get("source_mode") != "synthetic_fixture":
        errors.append("Manifold adapter contract review source_mode must remain synthetic_fixture")
    if scope.get("implementation_status") != "not_implemented":
        errors.append("Manifold adapter contract implementation_status must be not_implemented")
    if scope.get("route_status") != "not_created":
        errors.append("Manifold adapter contract route_status must be not_created")
    if scope.get("accepted_state_status") != "not_created":
        errors.append("Manifold adapter contract accepted_state_status must be not_created")
    if scope.get("payload_rate_class") != "low_rate":
        errors.append("Manifold adapter contract payload_rate_class must be low_rate")
    if scope.get("payload_authority") != "advisory_only":
        errors.append("Manifold adapter contract payload_authority must be advisory_only")

    authority = document.get("authority", {})
    if authority.get("runtime_authority_owner") != "rusty.manifold":
        errors.append("Manifold adapter contract runtime_authority_owner must be rusty.manifold")
    if authority.get("session_authority_owner") != "rusty.manifold":
        errors.append("Manifold adapter contract session_authority_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("Manifold adapter contract audit_owner must be rusty.manifold.audit")
    if authority.get("accepted_state_owner") != "rusty.manifold":
        errors.append("Manifold adapter contract accepted_state_owner must be rusty.manifold")
    if authority.get("sidecar_role") != "observer_proposer":
        errors.append("Manifold adapter contract sidecar_role must be observer_proposer")
    if authority.get("operator_role") != "approval_gate_for_private_evidence":
        errors.append("Manifold adapter contract operator_role must be approval_gate_for_private_evidence")
    if authority.get("hostess_role") != "future_operator_recovery_after_manifold_acceptance":
        errors.append("Manifold adapter contract hostess_role must remain future operator recovery")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("Manifold adapter contract proposal_status must be not_accepted")

    contract = document.get("proposed_manifold_contract", {})
    if contract.get("status") != "candidate":
        errors.append("Manifold adapter contract status must remain candidate")
    if contract.get("source_schema") != "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1":
        errors.append("Manifold adapter contract source_schema is invalid")
    if contract.get("source_path") != "fixtures/valid/configured-peer-rehearsal-plan.synthetic.json":
        errors.append("Manifold adapter contract source_path must point at the configured peer rehearsal plan")

    surfaces = contract.get("surfaces", [])
    if len(surfaces) < 3:
        errors.append("Manifold adapter contract must declare at least three proposed surfaces")
    for surface in surfaces:
        surface_id = surface.get("surface_id", "<unknown>")
        if surface.get("acceptance_owner") != "rusty.manifold":
            errors.append(f"contract surface {surface_id} acceptance_owner must be rusty.manifold")
        if surface.get("audit_owner") != "rusty.manifold.audit":
            errors.append(f"contract surface {surface_id} audit_owner must be rusty.manifold.audit")
        if surface.get("accepted_state_status") != "not_created":
            errors.append(f"contract surface {surface_id} accepted_state_status must be not_created")
        if surface.get("rate_class") not in {"low_rate", "control"}:
            errors.append(f"contract surface {surface_id} rate_class is invalid")

    lifecycle = set(contract.get("lifecycle_states", []))
    required_lifecycle = {
        "proposed",
        "operator_approval_required",
        "manifold_reviewing",
        "accepted_by_manifold",
        "rejected_by_manifold",
        "retired",
    }
    missing_lifecycle = sorted(required_lifecycle - lifecycle)
    if missing_lifecycle:
        errors.append(f"Manifold adapter contract missing lifecycle states: {missing_lifecycle}")

    forbidden_intake_fields = {"private_endpoint", "command_payload", "adb_target", "shell_command"}
    candidate_fields = set(contract.get("candidate_intake_fields", []))
    forbidden_candidate_fields = sorted(candidate_fields & forbidden_intake_fields)
    if forbidden_candidate_fields:
        errors.append(f"Manifold adapter contract candidate_intake_fields include forbidden fields: {forbidden_candidate_fields}")

    required_audit_fields = {
        "source_plan_id",
        "contract_id",
        "operator_approval_status",
        "acceptance_status",
        "rejection_reason",
        "accepted_state_owner",
        "audit_owner",
    }
    observed_audit_fields = set(contract.get("candidate_audit_fields", []))
    missing_audit_fields = sorted(required_audit_fields - observed_audit_fields)
    if missing_audit_fields:
        errors.append(f"Manifold adapter contract missing audit fields: {missing_audit_fields}")

    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "high_rate_payload_rejected",
        "unsupported_transport",
    }
    observed_rejections = set(contract.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold adapter contract missing rejection terms: {missing_rejections}")

    hostess = document.get("hostess_boundary", {})
    if hostess.get("status") != "future_lane_not_requested":
        errors.append("Manifold adapter contract Hostess boundary must remain future_lane_not_requested")
    if hostess.get("route_status") != "not_created":
        errors.append("Manifold adapter contract Hostess route_status must be not_created")
    if hostess.get("device_action_authority") != "not_in_sidecar":
        errors.append("Manifold adapter contract Hostess device_action_authority must be not_in_sidecar")
    if hostess.get("input_role") != "manifold_accepted_state_or_operator_request":
        errors.append("Manifold adapter contract Hostess input_role must require Manifold state or operator request")
    descriptor = hostess.get("request_descriptor_fields", {})
    if descriptor.get("required_authority") != "rusty.manifold_or_operator":
        errors.append("Manifold adapter contract Hostess request required_authority must be rusty.manifold_or_operator")
    if descriptor.get("implementation_status") != "not_implemented":
        errors.append("Manifold adapter contract Hostess implementation_status must be not_implemented")

    required_hostess_rejections = {
        "manifold_acceptance_missing",
        "operator_request_missing",
        "sidecar_device_action_forbidden",
    }
    observed_hostess_rejections = set(hostess.get("required_rejection_terms", []))
    missing_hostess_rejections = sorted(required_hostess_rejections - observed_hostess_rejections)
    if missing_hostess_rejections:
        errors.append(f"Manifold adapter contract missing Hostess rejection terms: {missing_hostess_rejections}")

    validation_slots = document.get("validation_slots", [])
    required_slots = {
        "slot.schema_and_fixture_validation",
        "slot.damaged_boundary_fixtures",
        "slot.future_manifold_contract_gate",
    }
    observed_slots = {slot.get("slot_id") for slot in validation_slots if isinstance(slot, dict)}
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold adapter contract missing validation slots: {missing_slots}")
    for slot in validation_slots:
        if not slot.get("owner"):
            errors.append(f"validation slot {slot.get('slot_id', '<unknown>')} must declare owner")
        if not slot.get("protected_risk"):
            errors.append(f"validation slot {slot.get('slot_id', '<unknown>')} must declare protected_risk")
        if not slot.get("command"):
            errors.append(f"validation slot {slot.get('slot_id', '<unknown>')} must declare command")

    rollback = document.get("rollback_policy", {})
    if rollback.get("rollback_owner") != "rusty.manifold":
        errors.append("Manifold adapter contract rollback_owner must be rusty.manifold")
    if rollback.get("sidecar_rollback_role") != "emit_retire_proposal_only":
        errors.append("Manifold adapter contract sidecar_rollback_role must be emit_retire_proposal_only")
    if rollback.get("accepted_state_removal_owner") != "rusty.manifold":
        errors.append("Manifold adapter contract accepted_state_removal_owner must be rusty.manifold")
    if rollback.get("audit_record_required") is not True:
        errors.append("Manifold adapter contract rollback must require audit records")
    if rollback.get("hostess_action_required") is not False:
        errors.append("Manifold adapter contract rollback must not require Hostess action")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold adapter contract review must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold adapter contract review contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold adapter contract review check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold adapter contract review fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold adapter contract review manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold adapter contract review pass_count does not match checks")
    if document.get("review_status") == "contract_ready" and fail_count != 0:
        errors.append("contract-ready Manifold adapter review must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold adapter contract review must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_owned_adapter_contract_or_operator_approved_private_rehearsal_evidence":
        errors.append("Manifold adapter contract review next_gate is invalid")
    return errors


def validate_manifold_handoff_package(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("package_status") not in {"handoff_package_ready", "manual_review", "blocked"}:
        errors.append("Manifold handoff package has invalid package_status")

    source = document.get("source_contract_review", {})
    if source.get("path") != "fixtures/valid/manifold-adapter-contract-review.synthetic.json":
        errors.append("Manifold handoff package must point at the synthetic contract review fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_adapter_contract_review.v1":
        errors.append("Manifold handoff package source schema is invalid")
    if source.get("review_status") != "contract_ready":
        errors.append("Manifold handoff package requires a contract_ready source review")
    if source.get("next_gate") != "manifold_owned_adapter_contract_or_operator_approved_private_rehearsal_evidence":
        errors.append("Manifold handoff package source next_gate is invalid")

    scope = document.get("package_scope", {})
    if scope.get("package_class") != "manifold_handoff_descriptor":
        errors.append("Manifold handoff package package_class must be manifold_handoff_descriptor")
    if scope.get("source_mode") != "synthetic_fixture":
        errors.append("Manifold handoff package source_mode must remain synthetic_fixture")
    if scope.get("implementation_status") != "not_implemented":
        errors.append("Manifold handoff package implementation_status must be not_implemented")
    if scope.get("route_status") != "not_created":
        errors.append("Manifold handoff package route_status must be not_created")
    if scope.get("accepted_state_status") != "not_created":
        errors.append("Manifold handoff package accepted_state_status must be not_created")
    if scope.get("live_evidence_status") != "not_included":
        errors.append("Manifold handoff package live_evidence_status must be not_included")

    authority = document.get("authority", {})
    if authority.get("package_owner") != "rusty.quest.sidecar_mesh":
        errors.append("Manifold handoff package owner must be rusty.quest.sidecar_mesh")
    if authority.get("handoff_acceptance_owner") != "rusty.manifold":
        errors.append("Manifold handoff package handoff_acceptance_owner must be rusty.manifold")
    if authority.get("runtime_authority_owner") != "rusty.manifold":
        errors.append("Manifold handoff package runtime_authority_owner must be rusty.manifold")
    if authority.get("session_authority_owner") != "rusty.manifold":
        errors.append("Manifold handoff package session_authority_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("Manifold handoff package audit_owner must be rusty.manifold.audit")
    if authority.get("accepted_state_owner") != "rusty.manifold":
        errors.append("Manifold handoff package accepted_state_owner must be rusty.manifold")
    if authority.get("sidecar_role") != "observer_proposer":
        errors.append("Manifold handoff package sidecar_role must be observer_proposer")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("Manifold handoff package proposal_status must be not_accepted")

    artifact_set = document.get("artifact_set", [])
    required_artifacts = {
        "artifact.public_lab_intake_report",
        "artifact.no_network_agent_recipe",
        "artifact.no_network_prototype_run",
        "artifact.no_network_handoff_review",
        "artifact.configured_peer_rehearsal_plan",
        "artifact.manifold_adapter_contract_review",
        "artifact.integration_acceptance_scorecard",
    }
    observed_artifacts = {artifact.get("artifact_id") for artifact in artifact_set if isinstance(artifact, dict)}
    missing_artifacts = sorted(required_artifacts - observed_artifacts)
    if missing_artifacts:
        errors.append(f"Manifold handoff package missing artifacts: {missing_artifacts}")
    for artifact in artifact_set:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        path = artifact.get("path", "")
        if not path or path.startswith("/") or "\\" in path:
            errors.append(f"artifact {artifact_id} path must be relative slash form")
        if ".." in Path(path).parts:
            errors.append(f"artifact {artifact_id} path must not escape repo")
        if artifact.get("required_for_handoff") is not True:
            errors.append(f"artifact {artifact_id} must be required_for_handoff")
        if not artifact.get("schema", "").startswith("rusty.quest.sidecar."):
            errors.append(f"artifact {artifact_id} schema must be a sidecar schema")

    handoff = document.get("proposed_manifold_handoff", {})
    if handoff.get("status") != "candidate":
        errors.append("Manifold handoff package proposed handoff status must be candidate")
    if handoff.get("target_repo") != "rusty.manifold":
        errors.append("Manifold handoff package target_repo must be rusty.manifold")
    if handoff.get("required_acceptance_owner") != "rusty.manifold":
        errors.append("Manifold handoff package required_acceptance_owner must be rusty.manifold")
    if handoff.get("required_audit_owner") != "rusty.manifold.audit":
        errors.append("Manifold handoff package required_audit_owner must be rusty.manifold.audit")
    if handoff.get("accepted_state_status") != "not_created":
        errors.append("Manifold handoff package proposed handoff accepted_state_status must be not_created")
    required_surfaces = {
        "sidecar_peer_status_source",
        "sidecar_peer_status_intake",
        "sidecar_peer_rehearsal_audit",
    }
    observed_surfaces = set(handoff.get("target_surfaces", []))
    missing_surfaces = sorted(required_surfaces - observed_surfaces)
    if missing_surfaces:
        errors.append(f"Manifold handoff package missing target surfaces: {missing_surfaces}")
    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
    }
    observed_rejections = set(handoff.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold handoff package missing rejection terms: {missing_rejections}")
    required_slots = {
        "slot.schema_and_fixture_validation",
        "slot.damaged_boundary_fixtures",
        "slot.future_manifold_contract_gate",
    }
    observed_slots = set(handoff.get("required_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold handoff package missing validation slots: {missing_slots}")

    hostess = document.get("hostess_boundary", {})
    if hostess.get("status") != "future_lane_not_requested":
        errors.append("Manifold handoff package Hostess status must be future_lane_not_requested")
    if hostess.get("route_status") != "not_created":
        errors.append("Manifold handoff package Hostess route_status must be not_created")
    if hostess.get("device_action_authority") != "not_in_sidecar":
        errors.append("Manifold handoff package Hostess device_action_authority must be not_in_sidecar")
    if hostess.get("input_role") != "manifold_accepted_state_or_operator_request":
        errors.append("Manifold handoff package Hostess input_role must require Manifold state or operator request")
    if hostess.get("allowed_action_class") != "operator_recovery_request_descriptor":
        errors.append("Manifold handoff package Hostess allowed_action_class must be operator_recovery_request_descriptor")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold handoff package local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/package_manifold_handoff.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold handoff package missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold handoff package damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "reject_endpoint_command_adb_stale_untrusted_inputs_before_acceptance":
        errors.append("Manifold handoff package future_manifold_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold handoff package privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold handoff package public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold handoff package must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold handoff package contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold handoff package check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold handoff package fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold handoff package manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold handoff package pass_count does not match checks")
    if document.get("package_status") == "handoff_package_ready" and fail_count != 0:
        errors.append("ready Manifold handoff package must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold handoff package must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_contract_intake_or_operator_approved_private_rehearsal_evidence":
        errors.append("Manifold handoff package next_gate is invalid")
    return errors


def validate_manifold_contract_intake_request(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("request_status") not in {"ready_for_manifold_contract_intake", "manual_review", "blocked"}:
        errors.append("Manifold contract intake request has invalid request_status")

    source = document.get("source_handoff_package", {})
    if source.get("path") != "fixtures/valid/manifold-handoff-package.synthetic.json":
        errors.append("Manifold contract intake request must point at the synthetic handoff package fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_handoff_package.v1":
        errors.append("Manifold contract intake request source schema is invalid")
    if source.get("package_status") != "handoff_package_ready":
        errors.append("Manifold contract intake request requires a handoff_package_ready source package")
    if source.get("next_gate") != "manifold_repo_contract_intake_or_operator_approved_private_rehearsal_evidence":
        errors.append("Manifold contract intake request source next_gate is invalid")

    scope = document.get("request_scope", {})
    if scope.get("request_class") != "manifold_contract_intake_descriptor":
        errors.append("Manifold contract intake request class must be manifold_contract_intake_descriptor")
    if scope.get("source_mode") != "synthetic_fixture":
        errors.append("Manifold contract intake request source_mode must remain synthetic_fixture")
    if scope.get("target_repo") != "rusty.manifold":
        errors.append("Manifold contract intake request target_repo must be rusty.manifold")
    if scope.get("repo_touch_status") != "not_touched":
        errors.append("Manifold contract intake request repo_touch_status must be not_touched")
    if scope.get("implementation_status") != "not_implemented":
        errors.append("Manifold contract intake request implementation_status must be not_implemented")
    if scope.get("route_status") != "not_created":
        errors.append("Manifold contract intake request route_status must be not_created")
    if scope.get("accepted_state_status") != "not_created":
        errors.append("Manifold contract intake request accepted_state_status must be not_created")
    if scope.get("live_evidence_status") != "not_included":
        errors.append("Manifold contract intake request live_evidence_status must be not_included")

    authority = document.get("authority", {})
    if authority.get("request_owner") != "rusty.quest.sidecar_mesh":
        errors.append("Manifold contract intake request owner must be rusty.quest.sidecar_mesh")
    if authority.get("intake_acceptance_owner") != "rusty.manifold":
        errors.append("Manifold contract intake request intake_acceptance_owner must be rusty.manifold")
    if authority.get("runtime_authority_owner") != "rusty.manifold":
        errors.append("Manifold contract intake request runtime_authority_owner must be rusty.manifold")
    if authority.get("session_authority_owner") != "rusty.manifold":
        errors.append("Manifold contract intake request session_authority_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("Manifold contract intake request audit_owner must be rusty.manifold.audit")
    if authority.get("accepted_state_owner") != "rusty.manifold":
        errors.append("Manifold contract intake request accepted_state_owner must be rusty.manifold")
    if authority.get("sidecar_role") != "observer_proposer":
        errors.append("Manifold contract intake request sidecar_role must be observer_proposer")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("Manifold contract intake request proposal_status must be not_accepted")

    intake = document.get("proposed_contract_intake", {})
    if intake.get("status") != "candidate":
        errors.append("Manifold contract intake request proposed intake status must be candidate")
    if intake.get("target_repo") != "rusty.manifold":
        errors.append("Manifold contract intake request proposed intake target_repo must be rusty.manifold")
    if intake.get("requested_request_type") != "open_sidecar_mesh_contract_intake":
        errors.append("Manifold contract intake request requested_request_type is invalid")
    if intake.get("required_acceptance_owner") != "rusty.manifold":
        errors.append("Manifold contract intake request required_acceptance_owner must be rusty.manifold")
    if intake.get("required_audit_owner") != "rusty.manifold.audit":
        errors.append("Manifold contract intake request required_audit_owner must be rusty.manifold.audit")
    if intake.get("accepted_state_status") != "not_created":
        errors.append("Manifold contract intake request proposed intake accepted_state_status must be not_created")
    if intake.get("hostess_escalation_input") != "manifold_accepted_state_or_operator_request":
        errors.append("Manifold contract intake request Hostess escalation input must require Manifold state or operator request")

    required_surfaces = {
        "sidecar_peer_status_source",
        "sidecar_peer_status_intake",
        "sidecar_peer_rehearsal_audit",
    }
    observed_surfaces = set(intake.get("candidate_surfaces", []))
    missing_surfaces = sorted(required_surfaces - observed_surfaces)
    if missing_surfaces:
        errors.append(f"Manifold contract intake request missing candidate surfaces: {missing_surfaces}")
    required_slots = {
        "slot.schema_and_fixture_validation",
        "slot.damaged_boundary_fixtures",
        "slot.future_manifold_contract_gate",
    }
    observed_slots = set(intake.get("candidate_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold contract intake request missing validation slots: {missing_slots}")
    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
    }
    observed_rejections = set(intake.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold contract intake request missing rejection terms: {missing_rejections}")

    hostess = document.get("hostess_boundary", {})
    if hostess.get("status") != "future_lane_not_requested":
        errors.append("Manifold contract intake request Hostess status must be future_lane_not_requested")
    if hostess.get("route_status") != "not_created":
        errors.append("Manifold contract intake request Hostess route_status must be not_created")
    if hostess.get("device_action_authority") != "not_in_sidecar":
        errors.append("Manifold contract intake request Hostess device_action_authority must be not_in_sidecar")
    if hostess.get("input_role") != "manifold_accepted_state_or_operator_request":
        errors.append("Manifold contract intake request Hostess input_role must require Manifold state or operator request")
    if hostess.get("allowed_action_class") != "operator_recovery_request_descriptor":
        errors.append("Manifold contract intake request Hostess allowed_action_class must be operator_recovery_request_descriptor")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold contract intake request local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_contract_intake.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold contract intake request missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold contract intake request damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_schema_route_acceptance_and_audit":
        errors.append("Manifold contract intake request future_manifold_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold contract intake request privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold contract intake request public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold contract intake request must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold contract intake request contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold contract intake request check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold contract intake request fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold contract intake request manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold contract intake request pass_count does not match checks")
    if document.get("request_status") == "ready_for_manifold_contract_intake" and fail_count != 0:
        errors.append("ready Manifold contract intake request must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold contract intake request must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence":
        errors.append("Manifold contract intake request next_gate is invalid")
    return errors


def validate_private_rehearsal_approval_request(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("request_status") not in {"operator_approval_required", "manual_review", "blocked"}:
        errors.append("private rehearsal approval request has invalid request_status")

    source_plan = document.get("source_peer_rehearsal_plan", {})
    if source_plan.get("path") != "fixtures/valid/configured-peer-rehearsal-plan.synthetic.json":
        errors.append("private rehearsal approval request must point at the configured peer rehearsal plan fixture")
    if source_plan.get("schema") != "rusty.quest.sidecar.configured_peer_rehearsal_plan.v1":
        errors.append("private rehearsal approval request source peer plan schema is invalid")
    if source_plan.get("plan_status") != "operator_approval_required":
        errors.append("private rehearsal approval request source peer plan must require operator approval")
    if source_plan.get("next_gate") != "operator_approved_private_rehearsal_evidence_or_manifold_adapter_contract":
        errors.append("private rehearsal approval request source peer plan next_gate is invalid")

    source_contract = document.get("source_contract_intake_request", {})
    if source_contract.get("path") != "fixtures/valid/manifold-contract-intake-request.synthetic.json":
        errors.append("private rehearsal approval request must point at the Manifold contract intake request fixture")
    if source_contract.get("schema") != "rusty.quest.sidecar.manifold_contract_intake_request.v1":
        errors.append("private rehearsal approval request source contract request schema is invalid")
    if source_contract.get("request_status") != "ready_for_manifold_contract_intake":
        errors.append("private rehearsal approval request source contract request must be ready")
    if source_contract.get("next_gate") != "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence":
        errors.append("private rehearsal approval request source contract request next_gate is invalid")

    scope = document.get("approval_scope", {})
    expected_scope = {
        "request_class": "private_configured_peer_rehearsal_approval_descriptor",
        "source_mode": "synthetic_fixture",
        "operator_approval_status": "not_recorded",
        "route_status": "not_started",
        "implementation_status": "not_implemented",
        "live_evidence_status": "not_collected",
        "endpoint_material_status": "private_evidence_required_not_in_fixture",
        "adb_status": "not_used",
        "command_status": "no_commands",
        "hostess_route_status": "not_created",
        "manifold_route_status": "not_created",
        "accepted_state_status": "not_created",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"private rehearsal approval request approval_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "request_owner": "rusty.quest.sidecar_mesh",
        "approval_owner": "operator",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"private rehearsal approval request authority.{key} must be {expected}")

    requested = document.get("requested_rehearsal", {})
    expected_requested = {
        "status": "candidate",
        "peer_scope": "configured_status_peers",
        "source_mode": "synthetic_fixture",
        "message_class": "status_only",
        "allowed_payload_class": "low_rate_advisory_status",
        "operator_approval_required": True,
        "route_start_allowed": False,
        "requires_private_configured_material": True,
        "public_fixture_contains_endpoint_values": False,
        "adb_allowed": False,
        "commands_allowed": False,
        "remote_desktop_allowed": False,
        "file_transfer_allowed": False,
        "hostess_escalation_input": "manifold_accepted_state_or_operator_request",
    }
    for key, expected in expected_requested.items():
        if requested.get(key) != expected:
            errors.append(f"private rehearsal approval request requested_rehearsal.{key} must be {expected}")

    operator_packet = document.get("operator_packet", {})
    if operator_packet.get("packet_status") != "draft":
        errors.append("private rehearsal approval request operator_packet.packet_status must be draft")
    if operator_packet.get("approval_decision") != "not_recorded":
        errors.append("private rehearsal approval request approval_decision must be not_recorded")
    if operator_packet.get("approval_record_status") != "not_created":
        errors.append("private rehearsal approval request approval_record_status must be not_created")

    required_private_inputs = {
        "peer_identity_map",
        "operator_selected_transport",
        "endpoint_material_private_evidence",
        "cleanup_plan",
    }
    observed_private_inputs = set(operator_packet.get("required_private_inputs", []))
    missing_private_inputs = sorted(required_private_inputs - observed_private_inputs)
    if missing_private_inputs:
        errors.append(f"private rehearsal approval request missing private inputs: {missing_private_inputs}")

    required_public_derivatives = {
        "route_health_summary",
        "sanitized_peer_status_summary",
        "cleanup_result_summary",
    }
    observed_public_derivatives = set(operator_packet.get("required_public_derivatives", []))
    missing_public_derivatives = sorted(required_public_derivatives - observed_public_derivatives)
    if missing_public_derivatives:
        errors.append(f"private rehearsal approval request missing public derivatives: {missing_public_derivatives}")

    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
    }
    observed_rejections = set(operator_packet.get("rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"private rehearsal approval request missing rejection terms: {missing_rejections}")

    hostess = document.get("hostess_boundary", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"private rehearsal approval request Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("private rehearsal approval request local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_private_rehearsal_approval.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"private rehearsal approval request missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("private rehearsal approval request damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_schema_route_acceptance_and_audit":
        errors.append("private rehearsal approval request future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("private rehearsal approval request future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"private rehearsal approval request privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("private rehearsal approval request public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("private rehearsal approval request must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("private rehearsal approval request contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("private rehearsal approval request check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("private rehearsal approval request fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("private rehearsal approval request manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("private rehearsal approval request pass_count does not match checks")
    if document.get("request_status") == "operator_approval_required" and fail_count != 0:
        errors.append("operator approval required private rehearsal request must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Operator approval" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("private rehearsal approval request must preserve operator, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "operator_decision_or_manifold_repo_owned_contract_schema":
        errors.append("private rehearsal approval request next_gate is invalid")
    return errors


def validate_private_rehearsal_evidence_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {"ready_for_operator_approved_private_evidence_plan", "manual_review", "blocked"}:
        errors.append("private rehearsal evidence expectation has invalid expectation_status")

    source_approval = document.get("source_private_rehearsal_approval_request", {})
    if source_approval.get("path") != "fixtures/valid/private-rehearsal-approval-request.synthetic.json":
        errors.append("private rehearsal evidence expectation must point at the private rehearsal approval request fixture")
    if source_approval.get("schema") != "rusty.quest.sidecar.private_rehearsal_approval_request.v1":
        errors.append("private rehearsal evidence expectation source approval request schema is invalid")
    if source_approval.get("request_status") != "operator_approval_required":
        errors.append("private rehearsal evidence expectation source approval request must require operator approval")
    if source_approval.get("next_gate") != "operator_decision_or_manifold_repo_owned_contract_schema":
        errors.append("private rehearsal evidence expectation source approval request next_gate is invalid")

    source_hostess = document.get("source_hostess_boundary_descriptor_expectation", {})
    if source_hostess.get("path") != "fixtures/valid/hostess-boundary-descriptor-expectation.synthetic.json":
        errors.append("private rehearsal evidence expectation must point at the Hostess boundary descriptor expectation fixture")
    if source_hostess.get("schema") != "rusty.quest.sidecar.hostess_boundary_descriptor_expectation.v1":
        errors.append("private rehearsal evidence expectation source Hostess schema is invalid")
    if source_hostess.get("expectation_status") != "ready_for_future_hostess_boundary_descriptor":
        errors.append("private rehearsal evidence expectation source Hostess boundary expectation must be ready")
    if source_hostess.get("next_gate") != "manifold_response_slice_or_operator_decision":
        errors.append("private rehearsal evidence expectation source Hostess boundary next_gate is invalid")

    scope = document.get("evidence_scope", {})
    expected_scope = {
        "expectation_class": "private_configured_peer_rehearsal_evidence_expectation",
        "source_mode": "synthetic_fixture",
        "operator_approval_status": "not_recorded",
        "rehearsal_route_status": "not_started",
        "private_evidence_status": "not_collected",
        "public_derivative_status": "not_created",
        "manifold_intake_status": "not_submitted",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
        "endpoint_material_status": "private_only_after_operator_approval",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"private rehearsal evidence expectation evidence_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "approval_owner": "operator",
        "private_evidence_capture_owner": "operator",
        "public_derivative_owner": "rusty.quest.sidecar_mesh",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"private rehearsal evidence expectation authority.{key} must be {expected}")

    private_requirements = document.get("private_evidence_requirements", {})
    expected_private_requirements = {
        "status": "not_collected",
        "private_store_required": True,
        "public_fixture_may_include_private_values": False,
        "operator_approval_required": True,
        "duration_limit_required": True,
        "cleanup_required": True,
        "route_start_allowed_by_this_fixture": False,
        "allowed_transport_profile": "configured_status_only",
        "allowed_message_class": "status_only",
        "allowed_payload_class": "low_rate_advisory_status",
    }
    for key, expected in expected_private_requirements.items():
        if private_requirements.get(key) != expected:
            errors.append(f"private rehearsal evidence expectation private_evidence_requirements.{key} must be {expected}")

    required_private_artifacts = {
        "peer_identity_map",
        "selected_transport_descriptor",
        "endpoint_material_private_evidence",
        "private_route_health_trace",
        "cleanup_result",
        "redaction_review_input",
    }
    missing_private_artifacts = sorted(required_private_artifacts - set(private_requirements.get("required_private_artifacts", [])))
    if missing_private_artifacts:
        errors.append(f"private rehearsal evidence expectation missing private artifacts: {missing_private_artifacts}")

    required_disallowed_actions = {
        "commands",
        "adb",
        "install",
        "launch",
        "recovery",
        "remote_desktop_control",
        "file_transfer",
        "high_rate_payloads",
    }
    missing_disallowed_actions = sorted(required_disallowed_actions - set(private_requirements.get("disallowed_private_actions", [])))
    if missing_disallowed_actions:
        errors.append(f"private rehearsal evidence expectation missing disallowed private actions: {missing_disallowed_actions}")

    public_requirements = document.get("public_derivative_requirements", {})
    expected_public_requirements = {
        "status": "not_created",
        "candidate_schema": "rusty.quest.sidecar.private_rehearsal_public_derivative.v1",
        "candidate_schema_status": "not_created",
        "contains_private_values": False,
        "public_fixture_policy": "synthetic_descriptor_only",
    }
    for key, expected in expected_public_requirements.items():
        if public_requirements.get(key) != expected:
            errors.append(f"private rehearsal evidence expectation public_derivative_requirements.{key} must be {expected}")

    required_public_fields = {
        "rehearsal_id",
        "approval_record_id",
        "participant_count",
        "message_class",
        "route_health_summary",
        "sanitized_peer_status_summary",
        "stale_peer_count",
        "redaction_status",
        "cleanup_status",
        "rejected_input_classes",
        "privacy_boundary",
    }
    missing_public_fields = sorted(required_public_fields - set(public_requirements.get("required_fields", [])))
    if missing_public_fields:
        errors.append(f"private rehearsal evidence expectation missing public derivative fields: {missing_public_fields}")

    prohibited_public_fields = {
        "endpoint_values",
        "commands",
        "adb",
        "pairing_material",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "package_ids",
    }
    missing_prohibited_fields = sorted(prohibited_public_fields - set(public_requirements.get("prohibited_public_fields", [])))
    if missing_prohibited_fields:
        errors.append(f"private rehearsal evidence expectation missing prohibited public fields: {missing_prohibited_fields}")

    required_redactions = {
        "endpoint_values_removed",
        "pairing_material_removed",
        "commands_absent",
        "adb_absent",
        "raw_logs_not_copied",
        "visual_captures_not_copied",
        "private_device_ids_removed",
    }
    missing_redactions = sorted(required_redactions - set(public_requirements.get("required_redaction_results", [])))
    if missing_redactions:
        errors.append(f"private rehearsal evidence expectation missing redaction results: {missing_redactions}")

    manifold = document.get("manifold_handoff_expectation", {})
    expected_manifold = {
        "target_repo": "rusty.manifold",
        "submission_status": "not_submitted",
        "requires_operator_approval": True,
        "requires_public_derivative": True,
        "requires_redaction_review": True,
        "acceptance_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_status": "not_created",
    }
    for key, expected in expected_manifold.items():
        if manifold.get(key) != expected:
            errors.append(f"private rehearsal evidence expectation manifold_handoff_expectation.{key} must be {expected}")
    if set(manifold.get("allowed_decisions", [])) != {"accepted_for_manifold_slice", "revision_requested", "rejected"}:
        errors.append("private rehearsal evidence expectation allowed_decisions are invalid")
    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "cleanup_incomplete",
    }
    missing_rejections = sorted(required_rejections - set(manifold.get("required_rejection_terms", [])))
    if missing_rejections:
        errors.append(f"private rehearsal evidence expectation missing rejection terms: {missing_rejections}")

    hostess = document.get("hostess_escalation_boundary", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"private rehearsal evidence expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("private rehearsal evidence expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_private_rehearsal_evidence_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"private rehearsal evidence expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("private rehearsal evidence expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_accepts_sanitized_derivative_after_operator_approval":
        errors.append("private rehearsal evidence expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("private rehearsal evidence expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"private rehearsal evidence expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("private rehearsal evidence expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("private rehearsal evidence expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("private rehearsal evidence expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("private rehearsal evidence expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("private rehearsal evidence expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("private rehearsal evidence expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("private rehearsal evidence expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_operator_approved_private_evidence_plan" and fail_count != 0:
        errors.append("ready private rehearsal evidence expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Operator approval" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("private rehearsal evidence expectation must preserve operator, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "operator_decision_or_manifold_response_slice":
        errors.append("private rehearsal evidence expectation next_gate is invalid")
    return errors


def validate_private_rehearsal_public_derivative_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {"ready_for_sanitized_public_derivative_contract", "manual_review", "blocked"}:
        errors.append("private rehearsal public derivative expectation has invalid expectation_status")

    source = document.get("source_private_rehearsal_evidence_expectation", {})
    if source.get("path") != "fixtures/valid/private-rehearsal-evidence-expectation.synthetic.json":
        errors.append("private rehearsal public derivative expectation must point at the private evidence expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1":
        errors.append("private rehearsal public derivative expectation source schema is invalid")
    if source.get("expectation_status") != "ready_for_operator_approved_private_evidence_plan":
        errors.append("private rehearsal public derivative expectation source evidence expectation must be ready")
    if source.get("next_gate") != "operator_decision_or_manifold_response_slice":
        errors.append("private rehearsal public derivative expectation source next_gate is invalid")

    scope = document.get("derivative_scope", {})
    expected_scope = {
        "expectation_class": "private_rehearsal_public_derivative_contract_expectation",
        "source_mode": "synthetic_fixture",
        "operator_approval_status": "not_recorded",
        "private_evidence_status": "not_collected",
        "public_derivative_status": "not_created",
        "derivative_schema_status": "not_created",
        "manifold_intake_status": "not_submitted",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
        "raw_artifact_status": "not_included",
        "endpoint_material_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"private rehearsal public derivative expectation derivative_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
        "derivative_contract_owner": "rusty.quest.sidecar_mesh",
        "redaction_review_owner": "operator",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"private rehearsal public derivative expectation authority.{key} must be {expected}")

    derivative = document.get("expected_public_derivative", {})
    expected_derivative = {
        "candidate_schema": "rusty.quest.sidecar.private_rehearsal_public_derivative.v1",
        "schema_status": "not_created",
        "artifact_status": "not_created",
        "source_private_evidence_policy": "operator_approved_private_store_only",
        "input_policy": "sanitized_summary_only",
        "allowed_message_class": "status_only",
        "allowed_payload_class": "low_rate_advisory_status",
        "public_fixture_policy": "synthetic_descriptor_only",
        "contains_private_values": False,
        "rejects_direct_hostess_input": True,
        "rejects_manifold_accepted_state": True,
    }
    for key, expected in expected_derivative.items():
        if derivative.get(key) != expected:
            errors.append(f"private rehearsal public derivative expectation expected_public_derivative.{key} must be {expected}")

    required_allowed_fields = {
        "derivative_id",
        "source_expectation_id",
        "approval_record_id",
        "rehearsal_id",
        "generated_at",
        "participant_count",
        "message_class",
        "route_health_summary",
        "sanitized_peer_status_summary",
        "stale_peer_count",
        "cleanup_status",
        "redaction_status",
        "rejected_input_classes",
        "privacy_boundary",
        "manifold_handoff_hint",
        "hostess_escalation_boundary",
        "validation_evidence",
        "summary",
    }
    missing_allowed_fields = sorted(required_allowed_fields - set(derivative.get("allowed_fields", [])))
    if missing_allowed_fields:
        errors.append(f"private rehearsal public derivative expectation missing allowed fields: {missing_allowed_fields}")

    required_prohibited_fields = {
        "endpoint_values",
        "commands",
        "adb",
        "pairing_material",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "package_ids",
        "screenshots",
        "logcat",
        "shell_text",
    }
    missing_prohibited_fields = sorted(required_prohibited_fields - set(derivative.get("prohibited_fields", [])))
    if missing_prohibited_fields:
        errors.append(f"private rehearsal public derivative expectation missing prohibited fields: {missing_prohibited_fields}")

    required_redactions = {
        "endpoint_values_removed",
        "pairing_material_removed",
        "commands_absent",
        "adb_absent",
        "raw_logs_not_copied",
        "visual_captures_not_copied",
        "private_device_ids_removed",
    }
    missing_redactions = sorted(required_redactions - set(derivative.get("required_redaction_results", [])))
    if missing_redactions:
        errors.append(f"private rehearsal public derivative expectation missing redaction results: {missing_redactions}")

    required_summary_classes = {
        "aggregate_counts",
        "health_status",
        "stale_peer_count",
        "cleanup_result_summary",
        "rejection_terms",
    }
    missing_summary_classes = sorted(required_summary_classes - set(derivative.get("accepted_summary_classes", [])))
    if missing_summary_classes:
        errors.append(f"private rehearsal public derivative expectation missing summary classes: {missing_summary_classes}")

    manifold = document.get("manifold_handoff_gate", {})
    expected_manifold = {
        "target_repo": "rusty.manifold",
        "submission_status": "not_submitted",
        "requires_operator_approval": True,
        "requires_public_derivative_schema": True,
        "requires_redaction_review": True,
        "requires_validation_report": True,
        "acceptance_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_status": "not_created",
    }
    for key, expected in expected_manifold.items():
        if manifold.get(key) != expected:
            errors.append(f"private rehearsal public derivative expectation manifold_handoff_gate.{key} must be {expected}")
    if set(manifold.get("allowed_decisions", [])) != {"accepted_for_manifold_slice", "revision_requested", "rejected"}:
        errors.append("private rehearsal public derivative expectation allowed_decisions are invalid")
    required_rejections = {
        "operator_approval_missing",
        "public_derivative_schema_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "cleanup_incomplete",
    }
    missing_rejections = sorted(required_rejections - set(manifold.get("required_rejection_terms", [])))
    if missing_rejections:
        errors.append(f"private rehearsal public derivative expectation missing rejection terms: {missing_rejections}")

    hostess = document.get("hostess_escalation_boundary", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"private rehearsal public derivative expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("private rehearsal public derivative expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_private_rehearsal_public_derivative_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"private rehearsal public derivative expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("private rehearsal public derivative expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_accepts_only_sanitized_public_derivative":
        errors.append("private rehearsal public derivative expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("private rehearsal public derivative expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"private rehearsal public derivative expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("private rehearsal public derivative expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("private rehearsal public derivative expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("private rehearsal public derivative expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("private rehearsal public derivative expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("private rehearsal public derivative expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("private rehearsal public derivative expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("private rehearsal public derivative expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_sanitized_public_derivative_contract" and fail_count != 0:
        errors.append("ready private rehearsal public derivative expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "operator approval" not in boundary_text.lower() or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("private rehearsal public derivative expectation must preserve operator, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "operator_decision_or_manifold_public_derivative_schema_slice":
        errors.append("private rehearsal public derivative expectation next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_request(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("request_status") not in {"ready_for_manifold_public_derivative_schema_review", "manual_review", "blocked"}:
        errors.append("Manifold public derivative schema request has invalid request_status")

    source = document.get("source_public_derivative_expectation", {})
    if source.get("path") != "fixtures/valid/private-rehearsal-public-derivative-expectation.synthetic.json":
        errors.append("Manifold public derivative schema request must point at the public derivative expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1":
        errors.append("Manifold public derivative schema request source schema is invalid")
    if source.get("expectation_status") != "ready_for_sanitized_public_derivative_contract":
        errors.append("Manifold public derivative schema request source expectation must be ready")
    if source.get("next_gate") != "operator_decision_or_manifold_public_derivative_schema_slice":
        errors.append("Manifold public derivative schema request source next_gate is invalid")

    scope = document.get("request_scope", {})
    expected_scope = {
        "request_class": "manifold_owned_public_derivative_schema_request",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "schema_status": "not_created",
        "route_handler_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "public_derivative_status": "not_created",
        "private_evidence_status": "not_collected",
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
        "endpoint_material_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema request request_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "request_owner": "rusty.quest.sidecar_mesh",
        "schema_owner": "rusty.manifold",
        "route_owner": "rusty.manifold",
        "review_owner": "rusty.manifold",
        "handoff_acceptance_owner": "rusty.manifold",
        "runtime_authority_owner": "rusty.manifold",
        "session_authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_owner": "rusty.manifold",
        "redaction_review_owner": "operator",
        "hostess_device_action_authority": "not_in_sidecar",
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema request authority.{key} must be {expected}")

    schema = document.get("proposed_manifold_schema", {})
    expected_schema = {
        "candidate_schema_id": "rusty.manifold.sidecar_peer_status_public_derivative.v1",
        "schema_status": "not_created",
        "schema_owner": "rusty.manifold",
        "source_contract": "rusty.quest.sidecar.private_rehearsal_public_derivative.v1",
        "source_contract_status": "not_created",
        "input_policy": "sanitized_summary_only",
        "allowed_payload_class": "low_rate_advisory_status",
        "allowed_message_class": "status_only",
        "public_fixture_policy": "synthetic_descriptor_only",
        "accepted_state_mapping_status": "not_created",
        "audit_fixture_status": "not_created",
        "contains_private_values": False,
        "creates_accepted_state": False,
        "creates_hostess_input": False,
    }
    for key, expected in expected_schema.items():
        if schema.get(key) != expected:
            errors.append(f"Manifold public derivative schema request proposed_manifold_schema.{key} must be {expected}")

    required_fields = {
        "derivative_id",
        "source_expectation_id",
        "approval_record_id",
        "rehearsal_id",
        "generated_at",
        "participant_count",
        "message_class",
        "route_health_summary",
        "sanitized_peer_status_summary",
        "stale_peer_count",
        "cleanup_status",
        "redaction_status",
        "rejected_input_classes",
        "privacy_boundary",
        "validation_evidence",
        "summary",
    }
    missing_fields = sorted(required_fields - set(schema.get("required_fields", [])))
    if missing_fields:
        errors.append(f"Manifold public derivative schema request missing required fields: {missing_fields}")

    prohibited_fields = {
        "endpoint_values",
        "commands",
        "adb",
        "pairing_material",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "package_ids",
        "screenshots",
        "logcat",
        "shell_text",
    }
    missing_prohibited = sorted(prohibited_fields - set(schema.get("prohibited_fields", [])))
    if missing_prohibited:
        errors.append(f"Manifold public derivative schema request missing prohibited fields: {missing_prohibited}")

    required_rejections = {
        "operator_approval_missing",
        "public_derivative_schema_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "cleanup_incomplete",
    }
    missing_rejections = sorted(required_rejections - set(schema.get("required_rejection_terms", [])))
    if missing_rejections:
        errors.append(f"Manifold public derivative schema request missing rejection terms: {missing_rejections}")

    route = document.get("proposed_manifold_route", {})
    expected_route = {
        "route_id": "route.sidecar_peer_status_public_derivative_intake",
        "route_status": "not_created",
        "route_owner": "rusty.manifold",
        "input_schema": "rusty.manifold.sidecar_peer_status_public_derivative.v1",
        "input_schema_status": "not_created",
        "decision_event_status": "not_created",
        "audit_record_status": "not_created",
        "accepted_state_status": "not_created",
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold public derivative schema request proposed_manifold_route.{key} must be {expected}")
    if set(route.get("allowed_decisions", [])) != {"accepted_for_manifold_slice", "revision_requested", "rejected"}:
        errors.append("Manifold public derivative schema request allowed_decisions are invalid")
    forbidden_route_inputs = {
        "endpoint_values",
        "commands",
        "adb",
        "pairing_material",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "hostess_direct_action",
    }
    missing_forbidden_inputs = sorted(forbidden_route_inputs - set(route.get("forbidden_route_inputs", [])))
    if missing_forbidden_inputs:
        errors.append(f"Manifold public derivative schema request missing forbidden route inputs: {missing_forbidden_inputs}")

    gate = document.get("manifold_review_gate", {})
    expected_gate = {
        "target_repo": "rusty.manifold",
        "review_status": "not_submitted",
        "requires_schema_review": True,
        "requires_route_review": True,
        "requires_redaction_review": True,
        "requires_validation_report": True,
        "requires_operator_approval": True,
        "acceptance_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "accepted_state_status": "not_created",
    }
    for key, expected in expected_gate.items():
        if gate.get(key) != expected:
            errors.append(f"Manifold public derivative schema request manifold_review_gate.{key} must be {expected}")
    if set(gate.get("allowed_outcomes", [])) != {"accepted_for_manifold_slice", "revision_requested", "rejected"}:
        errors.append("Manifold public derivative schema request allowed_outcomes are invalid")

    hostess = document.get("hostess_escalation_boundary", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema request Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema request local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_request.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema request missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema request damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_public_derivative_schema_route_and_audit":
        errors.append("Manifold public derivative schema request future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold public derivative schema request future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema request privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema request public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema request must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema request contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema request check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema request fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema request manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema request pass_count does not match checks")
    if document.get("request_status") == "ready_for_manifold_public_derivative_schema_review" and fail_count != 0:
        errors.append("ready Manifold public derivative schema request must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Operator approval" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema request must preserve Manifold, operator, and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_public_derivative_schema_review_or_operator_decision":
        errors.append("Manifold public derivative schema request next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_response_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {"ready_for_manifold_public_derivative_schema_response", "manual_review", "blocked"}:
        errors.append("Manifold public derivative schema response expectation has invalid expectation_status")

    source = document.get("source_manifold_public_derivative_schema_request", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-request.synthetic.json":
        errors.append("Manifold public derivative schema response expectation must point at the schema request fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_request.v1":
        errors.append("Manifold public derivative schema response expectation source request schema is invalid")
    if source.get("request_status") != "ready_for_manifold_public_derivative_schema_review":
        errors.append("Manifold public derivative schema response expectation source schema request must be ready")
    if source.get("next_gate") != "manifold_repo_public_derivative_schema_review_or_operator_decision":
        errors.append("Manifold public derivative schema response expectation source request next_gate is invalid")

    scope = document.get("response_expectation_scope", {})
    expected_scope = {
        "expectation_class": "manifold_owned_public_derivative_schema_response_expectation",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "schema_status": "not_created",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "public_derivative_status": "not_created",
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema response expectation response_expectation_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema response expectation authority.{key} must be {expected}")

    response = document.get("expected_manifold_response", {})
    if response.get("response_class") != "manifold_owned_public_derivative_schema_review_response":
        errors.append("Manifold public derivative schema response expectation response_class is invalid")
    if response.get("response_status") != "not_created":
        errors.append("Manifold public derivative schema response expectation response_status must be not_created")
    if response.get("decision_status") != "not_decided":
        errors.append("Manifold public derivative schema response expectation decision_status must be not_decided")
    if response.get("allowed_response_owner") != "rusty.manifold":
        errors.append("Manifold public derivative schema response expectation allowed_response_owner must be rusty.manifold")

    required_decisions = {
        "accepted_for_manifold_schema_slice",
        "revision_requested",
        "rejected",
    }
    missing_decisions = sorted(required_decisions - set(response.get("allowed_decisions", [])))
    if missing_decisions:
        errors.append(f"Manifold public derivative schema response expectation missing allowed decisions: {missing_decisions}")

    required_fields = {
        "response_id",
        "request_id",
        "decision",
        "decision_owner",
        "response_owner",
        "created_at",
        "revision",
        "schema_ref",
        "route_ref",
        "accepted_state_ref",
        "audit_ref",
        "rejection_terms",
        "required_revisions",
        "redaction_review",
        "operator_approval_status",
        "hostess_boundary_ref",
        "privacy_review",
        "validation_report_ref",
    }
    missing_fields = sorted(required_fields - set(response.get("required_fields", [])))
    if missing_fields:
        errors.append(f"Manifold public derivative schema response expectation missing required fields: {missing_fields}")

    required_rejections = {
        "operator_approval_missing",
        "public_derivative_schema_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "cleanup_incomplete",
        "high_rate_payload_rejected",
        "hostess_direct_action_rejected",
    }
    missing_rejections = sorted(required_rejections - set(response.get("required_rejection_terms", [])))
    if missing_rejections:
        errors.append(f"Manifold public derivative schema response expectation missing rejection terms: {missing_rejections}")

    required_revisions = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "accepted_state_mapping_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
        "validation_report_revision",
    }
    missing_revisions = sorted(required_revisions - set(response.get("required_revision_terms", [])))
    if missing_revisions:
        errors.append(f"Manifold public derivative schema response expectation missing revision terms: {missing_revisions}")

    required_audit_terms = {
        "request_id",
        "decision",
        "revision",
        "reject_or_revision_reason",
        "schema_ref",
        "route_ref",
        "accepted_state_ref",
        "operator_approval_status",
        "redaction_review_status",
    }
    missing_audit_terms = sorted(required_audit_terms - set(response.get("required_audit_terms", [])))
    if missing_audit_terms:
        errors.append(f"Manifold public derivative schema response expectation missing audit terms: {missing_audit_terms}")

    disallowed_content = {
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
    }
    missing_disallowed = sorted(disallowed_content - set(response.get("disallowed_response_content", [])))
    if missing_disallowed:
        errors.append(f"Manifold public derivative schema response expectation missing disallowed response content: {missing_disallowed}")

    if response.get("accepted_state_policy") != "manifold_owned_monotonic_revision":
        errors.append("Manifold public derivative schema response expectation accepted_state_policy is invalid")
    if response.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold public derivative schema response expectation rollback_policy is invalid")
    if response.get("public_derivative_policy") != "response_does_not_create_derivative_artifact":
        errors.append("Manifold public derivative schema response expectation public_derivative_policy is invalid")
    if response.get("hostess_input_policy") != "response_does_not_create_hostess_input":
        errors.append("Manifold public derivative schema response expectation hostess_input_policy is invalid")

    hostess = document.get("hostess_response_gate", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema response expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema response expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_response_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema response expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema response expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_public_derivative_schema_response_route_state_and_audit":
        errors.append("Manifold public derivative schema response expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold public derivative schema response expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema response expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema response expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema response expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema response expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema response expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema response expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema response expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema response expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_manifold_public_derivative_schema_response" and fail_count != 0:
        errors.append("ready Manifold public derivative schema response expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema response expectation must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_public_derivative_schema_response_or_operator_decision":
        errors.append("Manifold public derivative schema response expectation next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_implementation_preflight(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("preflight_status") not in {
        "ready_for_manifold_public_derivative_schema_slice_planning",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema implementation preflight has invalid preflight_status")

    source = document.get("source_manifold_public_derivative_schema_response_expectation", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-response-expectation.synthetic.json":
        errors.append("Manifold public derivative schema implementation preflight must point at the response expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_response_expectation.v1":
        errors.append("Manifold public derivative schema implementation preflight source expectation schema is invalid")
    if source.get("expectation_status") != "ready_for_manifold_public_derivative_schema_response":
        errors.append("Manifold public derivative schema implementation preflight source expectation must be ready")
    if source.get("next_gate") != "manifold_public_derivative_schema_response_or_operator_decision":
        errors.append("Manifold public derivative schema implementation preflight source expectation next_gate is invalid")

    scope = document.get("implementation_preflight_scope", {})
    expected_scope = {
        "preflight_class": "manifold_repo_public_derivative_schema_slice_preflight",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
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
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema implementation preflight implementation_preflight_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "preflight_owner": "rusty.quest.sidecar_mesh",
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema implementation preflight authority.{key} must be {expected}")

    requirements = document.get("manifold_repo_slice_requirements", {})
    if requirements.get("slice_class") != "manifold_owned_public_derivative_schema_slice":
        errors.append("Manifold public derivative schema implementation preflight slice_class is invalid")
    if requirements.get("target_repo") != "rusty.manifold":
        errors.append("Manifold public derivative schema implementation preflight target_repo must be rusty.manifold")
    if requirements.get("implementation_status") != "not_created_by_sidecar":
        errors.append("Manifold public derivative schema implementation preflight implementation_status must be not_created_by_sidecar")

    artifacts = requirements.get("required_manifold_owned_artifacts", [])
    if not artifacts:
        errors.append("Manifold public derivative schema implementation preflight must include required_manifold_owned_artifacts")
    required_artifact_kinds = {
        "response_schema",
        "input_schema",
        "route_handler",
        "decision_event_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "validation_report_fixture",
        "hostess_boundary_descriptor",
    }
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold public derivative schema implementation preflight missing artifact kinds: {missing_artifact_kinds}")
    for artifact in artifacts:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold public derivative schema implementation preflight artifact {artifact_id} owner must be Manifold-owned")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold public derivative schema implementation preflight artifact {artifact_id} status must be not_created_by_sidecar")

    required_slots = {
        "slot.public_derivative_response_schema_contract",
        "slot.public_derivative_schema_contract",
        "slot.public_derivative_valid_fixture",
        "slot.public_derivative_damaged_fixture",
        "slot.manifold_route_unit_tests",
        "slot.public_derivative_audit_fixture",
        "slot.accepted_state_mapping_check",
        "slot.hostess_boundary_descriptor_check",
        "slot.privacy_redaction_rejection_check",
        "slot.no_private_endpoint_or_command_content",
    }
    observed_slots = set(requirements.get("required_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold public derivative schema implementation preflight missing validation slots: {missing_slots}")

    required_decisions = {
        "accepted_for_manifold_schema_slice",
        "revision_requested",
        "rejected",
    }
    observed_decisions = set(requirements.get("required_response_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold public derivative schema implementation preflight missing response decisions: {missing_decisions}")

    required_rejections = {
        "operator_approval_missing",
        "public_derivative_schema_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "cleanup_incomplete",
        "high_rate_payload_rejected",
        "hostess_direct_action_rejected",
    }
    observed_rejections = set(requirements.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold public derivative schema implementation preflight missing rejection terms: {missing_rejections}")

    required_revisions = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "accepted_state_mapping_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
        "validation_report_revision",
    }
    observed_revisions = set(requirements.get("required_revision_terms", []))
    missing_revisions = sorted(required_revisions - observed_revisions)
    if missing_revisions:
        errors.append(f"Manifold public derivative schema implementation preflight missing revision terms: {missing_revisions}")

    route = requirements.get("required_route_boundaries", {})
    expected_route = {
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
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold public derivative schema implementation preflight route boundary {key} must be {expected}")
    if requirements.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold public derivative schema implementation preflight rollback_policy is invalid")

    hostess = document.get("hostess_boundary_preflight", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_action_class": "operator_recovery_request_descriptor",
        "preflight_result": "hostess_deferred_until_manifold_acceptance",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema implementation preflight Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema implementation preflight local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_implementation_preflight.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema implementation preflight missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema implementation preflight damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_public_derivative_schema_slice_implementation_and_audit":
        errors.append("Manifold public derivative schema implementation preflight future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold public derivative schema implementation preflight future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema implementation preflight privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema implementation preflight public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema implementation preflight must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema implementation preflight contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema implementation preflight check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema implementation preflight fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema implementation preflight manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema implementation preflight pass_count does not match checks")
    if document.get("preflight_status") == "ready_for_manifold_public_derivative_schema_slice_planning" and fail_count != 0:
        errors.append("ready Manifold public derivative schema implementation preflight must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema implementation preflight must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_public_derivative_schema_handoff_or_operator_decision":
        errors.append("Manifold public derivative schema implementation preflight next_gate is invalid")
    return errors


def validate_manifold_route_blueprint(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("blueprint_status") not in {"ready_for_manifold_repo_design_review", "manual_review", "blocked"}:
        errors.append("Manifold route blueprint has invalid blueprint_status")

    source_contract = document.get("source_contract_intake_request", {})
    if source_contract.get("path") != "fixtures/valid/manifold-contract-intake-request.synthetic.json":
        errors.append("Manifold route blueprint must point at the Manifold contract intake request fixture")
    if source_contract.get("schema") != "rusty.quest.sidecar.manifold_contract_intake_request.v1":
        errors.append("Manifold route blueprint source contract request schema is invalid")
    if source_contract.get("request_status") != "ready_for_manifold_contract_intake":
        errors.append("Manifold route blueprint source contract request must be ready")
    if source_contract.get("next_gate") != "manifold_repo_owned_contract_schema_or_operator_approved_private_rehearsal_evidence":
        errors.append("Manifold route blueprint source contract request next_gate is invalid")

    source_approval = document.get("source_private_rehearsal_approval_request", {})
    if source_approval.get("path") != "fixtures/valid/private-rehearsal-approval-request.synthetic.json":
        errors.append("Manifold route blueprint must point at the private rehearsal approval request fixture")
    if source_approval.get("schema") != "rusty.quest.sidecar.private_rehearsal_approval_request.v1":
        errors.append("Manifold route blueprint source private approval request schema is invalid")
    if source_approval.get("request_status") != "operator_approval_required":
        errors.append("Manifold route blueprint source private approval request must require operator approval")
    if source_approval.get("next_gate") != "operator_decision_or_manifold_repo_owned_contract_schema":
        errors.append("Manifold route blueprint source private approval request next_gate is invalid")

    scope = document.get("blueprint_scope", {})
    expected_scope = {
        "blueprint_class": "manifold_owned_sidecar_peer_status_route_blueprint",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "implementation_status": "not_implemented",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "live_evidence_status": "not_included",
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold route blueprint blueprint_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "blueprint_owner": "rusty.quest.sidecar_mesh",
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold route blueprint authority.{key} must be {expected}")

    route = document.get("proposed_manifold_route", {})
    expected_route = {
        "route_name": "sidecar_peer_status_intake",
        "route_status": "candidate",
        "route_creation_status": "not_created",
        "request_type": "submit_sidecar_peer_status_candidate",
        "input_payload_class": "low_rate_advisory_status",
        "output_event_class": "accept_reject_revision_audit",
        "requires_operator_approval_for_private_material": True,
        "requires_redaction_complete": True,
        "allows_endpoint_values": False,
        "allows_commands": False,
        "allows_adb": False,
        "allows_high_rate_payloads": False,
        "hostess_escalation_input": "manifold_accepted_state_or_operator_request",
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold route blueprint proposed_manifold_route.{key} must be {expected}")

    required_slots = {
        "slot.manifold_schema_contract_validation",
        "slot.sidecar_damaged_boundary_fixtures",
        "slot.manifold_accept_reject_audit_fixture",
        "slot.hostess_boundary_descriptor_check",
    }
    observed_slots = set(route.get("required_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold route blueprint missing validation slots: {missing_slots}")

    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "high_rate_payload_rejected",
    }
    observed_rejections = set(route.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold route blueprint missing rejection terms: {missing_rejections}")

    schemas = document.get("candidate_schemas", [])
    if not schemas:
        errors.append("Manifold route blueprint must include candidate_schemas")
    required_schema_roles = {"request", "decision_event", "accepted_state"}
    observed_schema_roles = {schema.get("schema_role") for schema in schemas if isinstance(schema, dict)}
    missing_schema_roles = sorted(required_schema_roles - observed_schema_roles)
    if missing_schema_roles:
        errors.append(f"Manifold route blueprint missing candidate schema roles: {missing_schema_roles}")
    for schema in schemas:
        schema_id = schema.get("schema_id", "<unknown>")
        if schema.get("owner") != "rusty.manifold":
            errors.append(f"Manifold route blueprint candidate schema {schema_id} owner must be rusty.manifold")
        if schema.get("status") != "candidate_not_created":
            errors.append(f"Manifold route blueprint candidate schema {schema_id} status must be candidate_not_created")
        if not schema.get("required_fields"):
            errors.append(f"Manifold route blueprint candidate schema {schema_id} must declare required_fields")

    audit = document.get("audit_contract", {})
    if audit.get("audit_surface") != "sidecar_peer_rehearsal_audit":
        errors.append("Manifold route blueprint audit_surface is invalid")
    if audit.get("audit_owner") != "rusty.manifold.audit":
        errors.append("Manifold route blueprint audit_owner must be rusty.manifold.audit")
    if audit.get("audit_record_status") != "not_created":
        errors.append("Manifold route blueprint audit_record_status must be not_created")
    if not audit.get("required_audit_fields"):
        errors.append("Manifold route blueprint must declare required audit fields")
    if audit.get("revision_policy") != "manifold_owned_monotonic_revision":
        errors.append("Manifold route blueprint revision_policy is invalid")
    if audit.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold route blueprint rollback_policy is invalid")

    hostess = document.get("hostess_boundary", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "input_role": "manifold_accepted_state_or_operator_request",
        "allowed_action_class": "operator_recovery_request_descriptor",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold route blueprint Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold route blueprint local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_route_blueprint.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold route blueprint missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold route blueprint damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_schema_route_acceptance_and_audit":
        errors.append("Manifold route blueprint future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold route blueprint future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold route blueprint privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold route blueprint public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold route blueprint must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold route blueprint contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold route blueprint check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold route blueprint fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold route blueprint manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold route blueprint pass_count does not match checks")
    if document.get("blueprint_status") == "ready_for_manifold_repo_design_review" and fail_count != 0:
        errors.append("ready Manifold route blueprint must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold route blueprint must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_design_review_or_operator_decision":
        errors.append("Manifold route blueprint next_gate is invalid")
    return errors


def validate_manifold_route_design_review_request(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("request_status") not in {"ready_for_manifold_route_design_review", "manual_review", "blocked"}:
        errors.append("Manifold route design review request has invalid request_status")

    source = document.get("source_manifold_route_blueprint", {})
    if source.get("path") != "fixtures/valid/manifold-route-blueprint.synthetic.json":
        errors.append("Manifold route design review request must point at the route blueprint fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_route_blueprint.v1":
        errors.append("Manifold route design review request source blueprint schema is invalid")
    if source.get("blueprint_status") != "ready_for_manifold_repo_design_review":
        errors.append("Manifold route design review request source blueprint must be ready")
    if source.get("next_gate") != "manifold_repo_design_review_or_operator_decision":
        errors.append("Manifold route design review request source blueprint next_gate is invalid")

    scope = document.get("request_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold route design review request request_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold route design review request authority.{key} must be {expected}")

    review = document.get("proposed_manifold_review", {})
    if review.get("review_status") != "requested_not_opened":
        errors.append("Manifold route design review request review_status must be requested_not_opened")
    if review.get("review_owner") != "rusty.manifold":
        errors.append("Manifold route design review request review_owner must be rusty.manifold")
    if review.get("requested_route_status") != "candidate":
        errors.append("Manifold route design review request requested_route_status must be candidate")
    if review.get("requested_payload_class") != "low_rate_advisory_status":
        errors.append("Manifold route design review request requested_payload_class must be low_rate_advisory_status")
    if review.get("decision_status") != "not_decided":
        errors.append("Manifold route design review request decision_status must be not_decided")
    if review.get("required_output_class") != "manifold_owned_schema_route_decision_or_rejection":
        errors.append("Manifold route design review request required_output_class is invalid")
    required_topics = {
        "topic.schema_contract",
        "topic.accept_reject_decision_event",
        "topic.accepted_state_revision_policy",
        "topic.audit_record_shape",
        "topic.hostess_boundary_preconditions",
        "topic.privacy_redaction_rejection_terms",
    }
    observed_topics = set(review.get("review_topics", []))
    missing_topics = sorted(required_topics - observed_topics)
    if missing_topics:
        errors.append(f"Manifold route design review request missing review topics: {missing_topics}")

    work_items = document.get("proposed_manifold_work_items", [])
    if not work_items:
        errors.append("Manifold route design review request must include proposed_manifold_work_items")
    allowed_work_item_kinds = {
        "schema",
        "route_handler",
        "audit_fixture",
        "hostess_boundary_descriptor",
    }
    required_work_item_ids = {
        "work.sidecar_peer_status_request_schema",
        "work.sidecar_peer_status_decision_schema",
        "work.sidecar_peer_status_accepted_state_schema",
        "work.sidecar_peer_status_route_handler",
        "work.sidecar_peer_status_audit_fixture",
        "work.sidecar_peer_status_hostess_boundary_descriptor",
    }
    observed_work_item_ids = {item.get("work_item_id") for item in work_items if isinstance(item, dict)}
    missing_work_items = sorted(required_work_item_ids - observed_work_item_ids)
    if missing_work_items:
        errors.append(f"Manifold route design review request missing work items: {missing_work_items}")
    for item in work_items:
        work_item_id = item.get("work_item_id", "<unknown>")
        if item.get("owner") != "rusty.manifold":
            errors.append(f"Manifold route design review request work item {work_item_id} owner must be rusty.manifold")
        if item.get("status") != "not_created":
            errors.append(f"Manifold route design review request work item {work_item_id} status must be not_created")
        if item.get("acceptance_required") is not True:
            errors.append(f"Manifold route design review request work item {work_item_id} must require acceptance")
        if item.get("work_item_kind") not in allowed_work_item_kinds:
            errors.append(f"Manifold route design review request work item {work_item_id} has invalid kind")

    hostess = document.get("hostess_integration_preconditions", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_input_class": "manifold_accepted_state_or_operator_request_descriptor",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold route design review request Hostess {key} must be {expected}")
    disallowed_inputs = set(hostess.get("disallowed_input_classes", []))
    required_disallowed_inputs = {
        "sidecar_peer_message",
        "endpoint_value",
        "command_payload",
        "adb_target",
        "pairing_material",
        "high_rate_payload",
    }
    missing_disallowed_inputs = sorted(required_disallowed_inputs - disallowed_inputs)
    if missing_disallowed_inputs:
        errors.append(f"Manifold route design review request Hostess missing disallowed inputs: {missing_disallowed_inputs}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold route design review request local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_route_design_review.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold route design review request missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold route design review request damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_schema_route_acceptance_and_audit":
        errors.append("Manifold route design review request future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold route design review request future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold route design review request privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold route design review request public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold route design review request must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold route design review request contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold route design review request check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold route design review request fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold route design review request manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold route design review request pass_count does not match checks")
    if document.get("request_status") == "ready_for_manifold_route_design_review" and fail_count != 0:
        errors.append("ready Manifold route design review request must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold route design review request must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_design_review_or_operator_decision":
        errors.append("Manifold route design review request next_gate is invalid")
    return errors


def validate_manifold_route_design_response_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {"ready_for_manifold_owned_response", "manual_review", "blocked"}:
        errors.append("Manifold route design response expectation has invalid expectation_status")

    source = document.get("source_manifold_route_design_review_request", {})
    if source.get("path") != "fixtures/valid/manifold-route-design-review-request.synthetic.json":
        errors.append("Manifold route design response expectation must point at the design review request fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_route_design_review_request.v1":
        errors.append("Manifold route design response expectation source request schema is invalid")
    if source.get("request_status") != "ready_for_manifold_route_design_review":
        errors.append("Manifold route design response expectation source design review request must be ready")
    if source.get("next_gate") != "manifold_repo_design_review_or_operator_decision":
        errors.append("Manifold route design response expectation source request next_gate is invalid")

    scope = document.get("response_expectation_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold route design response expectation response_expectation_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold route design response expectation authority.{key} must be {expected}")

    response = document.get("expected_manifold_response", {})
    if response.get("response_class") != "manifold_owned_design_review_response":
        errors.append("Manifold route design response expectation response_class is invalid")
    if response.get("response_status") != "not_created":
        errors.append("Manifold route design response expectation response_status must be not_created")
    if response.get("decision_status") != "not_decided":
        errors.append("Manifold route design response expectation decision_status must be not_decided")
    if response.get("allowed_response_owner") != "rusty.manifold":
        errors.append("Manifold route design response expectation allowed_response_owner must be rusty.manifold")

    required_decisions = {
        "accepted_for_manifold_slice",
        "revision_requested",
        "rejected",
    }
    observed_decisions = set(response.get("allowed_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold route design response expectation missing allowed decisions: {missing_decisions}")

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
    observed_fields = set(response.get("required_fields", []))
    missing_fields = sorted(required_fields - observed_fields)
    if missing_fields:
        errors.append(f"Manifold route design response expectation missing required fields: {missing_fields}")

    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "high_rate_payload_rejected",
    }
    observed_rejections = set(response.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold route design response expectation missing rejection terms: {missing_rejections}")

    required_revisions = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
    }
    observed_revisions = set(response.get("required_revision_terms", []))
    missing_revisions = sorted(required_revisions - observed_revisions)
    if missing_revisions:
        errors.append(f"Manifold route design response expectation missing revision terms: {missing_revisions}")

    required_audit_terms = {
        "request_id",
        "decision",
        "revision",
        "reject_or_revision_reason",
        "accepted_state_ref",
    }
    observed_audit_terms = set(response.get("required_audit_terms", []))
    missing_audit_terms = sorted(required_audit_terms - observed_audit_terms)
    if missing_audit_terms:
        errors.append(f"Manifold route design response expectation missing audit terms: {missing_audit_terms}")

    required_disallowed_content = {
        "endpoint_values",
        "shell_text",
        "android_target",
        "pairing_material",
        "package_markers",
        "high_rate_payloads",
        "raw_logs",
        "visual_captures",
    }
    observed_disallowed_content = set(response.get("disallowed_response_content", []))
    missing_disallowed_content = sorted(required_disallowed_content - observed_disallowed_content)
    if missing_disallowed_content:
        errors.append(f"Manifold route design response expectation missing disallowed response content: {missing_disallowed_content}")

    if response.get("accepted_state_policy") != "manifold_owned_monotonic_revision":
        errors.append("Manifold route design response expectation accepted_state_policy is invalid")
    if response.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold route design response expectation rollback_policy is invalid")

    hostess = document.get("hostess_response_gate", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_action_class": "operator_recovery_request_descriptor",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold route design response expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold route design response expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_route_design_response_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold route design response expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold route design response expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_response_decision_route_state_and_audit":
        errors.append("Manifold route design response expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold route design response expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold route design response expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold route design response expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold route design response expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold route design response expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold route design response expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold route design response expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold route design response expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold route design response expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_manifold_owned_response" and fail_count != 0:
        errors.append("ready Manifold route design response expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold route design response expectation must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_owned_response_or_operator_decision":
        errors.append("Manifold route design response expectation next_gate is invalid")
    return errors


def validate_manifold_response_implementation_preflight(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("preflight_status") not in {"ready_for_manifold_repo_slice_planning", "manual_review", "blocked"}:
        errors.append("Manifold response implementation preflight has invalid preflight_status")

    source = document.get("source_manifold_route_design_response_expectation", {})
    if source.get("path") != "fixtures/valid/manifold-route-design-response-expectation.synthetic.json":
        errors.append("Manifold response implementation preflight must point at the response expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_route_design_response_expectation.v1":
        errors.append("Manifold response implementation preflight source expectation schema is invalid")
    if source.get("expectation_status") != "ready_for_manifold_owned_response":
        errors.append("Manifold response implementation preflight source expectation must be ready")
    if source.get("next_gate") != "manifold_owned_response_or_operator_decision":
        errors.append("Manifold response implementation preflight source expectation next_gate is invalid")

    scope = document.get("implementation_preflight_scope", {})
    expected_scope = {
        "preflight_class": "manifold_repo_response_slice_preflight",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
        "repo_touch_status": "not_touched",
        "branch_status": "not_created",
        "response_status": "not_created",
        "decision_status": "not_decided",
        "route_status": "not_created",
        "accepted_state_status": "not_created",
        "audit_record_status": "not_created",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold response implementation preflight implementation_preflight_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "preflight_owner": "rusty.quest.sidecar_mesh",
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold response implementation preflight authority.{key} must be {expected}")

    requirements = document.get("manifold_repo_slice_requirements", {})
    if requirements.get("slice_class") != "manifold_owned_sidecar_peer_status_response_slice":
        errors.append("Manifold response implementation preflight slice_class is invalid")
    if requirements.get("target_repo") != "rusty.manifold":
        errors.append("Manifold response implementation preflight target_repo must be rusty.manifold")
    if requirements.get("implementation_status") != "not_created_by_sidecar":
        errors.append("Manifold response implementation preflight implementation_status must be not_created_by_sidecar")

    artifacts = requirements.get("required_manifold_owned_artifacts", [])
    if not artifacts:
        errors.append("Manifold response implementation preflight must include required_manifold_owned_artifacts")
    required_artifact_kinds = {
        "schema",
        "route_handler",
        "decision_event_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "hostess_boundary_descriptor",
    }
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold response implementation preflight missing artifact kinds: {missing_artifact_kinds}")
    for artifact in artifacts:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold response implementation preflight artifact {artifact_id} owner must be Manifold-owned")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold response implementation preflight artifact {artifact_id} status must be not_created_by_sidecar")

    required_slots = {
        "slot.manifold_response_schema_contract",
        "slot.sidecar_design_response_valid_fixture",
        "slot.sidecar_design_response_damaged_fixture",
        "slot.manifold_route_unit_tests",
        "slot.manifold_audit_fixture",
        "slot.hostess_boundary_descriptor_check",
        "slot.privacy_redaction_rejection_check",
    }
    observed_slots = set(requirements.get("required_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold response implementation preflight missing validation slots: {missing_slots}")

    required_decisions = {
        "accepted_for_manifold_slice",
        "revision_requested",
        "rejected",
    }
    observed_decisions = set(requirements.get("required_response_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold response implementation preflight missing response decisions: {missing_decisions}")

    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "high_rate_payload_rejected",
    }
    observed_rejections = set(requirements.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold response implementation preflight missing rejection terms: {missing_rejections}")

    route = requirements.get("required_route_boundaries", {})
    expected_route = {
        "input_payload_class": "low_rate_advisory_status",
        "allows_endpoint_values": False,
        "allows_commands": False,
        "allows_adb": False,
        "allows_high_rate_payloads": False,
        "allows_sidecar_direct_hostess_input": False,
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold response implementation preflight route boundary {key} must be {expected}")
    if requirements.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold response implementation preflight rollback_policy is invalid")

    hostess = document.get("hostess_boundary_preflight", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_action_class": "operator_recovery_request_descriptor",
        "preflight_result": "hostess_deferred_until_manifold_acceptance",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold response implementation preflight Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold response implementation preflight local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_response_implementation_preflight.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold response implementation preflight missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold response implementation preflight damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_response_slice_implementation_and_audit":
        errors.append("Manifold response implementation preflight future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold response implementation preflight future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold response implementation preflight privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold response implementation preflight public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold response implementation preflight must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold response implementation preflight contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold response implementation preflight check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold response implementation preflight fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold response implementation preflight manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold response implementation preflight pass_count does not match checks")
    if document.get("preflight_status") == "ready_for_manifold_repo_slice_planning" and fail_count != 0:
        errors.append("ready Manifold response implementation preflight must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold response implementation preflight must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_response_slice_or_operator_decision":
        errors.append("Manifold response implementation preflight next_gate is invalid")
    return errors


def validate_manifold_response_handoff_package(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("package_status") not in {"response_handoff_package_ready", "manual_review", "blocked"}:
        errors.append("Manifold response handoff package has invalid package_status")

    source = document.get("source_manifold_response_implementation_preflight", {})
    if source.get("path") != "fixtures/valid/manifold-response-implementation-preflight.synthetic.json":
        errors.append("Manifold response handoff package must point at the response preflight fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_response_implementation_preflight.v1":
        errors.append("Manifold response handoff package source preflight schema is invalid")
    if source.get("preflight_status") != "ready_for_manifold_repo_slice_planning":
        errors.append("Manifold response handoff package source preflight must be ready")
    if source.get("next_gate") != "manifold_repo_response_slice_or_operator_decision":
        errors.append("Manifold response handoff package source preflight next_gate is invalid")

    scope = document.get("package_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold response handoff package package_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold response handoff package authority.{key} must be {expected}")

    manifest = document.get("handoff_manifest", {})
    if manifest.get("status") != "candidate":
        errors.append("Manifold response handoff package manifest status must be candidate")
    if manifest.get("target_repo") != "rusty.manifold":
        errors.append("Manifold response handoff package target_repo must be rusty.manifold")
    if manifest.get("handoff_acceptance_status") != "not_accepted":
        errors.append("Manifold response handoff package handoff_acceptance_status must be not_accepted")
    if manifest.get("downstream_implementation_status") != "not_created":
        errors.append("Manifold response handoff package downstream_implementation_status must be not_created")

    required_sources = {
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
    sources = manifest.get("source_chain_artifacts", [])
    observed_sources = {source.get("artifact_id") for source in sources if isinstance(source, dict)}
    missing_sources = sorted(required_sources - observed_sources)
    if missing_sources:
        errors.append(f"Manifold response handoff package missing source artifacts: {missing_sources}")
    for source_artifact in sources:
        artifact_id = source_artifact.get("artifact_id", "<unknown>")
        path = source_artifact.get("path", "")
        if not path or path.startswith("/") or "\\" in path:
            errors.append(f"Manifold response handoff package source artifact {artifact_id} path must be relative slash form")
        if ".." in Path(path).parts:
            errors.append(f"Manifold response handoff package source artifact {artifact_id} path must not escape source root")
        if source_artifact.get("required_for_handoff") is not True:
            errors.append(f"Manifold response handoff package source artifact {artifact_id} must be required_for_handoff")

    required_artifact_kinds = {
        "schema",
        "route_handler",
        "decision_event_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "hostess_boundary_descriptor",
    }
    downstream_artifacts = manifest.get("required_downstream_artifacts", [])
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in downstream_artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold response handoff package missing artifact kinds: {missing_artifact_kinds}")
    for artifact in downstream_artifacts:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold response handoff package artifact {artifact_id} owner must be Manifold-owned")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold response handoff package artifact {artifact_id} status must be not_created_by_sidecar")

    required_slots = {
        "slot.manifold_response_schema_contract",
        "slot.sidecar_design_response_valid_fixture",
        "slot.sidecar_design_response_damaged_fixture",
        "slot.manifold_route_unit_tests",
        "slot.manifold_audit_fixture",
        "slot.hostess_boundary_descriptor_check",
        "slot.privacy_redaction_rejection_check",
    }
    observed_slots = set(manifest.get("required_downstream_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold response handoff package missing validation slots: {missing_slots}")

    required_decisions = {
        "accepted_for_manifold_slice",
        "revision_requested",
        "rejected",
    }
    observed_decisions = set(manifest.get("required_downstream_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold response handoff package missing response decisions: {missing_decisions}")

    required_rejections = {
        "operator_approval_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "high_rate_payload_rejected",
    }
    observed_rejections = set(manifest.get("required_downstream_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold response handoff package missing rejection terms: {missing_rejections}")

    route = manifest.get("required_route_boundaries", {})
    expected_route = {
        "input_payload_class": "low_rate_advisory_status",
        "allows_endpoint_values": False,
        "allows_commands": False,
        "allows_adb": False,
        "allows_high_rate_payloads": False,
        "allows_sidecar_direct_hostess_input": False,
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold response handoff package route boundary {key} must be {expected}")
    if manifest.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold response handoff package rollback_policy is invalid")

    hostess = document.get("hostess_boundary_handoff", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold response handoff package Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold response handoff package local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/package_manifold_response_handoff.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold response handoff package missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold response handoff package damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_response_slice_handoff_acceptance_and_implementation":
        errors.append("Manifold response handoff package future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold response handoff package future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold response handoff package privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold response handoff package public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold response handoff package must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold response handoff package contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold response handoff package check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold response handoff package fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold response handoff package manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold response handoff package pass_count does not match checks")
    if document.get("package_status") == "response_handoff_package_ready" and fail_count != 0:
        errors.append("ready Manifold response handoff package must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold response handoff package must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_response_slice_or_operator_decision":
        errors.append("Manifold response handoff package next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_handoff_package(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("package_status") not in {"public_derivative_schema_handoff_package_ready", "manual_review", "blocked"}:
        errors.append("Manifold public derivative schema handoff package has invalid package_status")

    source = document.get("source_manifold_public_derivative_schema_implementation_preflight", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-implementation-preflight.synthetic.json":
        errors.append("Manifold public derivative schema handoff package must point at the public derivative schema preflight fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_implementation_preflight.v1":
        errors.append("Manifold public derivative schema handoff package source preflight schema is invalid")
    if source.get("preflight_status") != "ready_for_manifold_public_derivative_schema_slice_planning":
        errors.append("Manifold public derivative schema handoff package source preflight must be ready")
    if source.get("next_gate") != "manifold_public_derivative_schema_handoff_or_operator_decision":
        errors.append("Manifold public derivative schema handoff package source preflight next_gate is invalid")

    scope = document.get("package_scope", {})
    expected_scope = {
        "package_class": "manifold_public_derivative_schema_slice_handoff_package",
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema handoff package package_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "package_owner": "rusty.quest.sidecar_mesh",
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema handoff package authority.{key} must be {expected}")

    manifest = document.get("handoff_manifest", {})
    if manifest.get("status") != "candidate":
        errors.append("Manifold public derivative schema handoff package manifest status must be candidate")
    if manifest.get("target_repo") != "rusty.manifold":
        errors.append("Manifold public derivative schema handoff package target_repo must be rusty.manifold")
    expected_manifest_statuses = {
        "handoff_acceptance_status": "not_accepted",
        "downstream_implementation_status": "not_created",
        "downstream_schema_status": "not_created",
        "downstream_route_status": "not_created",
        "downstream_validation_report_status": "not_created",
        "downstream_hostess_boundary_status": "not_created",
    }
    for key, expected in expected_manifest_statuses.items():
        if manifest.get(key) != expected:
            errors.append(f"Manifold public derivative schema handoff package {key} must be {expected}")

    required_sources = {
        "artifact.public_lab_artifact_drift_review",
        "artifact.no_network_prototype_handoff_review",
        "artifact.configured_peer_rehearsal_plan",
        "artifact.manifold_adapter_contract_review",
        "artifact.manifold_contract_intake_request",
        "artifact.private_rehearsal_approval_request",
        "artifact.private_rehearsal_evidence_expectation",
        "artifact.private_rehearsal_public_derivative_expectation",
        "artifact.manifold_public_derivative_schema_request",
        "artifact.manifold_public_derivative_schema_response_expectation",
        "artifact.manifold_public_derivative_schema_implementation_preflight",
        "artifact.integration_acceptance_scorecard",
    }
    sources = manifest.get("source_chain_artifacts", [])
    observed_sources = {source.get("artifact_id") for source in sources if isinstance(source, dict)}
    missing_sources = sorted(required_sources - observed_sources)
    if missing_sources:
        errors.append(f"Manifold public derivative schema handoff package missing source artifacts: {missing_sources}")
    for source_artifact in sources:
        artifact_id = source_artifact.get("artifact_id", "<unknown>")
        path = source_artifact.get("path", "")
        if not path or path.startswith("/") or "\\" in path:
            errors.append(f"Manifold public derivative schema handoff package source artifact {artifact_id} path must be relative slash form")
        if ".." in Path(path).parts:
            errors.append(f"Manifold public derivative schema handoff package source artifact {artifact_id} path must not escape source root")
        if source_artifact.get("required_for_handoff") is not True:
            errors.append(f"Manifold public derivative schema handoff package source artifact {artifact_id} must be required_for_handoff")

    required_artifact_kinds = {
        "response_schema",
        "input_schema",
        "route_handler",
        "decision_event_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "validation_report_fixture",
        "hostess_boundary_descriptor",
    }
    downstream_artifacts = manifest.get("required_downstream_artifacts", [])
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in downstream_artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold public derivative schema handoff package missing artifact kinds: {missing_artifact_kinds}")
    for artifact in downstream_artifacts:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold public derivative schema handoff package artifact {artifact_id} owner must be Manifold-owned")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold public derivative schema handoff package artifact {artifact_id} status must be not_created_by_sidecar")

    required_slots = {
        "slot.public_derivative_response_schema_contract",
        "slot.public_derivative_schema_contract",
        "slot.public_derivative_valid_fixture",
        "slot.public_derivative_damaged_fixture",
        "slot.manifold_route_unit_tests",
        "slot.public_derivative_audit_fixture",
        "slot.accepted_state_mapping_check",
        "slot.hostess_boundary_descriptor_check",
        "slot.privacy_redaction_rejection_check",
        "slot.no_private_endpoint_or_command_content",
    }
    observed_slots = set(manifest.get("required_downstream_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold public derivative schema handoff package missing validation slots: {missing_slots}")

    required_decisions = {
        "accepted_for_manifold_schema_slice",
        "revision_requested",
        "rejected",
    }
    observed_decisions = set(manifest.get("required_downstream_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold public derivative schema handoff package missing response decisions: {missing_decisions}")

    required_rejections = {
        "operator_approval_missing",
        "public_derivative_schema_missing",
        "endpoint_values_rejected",
        "commands_rejected",
        "adb_rejected",
        "stale_peer_status",
        "untrusted_sidecar",
        "redaction_incomplete",
        "cleanup_incomplete",
        "high_rate_payload_rejected",
        "hostess_direct_action_rejected",
    }
    observed_rejections = set(manifest.get("required_downstream_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold public derivative schema handoff package missing rejection terms: {missing_rejections}")

    required_revisions = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "accepted_state_mapping_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
        "validation_report_revision",
    }
    observed_revisions = set(manifest.get("required_downstream_revision_terms", []))
    missing_revisions = sorted(required_revisions - observed_revisions)
    if missing_revisions:
        errors.append(f"Manifold public derivative schema handoff package missing revision terms: {missing_revisions}")

    route = manifest.get("required_route_boundaries", {})
    expected_route = {
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
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold public derivative schema handoff package route boundary {key} must be {expected}")
    if manifest.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold public derivative schema handoff package rollback_policy is invalid")

    hostess = document.get("hostess_boundary_handoff", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "downstream_descriptor_owner": "rusty.manifold",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "handoff_result": "hostess_prepared_as_boundary_descriptor_only",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema handoff package Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema handoff package local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/package_manifold_public_derivative_schema_handoff.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema handoff package missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema handoff package damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_public_derivative_schema_handoff_acceptance_and_implementation":
        errors.append("Manifold public derivative schema handoff package future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold public derivative schema handoff package future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema handoff package privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema handoff package public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema handoff package must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema handoff package contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema handoff package check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema handoff package fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema handoff package manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema handoff package pass_count does not match checks")
    if document.get("package_status") == "public_derivative_schema_handoff_package_ready" and fail_count != 0:
        errors.append("ready Manifold public derivative schema handoff package must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema handoff package must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_public_derivative_schema_slice_or_operator_decision":
        errors.append("Manifold public derivative schema handoff package next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {
        "ready_for_manifold_public_derivative_schema_slice_response",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response expectation has invalid expectation_status")

    source = document.get("source_manifold_public_derivative_schema_handoff_package", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-handoff-package.synthetic.json":
        errors.append("Manifold public derivative schema slice response expectation must point at the handoff package fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_handoff_package.v1":
        errors.append("Manifold public derivative schema slice response expectation source package schema is invalid")
    if source.get("package_status") != "public_derivative_schema_handoff_package_ready":
        errors.append("Manifold public derivative schema slice response expectation source package must be ready")
    if source.get("next_gate") != "manifold_repo_public_derivative_schema_slice_or_operator_decision":
        errors.append("Manifold public derivative schema slice response expectation source package next_gate is invalid")

    scope = document.get("response_expectation_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response expectation response_expectation_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response expectation authority.{key} must be {expected}")

    response = document.get("expected_manifold_slice_response", {})
    if response.get("response_class") != "manifold_owned_public_derivative_schema_slice_handoff_response":
        errors.append("Manifold public derivative schema slice response expectation response_class is invalid")
    if response.get("response_status") != "not_created":
        errors.append("Manifold public derivative schema slice response expectation response_status must be not_created")
    if response.get("decision_status") != "not_decided":
        errors.append("Manifold public derivative schema slice response expectation decision_status must be not_decided")
    if response.get("allowed_response_owner") != "rusty.manifold":
        errors.append("Manifold public derivative schema slice response expectation allowed_response_owner must be rusty.manifold")

    required_decisions = {
        "accepted_for_manifold_schema_slice",
        "revision_requested",
        "rejected",
    }
    missing_decisions = sorted(required_decisions - set(response.get("allowed_decisions", [])))
    if missing_decisions:
        errors.append(f"Manifold public derivative schema slice response expectation missing allowed decisions: {missing_decisions}")

    required_fields = {
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
    }
    missing_fields = sorted(required_fields - set(response.get("required_fields", [])))
    if missing_fields:
        errors.append(f"Manifold public derivative schema slice response expectation missing required fields: {missing_fields}")

    required_rejections = {
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
    }
    missing_rejections = sorted(required_rejections - set(response.get("required_rejection_terms", [])))
    if missing_rejections:
        errors.append(f"Manifold public derivative schema slice response expectation missing rejection terms: {missing_rejections}")

    required_revisions = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "accepted_state_mapping_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
        "validation_report_revision",
        "source_chain_revision",
        "package_manifest_revision",
    }
    missing_revisions = sorted(required_revisions - set(response.get("required_revision_terms", [])))
    if missing_revisions:
        errors.append(f"Manifold public derivative schema slice response expectation missing revision terms: {missing_revisions}")

    required_audit_terms = {
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
    }
    missing_audit_terms = sorted(required_audit_terms - set(response.get("required_audit_terms", [])))
    if missing_audit_terms:
        errors.append(f"Manifold public derivative schema slice response expectation missing audit terms: {missing_audit_terms}")

    disallowed_content = {
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
    }
    missing_disallowed = sorted(disallowed_content - set(response.get("disallowed_response_content", [])))
    if missing_disallowed:
        errors.append(f"Manifold public derivative schema slice response expectation missing disallowed response content: {missing_disallowed}")

    if response.get("accepted_state_policy") != "manifold_owned_monotonic_revision":
        errors.append("Manifold public derivative schema slice response expectation accepted_state_policy is invalid")
    if response.get("implementation_policy") != "response_records_decision_only":
        errors.append("Manifold public derivative schema slice response expectation implementation_policy is invalid")
    if response.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold public derivative schema slice response expectation rollback_policy is invalid")
    if response.get("public_derivative_policy") != "response_does_not_create_derivative_artifact":
        errors.append("Manifold public derivative schema slice response expectation public_derivative_policy is invalid")
    if response.get("hostess_input_policy") != "response_does_not_create_hostess_input":
        errors.append("Manifold public derivative schema slice response expectation hostess_input_policy is invalid")

    hostess = document.get("hostess_response_gate", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_slice_response_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_public_derivative_schema_slice_response_and_audit":
        errors.append("Manifold public derivative schema slice response expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold public derivative schema slice response expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_manifold_public_derivative_schema_slice_response" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response expectation must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_public_derivative_schema_slice_response_or_operator_decision":
        errors.append("Manifold public derivative schema slice response expectation next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_handoff_package(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("package_status") not in {
        "public_derivative_schema_slice_response_handoff_package_ready",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response handoff package has invalid package_status")

    source = document.get("source_manifold_public_derivative_schema_slice_response_implementation_preflight", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json":
        errors.append("Manifold public derivative schema slice response handoff package must point at the slice response implementation preflight fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_implementation_preflight.v1":
        errors.append("Manifold public derivative schema slice response handoff package source preflight schema is invalid")
    if source.get("preflight_status") != "ready_for_manifold_public_derivative_schema_slice_response_planning":
        errors.append("Manifold public derivative schema slice response handoff package source preflight must be ready")
    if source.get("next_gate") != "manifold_public_derivative_schema_slice_response_handoff_or_operator_decision":
        errors.append("Manifold public derivative schema slice response handoff package source preflight next_gate is invalid")

    scope = document.get("package_scope", {})
    expected_scope = {
        "package_class": "manifold_public_derivative_schema_slice_response_handoff_package",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
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
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
        "hostess_input_status": "not_created",
        "live_evidence_status": "not_included",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response handoff package package_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "package_owner": "rusty.quest.sidecar_mesh",
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response handoff package authority.{key} must be {expected}")

    manifest = document.get("handoff_manifest", {})
    if manifest.get("status") != "candidate":
        errors.append("Manifold public derivative schema slice response handoff package manifest status must be candidate")
    if manifest.get("target_repo") != "rusty.manifold":
        errors.append("Manifold public derivative schema slice response handoff package target_repo must be rusty.manifold")
    expected_manifest_statuses = {
        "handoff_acceptance_status": "not_accepted",
        "downstream_implementation_plan_status": "not_created",
        "downstream_implementation_status": "not_created",
        "downstream_response_status": "not_created",
        "downstream_decision_status": "not_decided",
        "downstream_schema_status": "not_created",
        "downstream_route_status": "not_created",
        "downstream_accepted_state_status": "not_created",
        "downstream_audit_status": "not_created",
        "downstream_validation_report_status": "not_created",
        "downstream_hostess_boundary_status": "not_created",
    }
    for key, expected in expected_manifest_statuses.items():
        if manifest.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response handoff package {key} must be {expected}")

    required_sources = {
        "artifact.public_lab_artifact_drift_review",
        "artifact.no_network_prototype_handoff_review",
        "artifact.configured_peer_rehearsal_plan",
        "artifact.manifold_adapter_contract_review",
        "artifact.manifold_contract_intake_request",
        "artifact.private_rehearsal_approval_request",
        "artifact.private_rehearsal_evidence_expectation",
        "artifact.private_rehearsal_public_derivative_expectation",
        "artifact.manifold_public_derivative_schema_request",
        "artifact.manifold_public_derivative_schema_response_expectation",
        "artifact.manifold_public_derivative_schema_implementation_preflight",
        "artifact.manifold_public_derivative_schema_handoff_package",
        "artifact.manifold_public_derivative_schema_slice_response_expectation",
        "artifact.manifold_public_derivative_schema_slice_response_implementation_preflight",
        "artifact.integration_acceptance_scorecard",
    }
    sources = manifest.get("source_chain_artifacts", [])
    observed_sources = {source.get("artifact_id") for source in sources if isinstance(source, dict)}
    missing_sources = sorted(required_sources - observed_sources)
    if missing_sources:
        errors.append(f"Manifold public derivative schema slice response handoff package missing source artifacts: {missing_sources}")
    for source_artifact in sources:
        artifact_id = source_artifact.get("artifact_id", "<unknown>")
        path = source_artifact.get("path", "")
        if not path or path.startswith("/") or "\\" in path:
            errors.append(f"Manifold public derivative schema slice response handoff package source artifact {artifact_id} path must be relative slash form")
        if ".." in Path(path).parts:
            errors.append(f"Manifold public derivative schema slice response handoff package source artifact {artifact_id} path must not escape source root")
        if source_artifact.get("required_for_handoff") is not True:
            errors.append(f"Manifold public derivative schema slice response handoff package source artifact {artifact_id} must be required_for_handoff")

    required_artifact_kinds = {
        "response_schema",
        "decision_event_schema",
        "implementation_plan_descriptor",
        "accepted_source_chain_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "validation_report_fixture",
        "hostess_boundary_descriptor",
        "rollback_descriptor",
    }
    downstream_artifacts = manifest.get("required_downstream_artifacts", [])
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in downstream_artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold public derivative schema slice response handoff package missing artifact kinds: {missing_artifact_kinds}")
    for artifact in downstream_artifacts:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold public derivative schema slice response handoff package artifact {artifact_id} owner must be Manifold-owned")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold public derivative schema slice response handoff package artifact {artifact_id} status must be not_created_by_sidecar")

    required_slots = {
        "slot.public_derivative_schema_slice_response_schema_contract",
        "slot.public_derivative_schema_slice_acceptance_fixture",
        "slot.public_derivative_schema_slice_revision_fixture",
        "slot.public_derivative_schema_slice_rejection_fixture",
        "slot.public_derivative_schema_slice_audit_fixture",
        "slot.accepted_source_chain_mapping_check",
        "slot.accepted_state_mapping_check",
        "slot.validation_report_fixture",
        "slot.hostess_boundary_descriptor_check",
        "slot.privacy_redaction_rejection_check",
        "slot.no_private_endpoint_or_command_content",
    }
    observed_slots = set(manifest.get("required_downstream_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold public derivative schema slice response handoff package missing validation slots: {missing_slots}")

    required_decisions = {
        "accepted_for_manifold_schema_slice",
        "revision_requested",
        "rejected",
    }
    observed_decisions = set(manifest.get("required_downstream_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold public derivative schema slice response handoff package missing response decisions: {missing_decisions}")

    required_rejections = {
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
    }
    observed_rejections = set(manifest.get("required_downstream_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold public derivative schema slice response handoff package missing rejection terms: {missing_rejections}")

    required_revisions = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "accepted_state_mapping_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
        "validation_report_revision",
        "source_chain_revision",
        "package_manifest_revision",
    }
    observed_revisions = set(manifest.get("required_downstream_revision_terms", []))
    missing_revisions = sorted(required_revisions - observed_revisions)
    if missing_revisions:
        errors.append(f"Manifold public derivative schema slice response handoff package missing revision terms: {missing_revisions}")

    required_audit_terms = {
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
    }
    observed_audit_terms = set(manifest.get("required_downstream_audit_terms", []))
    missing_audit_terms = sorted(required_audit_terms - observed_audit_terms)
    if missing_audit_terms:
        errors.append(f"Manifold public derivative schema slice response handoff package missing audit terms: {missing_audit_terms}")

    route = manifest.get("required_route_boundaries", {})
    expected_route = {
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
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response handoff package route boundary {key} must be {expected}")
    if manifest.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold public derivative schema slice response handoff package rollback_policy is invalid")

    hostess = document.get("hostess_boundary_handoff", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "input_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "downstream_descriptor_owner": "rusty.manifold",
        "allowed_action_class": "operator_recovery_request_descriptor",
        "handoff_result": "hostess_prepared_as_boundary_descriptor_only",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response handoff package Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response handoff package local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/package_manifold_public_derivative_schema_slice_response_handoff.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response handoff package missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response handoff package damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_public_derivative_schema_slice_response_handoff_acceptance_and_implementation":
        errors.append("Manifold public derivative schema slice response handoff package future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold public derivative schema slice response handoff package future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response handoff package privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response handoff package public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response handoff package must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response handoff package contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response handoff package check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response handoff package fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response handoff package manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response handoff package pass_count does not match checks")
    if document.get("package_status") == "public_derivative_schema_slice_response_handoff_package_ready" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response handoff package must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response handoff package must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_public_derivative_schema_slice_response_or_operator_decision":
        errors.append("Manifold public derivative schema slice response handoff package next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {
        "ready_for_manifold_submission_intake_response",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response submission intake response expectation has invalid expectation_status")

    source = document.get("source_submission_envelope_expectation", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json":
        errors.append("Manifold public derivative schema slice response submission intake response expectation must point at the submission envelope expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_envelope_expectation.v1":
        errors.append("Manifold public derivative schema slice response submission intake response expectation source envelope expectation schema is invalid")
    if source.get("expectation_status") != "ready_for_manifold_submission_envelope":
        errors.append("Manifold public derivative schema slice response submission intake response expectation source envelope expectation must be ready")
    if source.get("next_gate") != "operator_submission_envelope_or_manifold_repo_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response submission intake response expectation source envelope expectation next_gate is invalid")

    scope = document.get("expectation_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response expectation expectation_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response expectation authority.{key} must be {expected}")

    response = document.get("expected_manifold_intake_response", {})
    if response.get("response_status") != "not_created":
        errors.append("Manifold public derivative schema slice response submission intake response expectation response_status must be not_created")
    if response.get("response_class") != "manifold_owned_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response expectation response_class is invalid")
    if response.get("allowed_response_owner") != "rusty.manifold":
        errors.append("Manifold public derivative schema slice response submission intake response expectation allowed_response_owner must be rusty.manifold")
    required_decisions = {
        "received_for_review",
        "request_submission_revision",
        "reject_submission_envelope",
    }
    missing_decisions = sorted(required_decisions - set(response.get("allowed_decisions", [])))
    if missing_decisions:
        errors.append(f"Manifold public derivative schema slice response submission intake response expectation missing allowed decisions: {missing_decisions}")
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
    missing_fields = sorted(required_fields - set(response.get("required_fields", [])))
    if missing_fields:
        errors.append(f"Manifold public derivative schema slice response submission intake response expectation missing required fields: {missing_fields}")
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
    missing_absences = sorted(required_absences - set(response.get("must_not_contain", [])))
    if missing_absences:
        errors.append(f"Manifold public derivative schema slice response submission intake response expectation missing must_not_contain entries: {missing_absences}")
    if response.get("default_without_response") != "hold":
        errors.append("Manifold public derivative schema slice response submission intake response expectation default_without_response must be hold")
    if response.get("creates_accepted_state") is not False:
        errors.append("Manifold public derivative schema slice response submission intake response expectation creates_accepted_state must be False")
    if response.get("creates_hostess_input") is not False:
        errors.append("Manifold public derivative schema slice response submission intake response expectation creates_hostess_input must be False")

    manifold = document.get("manifold_acceptance_after_response", {})
    expected_manifold = {
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
    for key, expected in expected_manifold.items():
        if manifold.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response expectation manifold_acceptance_after_response.{key} must be {expected}")

    hostess = document.get("hostess_boundary_after_response", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response submission intake response expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response submission intake response expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response submission intake response expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owned_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor":
        errors.append("Manifold public derivative schema slice response submission intake response expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response submission intake response expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response submission intake response expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response submission intake response expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response submission intake response expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response submission intake response expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response submission intake response expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response submission intake response expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response submission intake response expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_manifold_submission_intake_response" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response submission intake response expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Submission intake response" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response submission intake response expectation must preserve response, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "operator_submission_envelope_or_manifold_repo_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response expectation next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("preflight_status") not in {
        "ready_for_manifold_submission_intake_response_implementation_planning",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight has invalid preflight_status")

    source = document.get("source_submission_intake_response_expectation", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight must point at the submission intake response expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight source expectation schema is invalid")
    if source.get("expectation_status") != "ready_for_manifold_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight source expectation must be ready")
    if source.get("next_gate") != "operator_submission_envelope_or_manifold_repo_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight source expectation next_gate is invalid")

    scope = document.get("implementation_preflight_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight implementation_preflight_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight authority.{key} must be {expected}")

    requirements = document.get("manifold_repo_submission_intake_response_requirements", {})
    if requirements.get("slice_class") != "manifold_owned_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight slice_class is invalid")
    if requirements.get("target_repo") != "rusty.manifold":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight target_repo must be rusty.manifold")
    if requirements.get("implementation_status") != "not_created_by_sidecar":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight implementation_status must be not_created_by_sidecar")

    artifacts = requirements.get("required_manifold_owned_artifacts", [])
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
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight missing artifact kinds: {missing_artifact_kinds}")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            errors.append("Manifold public derivative schema slice response submission intake response implementation preflight artifact must be object")
            continue
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight artifact {artifact_id} owner must be Manifold")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight artifact {artifact_id} must be not_created_by_sidecar")

    required_validation_slots = {
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
    }
    missing_slots = sorted(required_validation_slots - set(requirements.get("required_validation_slots", [])))
    if missing_slots:
        errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight missing validation slots: {missing_slots}")

    if set(requirements.get("required_response_decisions", [])) != {
        "received_for_review",
        "request_submission_revision",
        "reject_submission_envelope",
    }:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight response decisions are invalid")

    required_rejection_terms = {
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
    }
    missing_rejections = sorted(required_rejection_terms - set(requirements.get("required_rejection_terms", [])))
    if missing_rejections:
        errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight missing rejection terms: {missing_rejections}")

    required_revision_terms = {
        "submission_envelope_revision",
        "validation_report_revision",
        "redaction_summary_revision",
        "source_chain_digest_revision",
        "hostess_boundary_intent_revision",
        "reason_revision",
    }
    missing_revisions = sorted(required_revision_terms - set(requirements.get("required_revision_terms", [])))
    if missing_revisions:
        errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight missing revision terms: {missing_revisions}")

    required_audit_terms = {
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
    }
    missing_audit_terms = sorted(required_audit_terms - set(requirements.get("required_audit_terms", [])))
    if missing_audit_terms:
        errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight missing audit terms: {missing_audit_terms}")

    route = requirements.get("required_route_boundaries", {})
    expected_route = {
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
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight required_route_boundaries.{key} must be {expected}")
    if requirements.get("rollback_policy") != "manifold_owned_reject_submission_or_request_revision":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight rollback_policy is invalid")

    hostess = document.get("hostess_boundary_preflight", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight hostess_boundary_preflight.{key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_submission_intake_response_implementation_and_audit":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response submission intake response implementation preflight privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight pass_count does not match checks")
    if document.get("preflight_status") == "ready_for_manifold_submission_intake_response_implementation_planning" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response submission intake response implementation preflight must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "submission intake response implementation" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight must preserve implementation, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_submission_intake_response_handoff_or_manifold_repo_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response implementation preflight next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff_package(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("package_status") not in {
        "submission_intake_response_handoff_package_ready",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package has invalid package_status")

    source = document.get("source_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package must point at the submission intake response implementation preflight fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.v1":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package source preflight schema is invalid")
    if source.get("preflight_status") != "ready_for_manifold_submission_intake_response_implementation_planning":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package source preflight must be ready")
    if source.get("next_gate") != "manifold_submission_intake_response_handoff_or_manifold_repo_submission_intake_response":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package source preflight next_gate is invalid")

    scope = document.get("package_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package package_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package authority.{key} must be {expected}")

    manifest = document.get("handoff_manifest", {})
    if manifest.get("status") != "candidate":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package manifest status must be candidate")
    if manifest.get("target_repo") != "rusty.manifold":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package target_repo must be rusty.manifold")
    expected_manifest_statuses = {
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
    for key, expected in expected_manifest_statuses.items():
        if manifest.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package {key} must be {expected}")

    required_sources = {
        "artifact.public_lab_artifact_drift_review",
        "artifact.no_network_prototype_handoff_review",
        "artifact.configured_peer_rehearsal_plan",
        "artifact.manifold_adapter_contract_review",
        "artifact.manifold_contract_intake_request",
        "artifact.private_rehearsal_approval_request",
        "artifact.private_rehearsal_evidence_expectation",
        "artifact.private_rehearsal_public_derivative_expectation",
        "artifact.manifold_public_derivative_schema_request",
        "artifact.manifold_public_derivative_schema_response_expectation",
        "artifact.manifold_public_derivative_schema_implementation_preflight",
        "artifact.manifold_public_derivative_schema_handoff_package",
        "artifact.manifold_public_derivative_schema_slice_response_expectation",
        "artifact.manifold_public_derivative_schema_slice_response_implementation_preflight",
        "artifact.manifold_public_derivative_schema_slice_response_handoff_package",
        "artifact.manifold_public_derivative_schema_slice_response_operator_decision_request",
        "artifact.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation",
        "artifact.manifold_public_derivative_schema_slice_response_submission_envelope_expectation",
        "artifact.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation",
        "artifact.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight",
        "artifact.integration_acceptance_scorecard",
    }
    sources = manifest.get("source_chain_artifacts", [])
    observed_sources = {source.get("artifact_id") for source in sources if isinstance(source, dict)}
    missing_sources = sorted(required_sources - observed_sources)
    if missing_sources:
        errors.append(f"Manifold public derivative schema slice response submission intake response handoff package missing source artifacts: {missing_sources}")
    for source_artifact in sources:
        artifact_id = source_artifact.get("artifact_id", "<unknown>")
        path = source_artifact.get("path", "")
        if not path or path.startswith("/") or "\\" in path:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package source artifact {artifact_id} path must be relative slash form")
        if ".." in Path(path).parts:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package source artifact {artifact_id} path must not escape source root")
        if source_artifact.get("required_for_handoff") is not True:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package source artifact {artifact_id} must be required_for_handoff")

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
    downstream_artifacts = manifest.get("required_downstream_artifacts", [])
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in downstream_artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold public derivative schema slice response submission intake response handoff package missing artifact kinds: {missing_artifact_kinds}")
    for artifact in downstream_artifacts:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package artifact {artifact_id} owner must be Manifold-owned")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package artifact {artifact_id} status must be not_created_by_sidecar")

    required_slots = {
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
    }
    missing_slots = sorted(required_slots - set(manifest.get("required_downstream_validation_slots", [])))
    if missing_slots:
        errors.append(f"Manifold public derivative schema slice response submission intake response handoff package missing validation slots: {missing_slots}")

    if set(manifest.get("required_downstream_decisions", [])) != {
        "received_for_review",
        "request_submission_revision",
        "reject_submission_envelope",
    }:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package response decisions are invalid")

    required_rejections = {
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
    }
    missing_rejections = sorted(required_rejections - set(manifest.get("required_downstream_rejection_terms", [])))
    if missing_rejections:
        errors.append(f"Manifold public derivative schema slice response submission intake response handoff package missing rejection terms: {missing_rejections}")

    required_revisions = {
        "submission_envelope_revision",
        "validation_report_revision",
        "redaction_summary_revision",
        "source_chain_digest_revision",
        "hostess_boundary_intent_revision",
        "reason_revision",
    }
    missing_revisions = sorted(required_revisions - set(manifest.get("required_downstream_revision_terms", [])))
    if missing_revisions:
        errors.append(f"Manifold public derivative schema slice response submission intake response handoff package missing revision terms: {missing_revisions}")

    required_audit_terms = {
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
    }
    missing_audit_terms = sorted(required_audit_terms - set(manifest.get("required_downstream_audit_terms", [])))
    if missing_audit_terms:
        errors.append(f"Manifold public derivative schema slice response submission intake response handoff package missing audit terms: {missing_audit_terms}")

    route = manifest.get("required_route_boundaries", {})
    expected_route = {
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
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package route boundary {key} must be {expected}")
    if manifest.get("rollback_policy") != "manifold_owned_reject_submission_or_request_revision":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package rollback_policy is invalid")

    hostess = document.get("hostess_boundary_handoff", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/package_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_submission_intake_response_handoff_acceptance_and_implementation":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response submission intake response handoff package privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response submission intake response handoff package check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package pass_count does not match checks")
    if document.get("package_status") == "submission_intake_response_handoff_package_ready" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response submission intake response handoff package must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "submission intake response handoff package" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response submission intake response handoff package must preserve handoff, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_repo_submission_intake_response_or_operator_submission_envelope":
        errors.append("Manifold public derivative schema slice response submission intake response handoff package next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_submission_envelope_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {
        "ready_for_manifold_submission_envelope",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response submission envelope expectation has invalid expectation_status")

    source = document.get("source_operator_decision_record_expectation", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json":
        errors.append("Manifold public derivative schema slice response submission envelope expectation must point at the operator decision record expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.v1":
        errors.append("Manifold public derivative schema slice response submission envelope expectation source record expectation schema is invalid")
    if source.get("expectation_status") != "ready_for_operator_decision_record":
        errors.append("Manifold public derivative schema slice response submission envelope expectation source record expectation must be ready")
    if source.get("next_gate") != "operator_decision_record_or_manifold_repo_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response submission envelope expectation source record expectation next_gate is invalid")

    scope = document.get("expectation_scope", {})
    expected_scope = {
        "expectation_class": "manifold_submission_envelope_expectation",
        "source_mode": "synthetic_fixture",
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
        "live_evidence_status": "not_included",
        "adb_status": "not_used",
        "command_status": "no_commands",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission envelope expectation expectation_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "expectation_owner": "rusty.quest.sidecar_mesh",
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
        "sidecar_role": "observer_proposer",
        "proposal_status": "not_accepted",
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission envelope expectation authority.{key} must be {expected}")

    envelope = document.get("expected_submission_envelope", {})
    if envelope.get("envelope_status") != "not_created":
        errors.append("Manifold public derivative schema slice response submission envelope expectation envelope_status must be not_created")
    if envelope.get("envelope_class") != "operator_requested_manifold_review_submission":
        errors.append("Manifold public derivative schema slice response submission envelope expectation envelope_class is invalid")
    if envelope.get("allowed_envelope_owner") != "operator":
        errors.append("Manifold public derivative schema slice response submission envelope expectation allowed_envelope_owner must be operator")
    if envelope.get("target_owner") != "rusty.manifold":
        errors.append("Manifold public derivative schema slice response submission envelope expectation target_owner must be rusty.manifold")
    if envelope.get("submit_decision_required") != "submit_to_manifold_review":
        errors.append("Manifold public derivative schema slice response submission envelope expectation submit_decision_required is invalid")
    if envelope.get("accepted_input_policy") != "sanitized_summary_only":
        errors.append("Manifold public derivative schema slice response submission envelope expectation accepted_input_policy must be sanitized_summary_only")
    required_fields = {
        "submission_envelope_id",
        "operator_decision_record_id",
        "source_request_id",
        "source_handoff_package_id",
        "decision",
        "decision_owner",
        "created_at",
        "reviewed_artifacts",
        "redaction_review_status",
        "source_chain_digest_status",
        "requested_manifold_action",
        "submission_intent",
        "hostess_boundary_intent",
        "reason",
    }
    missing_fields = sorted(required_fields - set(envelope.get("required_fields", [])))
    if missing_fields:
        errors.append(f"Manifold public derivative schema slice response submission envelope expectation missing required fields: {missing_fields}")
    required_absences = {
        "endpoint_values",
        "pairing_material",
        "adb_targets",
        "commands",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "hostess_direct_input",
        "manifold_accepted_state",
    }
    missing_absences = sorted(required_absences - set(envelope.get("must_not_contain", [])))
    if missing_absences:
        errors.append(f"Manifold public derivative schema slice response submission envelope expectation missing must_not_contain entries: {missing_absences}")
    if envelope.get("creates_manifold_state") is not False:
        errors.append("Manifold public derivative schema slice response submission envelope expectation creates_manifold_state must be False")
    if envelope.get("creates_hostess_input") is not False:
        errors.append("Manifold public derivative schema slice response submission envelope expectation creates_hostess_input must be False")

    manifold = document.get("manifold_intake_after_envelope", {})
    expected_manifold = {
        "submission_status": "not_submitted",
        "intake_owner": "rusty.manifold",
        "acceptance_owner": "rusty.manifold",
        "response_owner": "rusty.manifold",
        "accepted_state_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "requires_operator_decision_record": True,
        "requires_submit_decision_value": "submit_to_manifold_review",
        "requires_source_handoff_package": True,
        "requires_redaction_review": True,
        "requires_source_chain_digest": True,
        "sidecar_can_submit_directly": False,
        "sidecar_can_accept": False,
        "sidecar_can_create_state": False,
        "sidecar_can_create_response": False,
    }
    for key, expected in expected_manifold.items():
        if manifold.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission envelope expectation manifold_intake_after_envelope.{key} must be {expected}")

    hostess = document.get("hostess_boundary_after_envelope", {})
    expected_hostess = {
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
        "gate_result": "submission_envelope_expectation_without_hostess_input",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response submission envelope expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response submission envelope expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_slice_response_submission_envelope_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response submission envelope expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response submission envelope expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "operator_submission_envelope_then_manifold_repo_owned_response":
        errors.append("Manifold public derivative schema slice response submission envelope expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor":
        errors.append("Manifold public derivative schema slice response submission envelope expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response submission envelope expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response submission envelope expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response submission envelope expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response submission envelope expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response submission envelope expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response submission envelope expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response submission envelope expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response submission envelope expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_manifold_submission_envelope" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response submission envelope expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Submission envelope" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response submission envelope expectation must preserve submission, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "operator_submission_envelope_or_manifold_repo_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response submission envelope expectation next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("expectation_status") not in {
        "ready_for_operator_decision_record",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response operator decision record expectation has invalid expectation_status")

    source = document.get("source_operator_decision_request", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json":
        errors.append("Manifold public derivative schema slice response operator decision record expectation must point at the operator decision request fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1":
        errors.append("Manifold public derivative schema slice response operator decision record expectation source request schema is invalid")
    if source.get("request_status") != "operator_decision_required":
        errors.append("Manifold public derivative schema slice response operator decision record expectation source request must require operator decision")
    if source.get("next_gate") != "operator_decision_or_manifold_repo_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response operator decision record expectation source request next_gate is invalid")

    scope = document.get("expectation_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision record expectation expectation_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision record expectation authority.{key} must be {expected}")

    record = document.get("expected_operator_decision_record", {})
    if record.get("record_status") != "not_created":
        errors.append("Manifold public derivative schema slice response operator decision record expectation record_status must be not_created")
    if record.get("record_class") != "operator_owned_sidecar_handoff_decision":
        errors.append("Manifold public derivative schema slice response operator decision record expectation record_class is invalid")
    if record.get("allowed_record_owner") != "operator":
        errors.append("Manifold public derivative schema slice response operator decision record expectation allowed_record_owner must be operator")
    required_decisions = {
        "submit_to_manifold_review",
        "hold_for_revision",
        "reject_sidecar_handoff",
    }
    missing_decisions = sorted(required_decisions - set(record.get("allowed_decisions", [])))
    if missing_decisions:
        errors.append(f"Manifold public derivative schema slice response operator decision record expectation missing allowed decisions: {missing_decisions}")
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
    missing_fields = sorted(required_fields - set(record.get("required_fields", [])))
    if missing_fields:
        errors.append(f"Manifold public derivative schema slice response operator decision record expectation missing required fields: {missing_fields}")
    required_absences = {
        "endpoint_values",
        "pairing_material",
        "adb_targets",
        "commands",
        "raw_logs",
        "visual_captures",
        "private_device_ids",
        "hostess_direct_input",
    }
    missing_absences = sorted(required_absences - set(record.get("must_not_contain", [])))
    if missing_absences:
        errors.append(f"Manifold public derivative schema slice response operator decision record expectation missing must_not_contain entries: {missing_absences}")
    if record.get("default_without_record") != "hold":
        errors.append("Manifold public derivative schema slice response operator decision record expectation default_without_record must be hold")
    if record.get("creates_manifold_state") is not False:
        errors.append("Manifold public derivative schema slice response operator decision record expectation creates_manifold_state must be False")
    if record.get("creates_hostess_input") is not False:
        errors.append("Manifold public derivative schema slice response operator decision record expectation creates_hostess_input must be False")

    manifold = document.get("manifold_submission_after_decision", {})
    expected_manifold = {
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
    for key, expected in expected_manifold.items():
        if manifold.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision record expectation manifold_submission_after_decision.{key} must be {expected}")

    hostess = document.get("hostess_boundary_after_decision", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision record expectation Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response operator decision record expectation local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response operator decision record expectation missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response operator decision record expectation damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "operator_decision_record_then_manifold_repo_owned_response":
        errors.append("Manifold public derivative schema slice response operator decision record expectation future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor":
        errors.append("Manifold public derivative schema slice response operator decision record expectation future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response operator decision record expectation privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response operator decision record expectation public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response operator decision record expectation must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response operator decision record expectation contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response operator decision record expectation check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response operator decision record expectation fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response operator decision record expectation manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response operator decision record expectation pass_count does not match checks")
    if document.get("expectation_status") == "ready_for_operator_decision_record" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response operator decision record expectation must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Operator decision record" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response operator decision record expectation must preserve operator, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "operator_decision_record_or_manifold_repo_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response operator decision record expectation next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_operator_decision_request(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("request_status") not in {
        "operator_decision_required",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response operator decision request has invalid request_status")

    source = document.get("source_manifold_public_derivative_schema_slice_response_handoff_package", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json":
        errors.append("Manifold public derivative schema slice response operator decision request must point at the handoff package fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_handoff_package.v1":
        errors.append("Manifold public derivative schema slice response operator decision request source package schema is invalid")
    if source.get("package_status") != "public_derivative_schema_slice_response_handoff_package_ready":
        errors.append("Manifold public derivative schema slice response operator decision request source handoff package must be ready")
    if source.get("next_gate") != "manifold_repo_public_derivative_schema_slice_response_or_operator_decision":
        errors.append("Manifold public derivative schema slice response operator decision request source package next_gate is invalid")

    scope = document.get("decision_request_scope", {})
    expected_scope = {
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
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision request decision_request_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision request authority.{key} must be {expected}")

    requested = document.get("requested_decision", {})
    if requested.get("decision_class") != "submit_handoff_package_to_manifold_or_hold":
        errors.append("Manifold public derivative schema slice response operator decision request decision_class is invalid")
    if requested.get("decision_status") != "not_recorded":
        errors.append("Manifold public derivative schema slice response operator decision request requested_decision.decision_status must be not_recorded")
    required_decisions = {
        "submit_to_manifold_review",
        "hold_for_revision",
        "reject_sidecar_handoff",
    }
    observed_decisions = set(requested.get("allowed_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold public derivative schema slice response operator decision request missing allowed decisions: {missing_decisions}")
    expected_requested = {
        "default_without_decision": "hold",
        "requires_operator_review": True,
        "creates_manifold_state": False,
        "creates_manifold_route": False,
        "creates_hostess_input": False,
        "route_start_allowed": False,
        "live_evidence_allowed": False,
    }
    for key, expected in expected_requested.items():
        if requested.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision request requested_decision.{key} must be {expected}")

    operator_packet = document.get("operator_packet", {})
    if operator_packet.get("packet_status") != "draft":
        errors.append("Manifold public derivative schema slice response operator decision request operator_packet.packet_status must be draft")
    if operator_packet.get("decision_record_status") != "not_created":
        errors.append("Manifold public derivative schema slice response operator decision request decision_record_status must be not_created")
    required_review_items = {
        "source_handoff_package_status",
        "source_chain_summary",
        "manifold_owned_artifact_requirements",
        "validation_summary",
        "privacy_boundary",
        "hostess_boundary_gate",
        "rollback_policy",
    }
    observed_review_items = set(operator_packet.get("required_review_items", []))
    missing_review_items = sorted(required_review_items - observed_review_items)
    if missing_review_items:
        errors.append(f"Manifold public derivative schema slice response operator decision request missing required review items: {missing_review_items}")

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
    observed_rejections = set(operator_packet.get("rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold public derivative schema slice response operator decision request missing rejection terms: {missing_rejections}")

    required_revisions = {
        "handoff_manifest_revision",
        "source_chain_revision",
        "hostess_boundary_revision",
        "validation_evidence_revision",
        "privacy_boundary_revision",
    }
    observed_revisions = set(operator_packet.get("revision_terms", []))
    missing_revisions = sorted(required_revisions - observed_revisions)
    if missing_revisions:
        errors.append(f"Manifold public derivative schema slice response operator decision request missing revision terms: {missing_revisions}")

    manifold_gate = document.get("manifold_submission_gate", {})
    expected_manifold_gate = {
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
    for key, expected in expected_manifold_gate.items():
        if manifold_gate.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision request manifold_submission_gate.{key} must be {expected}")

    hostess = document.get("hostess_boundary_gate", {})
    expected_hostess = {
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
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response operator decision request Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response operator decision request local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response operator decision request missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response operator decision request damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "operator_decision_then_manifold_repo_owned_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response operator decision request future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_explicit_operator_request_descriptor":
        errors.append("Manifold public derivative schema slice response operator decision request future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response operator decision request privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response operator decision request public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response operator decision request must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response operator decision request contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response operator decision request check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response operator decision request fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response operator decision request manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response operator decision request pass_count does not match checks")
    if document.get("request_status") == "operator_decision_required" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response operator decision request must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Operator decision" not in boundary_text or "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response operator decision request must preserve operator, Manifold, and Hostess authority boundaries")
    if document.get("next_gate") != "operator_decision_or_manifold_repo_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response operator decision request next_gate is invalid")
    return errors


def validate_manifold_public_derivative_schema_slice_response_implementation_preflight(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("preflight_status") not in {
        "ready_for_manifold_public_derivative_schema_slice_response_planning",
        "manual_review",
        "blocked",
    }:
        errors.append("Manifold public derivative schema slice response implementation preflight has invalid preflight_status")

    source = document.get("source_manifold_public_derivative_schema_slice_response_expectation", {})
    if source.get("path") != "fixtures/valid/manifold-public-derivative-schema-slice-response-expectation.synthetic.json":
        errors.append("Manifold public derivative schema slice response implementation preflight must point at the slice response expectation fixture")
    if source.get("schema") != "rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_expectation.v1":
        errors.append("Manifold public derivative schema slice response implementation preflight source expectation schema is invalid")
    if source.get("expectation_status") != "ready_for_manifold_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response implementation preflight source expectation must be ready")
    if source.get("next_gate") != "manifold_public_derivative_schema_slice_response_or_operator_decision":
        errors.append("Manifold public derivative schema slice response implementation preflight source expectation next_gate is invalid")

    scope = document.get("implementation_preflight_scope", {})
    expected_scope = {
        "preflight_class": "manifold_repo_public_derivative_schema_slice_response_preflight",
        "source_mode": "synthetic_fixture",
        "target_repo": "rusty.manifold",
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
        "operator_approval_status": "not_recorded",
        "hostess_route_status": "not_created",
        "live_evidence_status": "not_included",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response implementation preflight implementation_preflight_scope.{key} must be {expected}")

    authority = document.get("authority", {})
    expected_authority = {
        "preflight_owner": "rusty.quest.sidecar_mesh",
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
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response implementation preflight authority.{key} must be {expected}")

    requirements = document.get("manifold_repo_slice_response_requirements", {})
    if requirements.get("slice_class") != "manifold_owned_public_derivative_schema_slice_response":
        errors.append("Manifold public derivative schema slice response implementation preflight slice_class is invalid")
    if requirements.get("target_repo") != "rusty.manifold":
        errors.append("Manifold public derivative schema slice response implementation preflight target_repo must be rusty.manifold")
    if requirements.get("implementation_status") != "not_created_by_sidecar":
        errors.append("Manifold public derivative schema slice response implementation preflight implementation_status must be not_created_by_sidecar")

    artifacts = requirements.get("required_manifold_owned_artifacts", [])
    if not artifacts:
        errors.append("Manifold public derivative schema slice response implementation preflight must include required_manifold_owned_artifacts")
    required_artifact_kinds = {
        "response_schema",
        "decision_event_schema",
        "implementation_plan_descriptor",
        "accepted_source_chain_fixture",
        "accepted_state_fixture",
        "audit_fixture",
        "validation_report_fixture",
        "hostess_boundary_descriptor",
        "rollback_descriptor",
    }
    observed_artifact_kinds = {artifact.get("artifact_kind") for artifact in artifacts if isinstance(artifact, dict)}
    missing_artifact_kinds = sorted(required_artifact_kinds - observed_artifact_kinds)
    if missing_artifact_kinds:
        errors.append(f"Manifold public derivative schema slice response implementation preflight missing artifact kinds: {missing_artifact_kinds}")
    for artifact in artifacts:
        artifact_id = artifact.get("artifact_id", "<unknown>")
        if artifact.get("owner") not in {"rusty.manifold", "rusty.manifold.audit"}:
            errors.append(f"Manifold public derivative schema slice response implementation preflight artifact {artifact_id} owner must be Manifold-owned")
        if artifact.get("status") != "not_created_by_sidecar":
            errors.append(f"Manifold public derivative schema slice response implementation preflight artifact {artifact_id} status must be not_created_by_sidecar")

    required_slots = {
        "slot.public_derivative_schema_slice_response_schema_contract",
        "slot.public_derivative_schema_slice_acceptance_fixture",
        "slot.public_derivative_schema_slice_revision_fixture",
        "slot.public_derivative_schema_slice_rejection_fixture",
        "slot.public_derivative_schema_slice_audit_fixture",
        "slot.accepted_source_chain_mapping_check",
        "slot.accepted_state_mapping_check",
        "slot.validation_report_fixture",
        "slot.hostess_boundary_descriptor_check",
        "slot.privacy_redaction_rejection_check",
        "slot.no_private_endpoint_or_command_content",
    }
    observed_slots = set(requirements.get("required_validation_slots", []))
    missing_slots = sorted(required_slots - observed_slots)
    if missing_slots:
        errors.append(f"Manifold public derivative schema slice response implementation preflight missing validation slots: {missing_slots}")

    required_decisions = {
        "accepted_for_manifold_schema_slice",
        "revision_requested",
        "rejected",
    }
    observed_decisions = set(requirements.get("required_response_decisions", []))
    missing_decisions = sorted(required_decisions - observed_decisions)
    if missing_decisions:
        errors.append(f"Manifold public derivative schema slice response implementation preflight missing response decisions: {missing_decisions}")

    required_rejections = {
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
    }
    observed_rejections = set(requirements.get("required_rejection_terms", []))
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"Manifold public derivative schema slice response implementation preflight missing rejection terms: {missing_rejections}")

    required_revisions = {
        "schema_shape_revision",
        "route_semantics_revision",
        "audit_shape_revision",
        "accepted_state_mapping_revision",
        "hostess_boundary_revision",
        "privacy_boundary_revision",
        "validation_report_revision",
        "source_chain_revision",
        "package_manifest_revision",
    }
    observed_revisions = set(requirements.get("required_revision_terms", []))
    missing_revisions = sorted(required_revisions - observed_revisions)
    if missing_revisions:
        errors.append(f"Manifold public derivative schema slice response implementation preflight missing revision terms: {missing_revisions}")

    required_audit_terms = {
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
    }
    observed_audit_terms = set(requirements.get("required_audit_terms", []))
    missing_audit_terms = sorted(required_audit_terms - observed_audit_terms)
    if missing_audit_terms:
        errors.append(f"Manifold public derivative schema slice response implementation preflight missing audit terms: {missing_audit_terms}")

    route = requirements.get("required_route_boundaries", {})
    expected_route = {
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
    }
    for key, expected in expected_route.items():
        if route.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response implementation preflight route boundary {key} must be {expected}")
    if requirements.get("rollback_policy") != "manifold_owned_disable_route_or_reject_source":
        errors.append("Manifold public derivative schema slice response implementation preflight rollback_policy is invalid")

    hostess = document.get("hostess_boundary_preflight", {})
    expected_hostess = {
        "status": "future_lane_not_requested",
        "route_status": "not_created",
        "recovery_request_status": "not_created",
        "device_action_authority": "not_in_sidecar",
        "consumes_only": "manifold_accepted_state_or_operator_request_descriptor",
        "sidecar_direct_input_allowed": False,
        "requires_manifold_accepted_state": True,
        "requires_explicit_operator_request": True,
        "allowed_action_class": "operator_recovery_request_descriptor",
        "preflight_result": "hostess_deferred_until_manifold_slice_response_acceptance",
    }
    for key, expected in expected_hostess.items():
        if hostess.get(key) != expected:
            errors.append(f"Manifold public derivative schema slice response implementation preflight Hostess {key} must be {expected}")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("Manifold public derivative schema slice response implementation preflight local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/prepare_manifold_public_derivative_schema_slice_response_implementation_preflight.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"Manifold public derivative schema slice response implementation preflight missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("Manifold public derivative schema slice response implementation preflight damaged_fixture_policy must be must_fail_validation")
    if validation.get("future_manifold_gate") != "manifold_repo_owns_public_derivative_schema_slice_response_implementation_and_audit":
        errors.append("Manifold public derivative schema slice response implementation preflight future_manifold_gate is invalid")
    if validation.get("future_hostess_gate") != "hostess_route_requires_manifold_state_or_operator_request":
        errors.append("Manifold public derivative schema slice response implementation preflight future_hostess_gate is invalid")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"Manifold public derivative schema slice response implementation preflight privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("Manifold public derivative schema slice response implementation preflight public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("Manifold public derivative schema slice response implementation preflight must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("Manifold public derivative schema slice response implementation preflight contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("check_count") != len(checks):
        errors.append("Manifold public derivative schema slice response implementation preflight check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("Manifold public derivative schema slice response implementation preflight fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("Manifold public derivative schema slice response implementation preflight manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("Manifold public derivative schema slice response implementation preflight pass_count does not match checks")
    if document.get("preflight_status") == "ready_for_manifold_public_derivative_schema_slice_response_planning" and fail_count != 0:
        errors.append("ready Manifold public derivative schema slice response implementation preflight must not have failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("Manifold public derivative schema slice response implementation preflight must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "manifold_public_derivative_schema_slice_response_handoff_or_operator_decision":
        errors.append("Manifold public derivative schema slice response implementation preflight next_gate is invalid")
    return errors


def validate_manifold_adapter_proposal(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    authority = document.get("authority", {})
    if authority.get("source_of_truth") != "rusty.manifold":
        errors.append("adapter proposal source_of_truth must be rusty.manifold")
    if authority.get("accepted_mutation_owner") != "rusty.manifold":
        errors.append("adapter proposal accepted_mutation_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("adapter proposal audit_owner must be rusty.manifold.audit")
    if authority.get("sidecar_role") != "observer_proposer":
        errors.append("adapter proposal sidecar_role must be observer_proposer")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("adapter proposal must remain not_accepted")

    surfaces = document.get("adapter_surfaces", [])
    if not surfaces:
        errors.append("adapter proposal must declare adapter_surfaces")
    for surface in surfaces:
        surface_id = surface.get("surface_id", "<unknown>")
        if surface.get("status") != "proposed":
            errors.append(f"surface {surface_id} must remain proposed")
        if surface.get("acceptance_owner") != "rusty.manifold":
            errors.append(f"surface {surface_id} acceptance_owner must be rusty.manifold")
        if surface.get("rate_class") not in {"low_rate", "control"}:
            errors.append(f"surface {surface_id} has invalid rate_class")

    required_rejections = {
        "stale_observation",
        "untrusted_sidecar",
        "forbidden_authority",
        "redaction_incomplete",
        "operator_approval_missing",
        "endpoint_values_rejected",
        "high_rate_payload_rejected",
        "unsupported_transport",
    }
    observed_rejections = {item.get("rejection_id") for item in document.get("rejection_vocabulary", [])}
    missing_rejections = sorted(required_rejections - observed_rejections)
    if missing_rejections:
        errors.append(f"adapter proposal missing rejection vocabulary: {missing_rejections}")
    return errors


def validate_public_lab_intake_report(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("overall_status") not in {"intake_ready", "manual_review", "intake_blocked"}:
        errors.append("public lab intake report has invalid overall_status")
    redaction = document.get("redaction", {})
    if redaction.get("contains_endpoint_values") is not False:
        errors.append("public lab intake report must not contain endpoint values")
    if redaction.get("contains_commands") is not False:
        errors.append("public lab intake report must not contain commands")
    if redaction.get("contains_pairing_material") is not False:
        errors.append("public lab intake report must not contain pairing material")
    summary = document.get("summary", {})
    if summary.get("artifact_count") != len(document.get("artifacts", [])):
        errors.append("public lab intake artifact_count does not match artifacts")
    if summary.get("failed_count", 0) != 0:
        errors.append("public lab intake report must not have failed artifacts in valid fixtures")
    for artifact in document.get("artifacts", []):
        if artifact.get("status") not in {"passed", "manual_review", "failed"}:
            errors.append(f"artifact {artifact.get('artifact_id', '<unknown>')} has invalid status")
        if artifact.get("observed_status_class") not in {"ready", "blocked", "manual_review", "missing"}:
            errors.append(f"artifact {artifact.get('artifact_id', '<unknown>')} has invalid observed_status_class")
        if artifact.get("expected_status_class") not in {"ready", "blocked", "manual_review"}:
            errors.append(f"artifact {artifact.get('artifact_id', '<unknown>')} has invalid expected_status_class")
    return errors


def validate_public_lab_artifact_drift_review(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if document.get("drift_status") not in {"drift_clear", "manual_review", "drift_detected"}:
        errors.append("public lab artifact drift review has invalid drift_status")

    manifest = document.get("source_manifest", {})
    if manifest.get("path") != "fixtures/valid/public-lab-artifact-intake-manifest.synthetic.json":
        errors.append("public lab artifact drift review manifest path is invalid")
    if manifest.get("schema") != "rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1":
        errors.append("public lab artifact drift review manifest schema is invalid")
    if manifest.get("artifact_count", 0) < 1:
        errors.append("public lab artifact drift review manifest artifact_count must be positive")

    report = document.get("source_report", {})
    if report.get("path") != "fixtures/valid/public-lab-artifact-intake-report.synthetic.json":
        errors.append("public lab artifact drift review report path is invalid")
    if report.get("schema") != "rusty.quest.sidecar.public_lab_artifact_intake_report.v1":
        errors.append("public lab artifact drift review report schema is invalid")
    if report.get("overall_status") != "intake_ready":
        errors.append("public lab artifact drift review report overall_status must be intake_ready")

    policy = document.get("source_access_policy", {})
    if policy.get("source_root_mode") != "cli_supplied":
        errors.append("public lab artifact drift review source_root_mode must be cli_supplied")
    if policy.get("read_declared_public_artifacts") is not True:
        errors.append("public lab artifact drift review must read declared public artifacts")
    if policy.get("copy_raw_artifact") is not False:
        errors.append("public lab artifact drift review copy_raw_artifact must be false")
    if policy.get("execute_source_validation") is not False:
        errors.append("public lab artifact drift review execute_source_validation must be false")
    if policy.get("read_private_evidence") is not False:
        errors.append("public lab artifact drift review read_private_evidence must be false")
    if policy.get("import_private_values") is not False:
        errors.append("public lab artifact drift review import_private_values must be false")

    authority = document.get("authority", {})
    if authority.get("review_owner") != "rusty.quest.sidecar_mesh":
        errors.append("public lab artifact drift review owner must be rusty.quest.sidecar_mesh")
    if authority.get("handoff_acceptance_owner") != "rusty.manifold":
        errors.append("public lab artifact drift review handoff_acceptance_owner must be rusty.manifold")
    if authority.get("audit_owner") != "rusty.manifold.audit":
        errors.append("public lab artifact drift review audit_owner must be rusty.manifold.audit")
    if authority.get("sidecar_role") != "observer_proposer":
        errors.append("public lab artifact drift review sidecar_role must be observer_proposer")
    if authority.get("proposal_status") != "not_accepted":
        errors.append("public lab artifact drift review proposal_status must be not_accepted")

    comparisons = document.get("artifact_comparisons", [])
    if not comparisons:
        errors.append("public lab artifact drift review must include artifact_comparisons")
    drifted = [row for row in comparisons if isinstance(row, dict) and row.get("drift_status") != "drift_clear"]
    expected_blocked = [row for row in comparisons if isinstance(row, dict) and row.get("expected_status_class") == "blocked"]
    for row in comparisons:
        artifact_id = row.get("artifact_id", "<unknown>")
        path = row.get("path", "")
        if not path or path.startswith("/") or "\\" in path:
            errors.append(f"public lab drift artifact {artifact_id} path must be relative slash form")
        if ".." in Path(path).parts:
            errors.append(f"public lab drift artifact {artifact_id} path must not escape source root")
        if row.get("source_path_exists") is not True:
            errors.append(f"public lab drift artifact {artifact_id} source_path_exists must be true")
        if row.get("schema_match") is not True:
            errors.append(f"public lab drift artifact {artifact_id} schema_match must be true")
        if row.get("status_class_match") is not True:
            errors.append(f"public lab drift artifact {artifact_id} status_class_match must be true")
        if row.get("source_status_match") is not True:
            errors.append(f"public lab drift artifact {artifact_id} source_status_match must be true")
        if row.get("result_match") is not True:
            errors.append(f"public lab drift artifact {artifact_id} result_match must be true")
        if row.get("summary_match") is not True:
            errors.append(f"public lab drift artifact {artifact_id} summary_match must be true")

    validation = document.get("validation_evidence", {})
    if validation.get("local_validation_status") != "expected_pass":
        errors.append("public lab artifact drift review local_validation_status must be expected_pass")
    commands = validation.get("required_commands", [])
    for required in [
        "python tools/review_public_lab_artifact_drift.py",
        "python tools/evaluate_integration_acceptance.py",
        "python tools/validate_repo.py",
        "python -m unittest discover -s tests -p test_*.py",
        "git diff --check",
    ]:
        if not any(command.startswith(required) for command in commands):
            errors.append(f"public lab artifact drift review missing validation command: {required}")
    if validation.get("damaged_fixture_policy") != "must_fail_validation":
        errors.append("public lab artifact drift review damaged_fixture_policy must be must_fail_validation")

    privacy = document.get("privacy_boundary", {})
    for key in [
        "contains_endpoint_values",
        "contains_pairing_material",
        "contains_commands",
        "contains_raw_logs",
        "contains_visual_captures",
        "contains_private_device_ids",
    ]:
        if privacy.get(key) is not False:
            errors.append(f"public lab artifact drift review privacy_boundary.{key} must be false")
    if privacy.get("public_fixture_policy") != "synthetic_descriptor_only":
        errors.append("public lab artifact drift review public_fixture_policy must be synthetic_descriptor_only")

    checks = document.get("checks", [])
    if not checks:
        errors.append("public lab artifact drift review must include checks")
    statuses = {check.get("status") for check in checks if isinstance(check, dict)}
    if not statuses <= {"pass", "manual_review", "fail"}:
        errors.append("public lab artifact drift review contains invalid check status")
    summary = document.get("summary", {})
    if summary.get("artifact_count") != len(comparisons):
        errors.append("public lab artifact drift review artifact_count does not match comparisons")
    if summary.get("drifted_artifact_count") != len(drifted):
        errors.append("public lab artifact drift review drifted_artifact_count does not match comparisons")
    if summary.get("expected_blocked_artifact_count") != len(expected_blocked):
        errors.append("public lab artifact drift review expected_blocked_artifact_count does not match comparisons")
    if summary.get("expected_blocked_artifact_count", 0) < 1:
        errors.append("public lab artifact drift review must preserve at least one expected blocked artifact")
    if summary.get("check_count") != len(checks):
        errors.append("public lab artifact drift review check_count does not match checks")
    fail_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "fail")
    manual_review_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "manual_review")
    pass_count = sum(1 for check in checks if isinstance(check, dict) and check.get("status") == "pass")
    if summary.get("fail_count") != fail_count:
        errors.append("public lab artifact drift review fail_count does not match checks")
    if summary.get("manual_review_count") != manual_review_count:
        errors.append("public lab artifact drift review manual_review_count does not match checks")
    if summary.get("pass_count") != pass_count:
        errors.append("public lab artifact drift review pass_count does not match checks")
    if document.get("drift_status") == "drift_clear" and (drifted or fail_count != 0):
        errors.append("drift_clear public lab artifact drift review must not contain drifted artifacts or failed checks")

    boundary_text = " ".join(document.get("authority_boundary", []))
    if "Manifold remains" not in boundary_text or "Hostess remains" not in boundary_text:
        errors.append("public lab artifact drift review must preserve Manifold and Hostess authority boundaries")
    if document.get("next_gate") != "public_lab_drift_clear_before_manifold_handoff_or_contract_intake":
        errors.append("public lab artifact drift review next_gate is invalid")
    return errors


def validate_json_file(path: Path) -> ValidationResult:
    try:
        document = load_json(path)
    except json.JSONDecodeError as exc:
        return ValidationResult(path, False, [f"json parse error: {exc}"])

    if path.name.endswith(".schema.json"):
        errors = validate_schema_file(path, document)
    else:
        errors = validate_fixture(document)
    return ValidationResult(path, not errors, errors)


def validate_repo(root: Path) -> tuple[list[str], list[ValidationResult], list[ValidationResult]]:
    missing = [file for file in REQUIRED_FILES if not (root / file).exists()]
    valid_results: list[ValidationResult] = []
    damaged_results: list[ValidationResult] = []

    for json_path in iter_json_files(root):
        result = validate_json_file(json_path)
        try:
            json_path.relative_to(root / "fixtures" / "damaged")
            damaged_results.append(result)
        except ValueError:
            valid_results.append(result)

    return missing, valid_results, damaged_results


def print_summary(root: Path, missing: list[str], valid: list[ValidationResult], damaged: list[ValidationResult]) -> None:
    valid_failures = [result for result in valid if not result.ok]
    damaged_unexpected_passes = [result for result in damaged if result.ok]
    damaged_expected_failures = [result for result in damaged if not result.ok]

    summary = {
        "repo_root": str(root),
        "status": "ok" if not missing and not valid_failures and not damaged_unexpected_passes else "failed",
        "required_files_missing": missing,
        "valid_json_checked": len(valid),
        "valid_json_failed": len(valid_failures),
        "damaged_json_checked": len(damaged),
        "damaged_expected_failures": len(damaged_expected_failures),
        "damaged_unexpected_passes": len(damaged_unexpected_passes),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))

    for result in valid_failures:
        rel = result.path.relative_to(root)
        for error in result.errors:
            print(f"VALIDATION_ERROR {rel}: {error}", file=sys.stderr)
    for result in damaged_unexpected_passes:
        rel = result.path.relative_to(root)
        print(f"DAMAGED_FIXTURE_UNEXPECTED_PASS {rel}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Repository root to validate.")
    args = parser.parse_args(argv)

    root = Path(args.repo_root).resolve()
    missing, valid, damaged = validate_repo(root)
    print_summary(root, missing, valid, damaged)
    valid_failures = [result for result in valid if not result.ok]
    damaged_unexpected_passes = [result for result in damaged if result.ok]
    return 0 if not missing and not valid_failures and not damaged_unexpected_passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
