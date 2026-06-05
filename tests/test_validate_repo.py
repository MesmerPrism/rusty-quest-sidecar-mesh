import unittest
from pathlib import Path

from tools import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidateRepoTests(unittest.TestCase):
    def test_repo_validation_passes_with_damaged_fixture_expected_to_fail(self) -> None:
        missing, valid, damaged = validate_repo.validate_repo(REPO_ROOT)
        self.assertEqual([], missing)
        self.assertEqual([], [result for result in valid if not result.ok])
        self.assertGreaterEqual(len(damaged), 1)
        self.assertEqual([], [result for result in damaged if result.ok])

    def test_command_authority_fixture_is_rejected_for_multiple_reasons(self) -> None:
        damaged_path = REPO_ROOT / "fixtures" / "damaged" / "mesh-handoff-command-authority.damaged.json"
        result = validate_repo.validate_json_file(damaged_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'shell_command'", joined)
        self.assertIn("must require rusty.manifold", joined)
        self.assertIn("must not pre-approve mutation", joined)
        self.assertIn("source_of_truth must be rusty.manifold.audit", joined)

    def test_valid_handoff_requires_manifold_authority(self) -> None:
        handoff_path = REPO_ROOT / "fixtures" / "valid" / "mesh-handoff.synthetic.json"
        result = validate_repo.validate_json_file(handoff_path)
        self.assertTrue(result.ok, result.errors)

    def test_manifold_adapter_proposal_preserves_manifold_authority(self) -> None:
        proposal_path = REPO_ROOT / "fixtures" / "valid" / "manifold-adapter-proposal.synthetic.json"
        result = validate_repo.validate_json_file(proposal_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_adapter_proposal_is_rejected(self) -> None:
        proposal_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-adapter-proposal-sidecar-authority.damaged.json"
        result = validate_repo.validate_json_file(proposal_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("source_of_truth must be rusty.manifold", joined)
        self.assertIn("accepted_mutation_owner must be rusty.manifold", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)

    def test_integration_acceptance_scorecard_passes(self) -> None:
        scorecard_path = REPO_ROOT / "fixtures" / "valid" / "integration-acceptance-scorecard.synthetic.json"
        result = validate_repo.validate_json_file(scorecard_path)
        self.assertTrue(result.ok, result.errors)

    def test_no_network_agent_recipe_passes(self) -> None:
        recipe_path = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-recipe.synthetic.json"
        result = validate_repo.validate_json_file(recipe_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_no_network_agent_recipe_is_rejected(self) -> None:
        recipe_path = REPO_ROOT / "fixtures" / "damaged" / "no-network-agent-recipe-network-adb.damaged.json"
        result = validate_repo.validate_json_file(recipe_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'launch_package'", joined)
        self.assertIn("network_policy must be no_inbound_listener", joined)

    def test_public_lab_artifact_drift_review_passes(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "valid" / "public-lab-artifact-drift-review.synthetic.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_public_lab_artifact_drift_review_is_rejected(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "damaged" / "public-lab-artifact-drift-review-raw-copy.damaged.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("copy_raw_artifact must be false", joined)
        self.assertIn("execute_source_validation must be false", joined)
        self.assertIn("read_private_evidence must be false", joined)
        self.assertIn("handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_no_network_agent_recipe_review_passes(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-recipe-review.synthetic.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_no_network_agent_recipe_review_is_rejected(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "damaged" / "no-network-agent-recipe-review-runtime-authority.damaged.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("source must remain recipe_only", joined)
        self.assertIn("ready no-network recipe review must not have failed checks", joined)
        self.assertIn("must preserve Manifold acceptance authority", joined)
        self.assertIn("next_gate must remain the no-network prototype gate", joined)

    def test_no_network_agent_run_passes(self) -> None:
        run_path = REPO_ROOT / "fixtures" / "valid" / "no-network-agent-run.synthetic.json"
        result = validate_repo.validate_json_file(run_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_no_network_agent_run_is_rejected(self) -> None:
        run_path = REPO_ROOT / "fixtures" / "damaged" / "no-network-agent-run-network-command.damaged.json"
        result = validate_repo.validate_json_file(run_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'shell_command'", joined)
        self.assertIn("network_policy must be no_inbound_listener", joined)
        self.assertIn("acceptance_owner must be rusty.manifold", joined)
        self.assertIn("Hostess handoff readiness must remain future_lane_not_requested", joined)

    def test_no_network_prototype_handoff_review_passes(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "valid" / "no-network-prototype-handoff-review.synthetic.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_no_network_prototype_handoff_review_is_rejected(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "damaged" / "no-network-prototype-handoff-review-sidecar-authority.damaged.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("integration_status.manifold_repo_touched must be false", joined)
        self.assertIn("Manifold authority_owner must be rusty.manifold", joined)
        self.assertIn("Hostess mapping must remain future_lane_not_requested", joined)
        self.assertIn("device_action_authority must be not_in_sidecar", joined)

    def test_configured_peer_rehearsal_plan_passes(self) -> None:
        plan_path = REPO_ROOT / "fixtures" / "valid" / "configured-peer-rehearsal-plan.synthetic.json"
        result = validate_repo.validate_json_file(plan_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_configured_peer_rehearsal_plan_is_rejected(self) -> None:
        plan_path = REPO_ROOT / "fixtures" / "damaged" / "configured-peer-rehearsal-plan-endpoint-command.damaged.json"
        result = validate_repo.validate_json_file(plan_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'shell_command'", joined)
        self.assertIn("must require operator approval", joined)
        self.assertIn("Manifold authority_owner must be rusty.manifold", joined)
        self.assertIn("Hostess readiness must remain future_lane_not_requested", joined)
        self.assertIn("route_started must be false", joined)

    def test_hostess_boundary_descriptor_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "hostess-boundary-descriptor-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_hostess_boundary_descriptor_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "hostess-boundary-descriptor-expectation-direct-sidecar.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source handoff must be ready", joined)
        self.assertIn("expectation_scope.manifold_repo_touch_status must be not_touched", joined)
        self.assertIn("expectation_scope.hostess_repo_touch_status must be not_touched", joined)
        self.assertIn("authority.boundary_descriptor_owner must be rusty.manifold", joined)
        self.assertIn("authority.future_hostess_route_owner must be rusty.hostess", joined)
        self.assertIn("descriptor sidecar_direct_input_allowed must be False", joined)
        self.assertIn("descriptor allows_commands must be False", joined)
        self.assertIn("missing descriptor fields", joined)
        self.assertIn("missing validation slots", joined)
        self.assertIn("manifold_acceptance_gate.handoff_acceptance_status must be not_accepted", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_adapter_contract_review_passes(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "valid" / "manifold-adapter-contract-review.synthetic.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_adapter_contract_review_is_rejected(self) -> None:
        review_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-adapter-contract-review-authority-command.damaged.json"
        result = validate_repo.validate_json_file(review_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("runtime_authority_owner must be rusty.manifold", joined)
        self.assertIn("session_authority_owner must be rusty.manifold", joined)
        self.assertIn("accepted_state_owner must be rusty.manifold", joined)
        self.assertIn("integration_status.manifold_repo_touched must be false", joined)
        self.assertIn("Hostess boundary must remain future_lane_not_requested", joined)
        self.assertIn("missing validation slots", joined)

    def test_manifold_handoff_package_passes(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "valid" / "manifold-handoff-package.synthetic.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_handoff_package_is_rejected(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-handoff-package-live-accepted.damaged.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("route_status must be not_created", joined)
        self.assertIn("accepted_state_status must be not_created", joined)
        self.assertIn("handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("runtime_authority_owner must be rusty.manifold", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_contract_intake_request_passes(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "valid" / "manifold-contract-intake-request.synthetic.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_contract_intake_request_is_rejected(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-contract-intake-request-live-route.damaged.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("repo_touch_status must be not_touched", joined)
        self.assertIn("route_status must be not_created", joined)
        self.assertIn("accepted_state_status must be not_created", joined)
        self.assertIn("intake_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("runtime_authority_owner must be rusty.manifold", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_route_blueprint_passes(self) -> None:
        blueprint_path = REPO_ROOT / "fixtures" / "valid" / "manifold-route-blueprint.synthetic.json"
        result = validate_repo.validate_json_file(blueprint_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_route_blueprint_is_rejected(self) -> None:
        blueprint_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-route-blueprint-sidecar-route.damaged.json"
        result = validate_repo.validate_json_file(blueprint_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("source private approval request must require operator approval", joined)
        self.assertIn("blueprint_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("blueprint_scope.route_status must be not_created", joined)
        self.assertIn("authority.route_implementation_owner must be rusty.manifold", joined)
        self.assertIn("authority.runtime_authority_owner must be rusty.manifold", joined)
        self.assertIn("proposed_manifold_route.route_creation_status must be not_created", joined)
        self.assertIn("audit_owner must be rusty.manifold.audit", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_route_design_review_request_passes(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "valid" / "manifold-route-design-review-request.synthetic.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_route_design_review_request_is_rejected(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-route-design-review-request-sidecar-authority.damaged.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid request_status", joined)
        self.assertIn("source blueprint must be ready", joined)
        self.assertIn("request_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("request_scope.route_status must be not_created", joined)
        self.assertIn("authority.design_review_owner must be rusty.manifold", joined)
        self.assertIn("authority.runtime_authority_owner must be rusty.manifold", joined)
        self.assertIn("review_owner must be rusty.manifold", joined)
        self.assertIn("work item work.sidecar_peer_status_route_handler owner must be rusty.manifold", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_route_design_response_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "manifold-route-design-response-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_route_design_response_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-route-design-response-expectation-sidecar-response.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source design review request must be ready", joined)
        self.assertIn("response_expectation_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("response_expectation_scope.response_status must be not_created", joined)
        self.assertIn("authority.response_owner must be rusty.manifold", joined)
        self.assertIn("authority.decision_owner must be rusty.manifold", joined)
        self.assertIn("response_status must be not_created", joined)
        self.assertIn("allowed_response_owner must be rusty.manifold", joined)
        self.assertIn("missing required fields", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_response_implementation_preflight_passes(self) -> None:
        preflight_path = REPO_ROOT / "fixtures" / "valid" / "manifold-response-implementation-preflight.synthetic.json"
        result = validate_repo.validate_json_file(preflight_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_response_implementation_preflight_is_rejected(self) -> None:
        preflight_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-response-implementation-preflight-sidecar-implementation.damaged.json"
        result = validate_repo.validate_json_file(preflight_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid preflight_status", joined)
        self.assertIn("source expectation must be ready", joined)
        self.assertIn("implementation_preflight_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("implementation_preflight_scope.branch_status must be not_created", joined)
        self.assertIn("authority.implementation_plan_owner must be rusty.manifold", joined)
        self.assertIn("authority.response_owner must be rusty.manifold", joined)
        self.assertIn("implementation_status must be not_created_by_sidecar", joined)
        self.assertIn("owner must be Manifold-owned", joined)
        self.assertIn("missing validation slots", joined)
        self.assertIn("route boundary input_payload_class must be low_rate_advisory_status", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_response_handoff_package_passes(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "valid" / "manifold-response-handoff-package.synthetic.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_response_handoff_package_is_rejected(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-response-handoff-package-sidecar-accepted.damaged.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid package_status", joined)
        self.assertIn("source preflight must be ready", joined)
        self.assertIn("package_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("package_scope.branch_status must be not_created", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.implementation_plan_owner must be rusty.manifold", joined)
        self.assertIn("handoff_acceptance_status must be not_accepted", joined)
        self.assertIn("downstream_implementation_status must be not_created", joined)
        self.assertIn("owner must be Manifold-owned", joined)
        self.assertIn("missing validation slots", joined)
        self.assertIn("route boundary input_payload_class must be low_rate_advisory_status", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_private_rehearsal_approval_request_passes(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-approval-request.synthetic.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_private_rehearsal_approval_request_is_rejected(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "damaged" / "private-rehearsal-approval-request-endpoint-command.damaged.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'shell_command'", joined)
        self.assertIn("has invalid request_status", joined)
        self.assertIn("source peer plan must require operator approval", joined)
        self.assertIn("approval_scope.route_status must be not_started", joined)
        self.assertIn("authority.runtime_authority_owner must be rusty.manifold", joined)
        self.assertIn("approval_decision must be not_recorded", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_private_rehearsal_evidence_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-evidence-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_private_rehearsal_evidence_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "private-rehearsal-evidence-expectation-leaky-live.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source approval request must require operator approval", joined)
        self.assertIn("source Hostess boundary expectation must be ready", joined)
        self.assertIn("evidence_scope.rehearsal_route_status must be not_started", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.hostess_device_action_authority must be not_in_sidecar", joined)
        self.assertIn("private_evidence_requirements.route_start_allowed_by_this_fixture must be False", joined)
        self.assertIn("public_derivative_requirements.contains_private_values must be False", joined)
        self.assertIn("manifold_handoff_expectation.submission_status must be not_submitted", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_private_rehearsal_public_derivative_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "private-rehearsal-public-derivative-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_private_rehearsal_public_derivative_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "private-rehearsal-public-derivative-expectation-leaky-live.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source evidence expectation must be ready", joined)
        self.assertIn("derivative_scope.public_derivative_status must be not_created", joined)
        self.assertIn("derivative_scope.manifold_intake_status must be not_submitted", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.hostess_device_action_authority must be not_in_sidecar", joined)
        self.assertIn("expected_public_derivative.contains_private_values must be False", joined)
        self.assertIn("expected_public_derivative.rejects_direct_hostess_input must be True", joined)
        self.assertIn("manifold_handoff_gate.submission_status must be not_submitted", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_request_passes(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-request.synthetic.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_request_is_rejected(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-request-sidecar-owned.damaged.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid request_status", joined)
        self.assertIn("source expectation must be ready", joined)
        self.assertIn("request_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("request_scope.schema_status must be not_created", joined)
        self.assertIn("authority.schema_owner must be rusty.manifold", joined)
        self.assertIn("authority.hostess_device_action_authority must be not_in_sidecar", joined)
        self.assertIn("proposed_manifold_schema.schema_status must be not_created", joined)
        self.assertIn("proposed_manifold_schema.input_policy must be sanitized_summary_only", joined)
        self.assertIn("proposed_manifold_schema.contains_private_values must be False", joined)
        self.assertIn("proposed_manifold_route.route_status must be not_created", joined)
        self.assertIn("manifold_review_gate.review_status must be not_submitted", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_response_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-response-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_response_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-response-expectation-sidecar-response.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source schema request must be ready", joined)
        self.assertIn("response_expectation_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("response_expectation_scope.response_status must be not_created", joined)
        self.assertIn("response_expectation_scope.schema_status must be not_created", joined)
        self.assertIn("authority.response_owner must be rusty.manifold", joined)
        self.assertIn("authority.schema_owner must be rusty.manifold", joined)
        self.assertIn("authority.redaction_review_owner must be operator", joined)
        self.assertIn("response_status must be not_created", joined)
        self.assertIn("allowed_response_owner must be rusty.manifold", joined)
        self.assertIn("missing required fields", joined)
        self.assertIn("public_derivative_policy is invalid", joined)
        self.assertIn("hostess_input_policy is invalid", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_implementation_preflight_passes(self) -> None:
        preflight_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-implementation-preflight.synthetic.json"
        result = validate_repo.validate_json_file(preflight_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_implementation_preflight_is_rejected(self) -> None:
        preflight_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-implementation-preflight-sidecar-implementation.damaged.json"
        result = validate_repo.validate_json_file(preflight_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid preflight_status", joined)
        self.assertIn("source expectation must be ready", joined)
        self.assertIn("implementation_preflight_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("implementation_preflight_scope.branch_status must be not_created", joined)
        self.assertIn("authority.implementation_plan_owner must be rusty.manifold", joined)
        self.assertIn("authority.schema_owner must be rusty.manifold", joined)
        self.assertIn("implementation_status must be not_created_by_sidecar", joined)
        self.assertIn("owner must be Manifold-owned", joined)
        self.assertIn("missing validation slots", joined)
        self.assertIn("missing revision terms", joined)
        self.assertIn("route boundary input_payload_class must be low_rate_advisory_status", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_handoff_package_passes(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-handoff-package.synthetic.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_handoff_package_is_rejected(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-handoff-package-sidecar-accepted.damaged.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid package_status", joined)
        self.assertIn("source preflight must be ready", joined)
        self.assertIn("package_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("package_scope.schema_status must be not_created", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.schema_owner must be rusty.manifold", joined)
        self.assertIn("authority.redaction_review_owner must be operator", joined)
        self.assertIn("manifest status must be candidate", joined)
        self.assertIn("handoff_acceptance_status must be not_accepted", joined)
        self.assertIn("downstream_schema_status must be not_created", joined)
        self.assertIn("missing source artifacts", joined)
        self.assertIn("missing artifact kinds", joined)
        self.assertIn("owner must be Manifold-owned", joined)
        self.assertIn("missing validation slots", joined)
        self.assertIn("missing revision terms", joined)
        self.assertIn("route boundary input_payload_class must be low_rate_advisory_status", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_slice_response_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_slice_response_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-slice-response-expectation-sidecar-response.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source package must be ready", joined)
        self.assertIn("response_expectation_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("response_expectation_scope.schema_status must be not_created", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.schema_owner must be rusty.manifold", joined)
        self.assertIn("authority.redaction_review_owner must be operator", joined)
        self.assertIn("response_status must be not_created", joined)
        self.assertIn("allowed_response_owner must be rusty.manifold", joined)
        self.assertIn("missing required fields", joined)
        self.assertIn("missing revision terms", joined)
        self.assertIn("public_derivative_policy is invalid", joined)
        self.assertIn("hostess_input_policy is invalid", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_slice_response_implementation_preflight_passes(self) -> None:
        preflight_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json"
        result = validate_repo.validate_json_file(preflight_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_slice_response_implementation_preflight_is_rejected(self) -> None:
        preflight_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-slice-response-implementation-preflight-sidecar-implementation.damaged.json"
        result = validate_repo.validate_json_file(preflight_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid preflight_status", joined)
        self.assertIn("source expectation must be ready", joined)
        self.assertIn("implementation_preflight_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("implementation_preflight_scope.implementation_plan_status must be not_created", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.implementation_plan_owner must be rusty.manifold", joined)
        self.assertIn("authority.response_owner must be rusty.manifold", joined)
        self.assertIn("authority.redaction_review_owner must be operator", joined)
        self.assertIn("implementation_status must be not_created_by_sidecar", joined)
        self.assertIn("owner must be Manifold-owned", joined)
        self.assertIn("missing validation slots", joined)
        self.assertIn("missing revision terms", joined)
        self.assertIn("missing audit terms", joined)
        self.assertIn("route boundary input_payload_class must be low_rate_advisory_status", joined)
        self.assertIn("route boundary creates_accepted_state_by_sidecar must be False", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_slice_response_handoff_package_passes(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_slice_response_handoff_package_is_rejected(self) -> None:
        package_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-slice-response-handoff-package-sidecar-accepted.damaged.json"
        result = validate_repo.validate_json_file(package_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid package_status", joined)
        self.assertIn("source preflight must be ready", joined)
        self.assertIn("package_scope.repo_touch_status must be not_touched", joined)
        self.assertIn("package_scope.implementation_plan_status must be not_created", joined)
        self.assertIn("package_scope.hostess_input_status must be not_created", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.implementation_plan_owner must be rusty.manifold", joined)
        self.assertIn("authority.response_owner must be rusty.manifold", joined)
        self.assertIn("authority.redaction_review_owner must be operator", joined)
        self.assertIn("manifest status must be candidate", joined)
        self.assertIn("handoff_acceptance_status must be not_accepted", joined)
        self.assertIn("downstream_implementation_plan_status must be not_created", joined)
        self.assertIn("downstream_response_status must be not_created", joined)
        self.assertIn("downstream_accepted_state_status must be not_created", joined)
        self.assertIn("missing source artifacts", joined)
        self.assertIn("missing artifact kinds", joined)
        self.assertIn("owner must be Manifold-owned", joined)
        self.assertIn("missing validation slots", joined)
        self.assertIn("missing revision terms", joined)
        self.assertIn("missing audit terms", joined)
        self.assertIn("route boundary input_payload_class must be low_rate_advisory_status", joined)
        self.assertIn("route boundary creates_accepted_state_by_sidecar must be False", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_slice_response_operator_decision_request_passes(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_slice_response_operator_decision_request_is_rejected(self) -> None:
        request_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-slice-response-operator-decision-request-sidecar-decision.damaged.json"
        result = validate_repo.validate_json_file(request_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid request_status", joined)
        self.assertIn("source handoff package must be ready", joined)
        self.assertIn("decision_request_scope.manifold_submission_status must be not_submitted", joined)
        self.assertIn("decision_request_scope.hostess_input_status must be not_created", joined)
        self.assertIn("authority.operator_decision_owner must be operator", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("authority.future_hostess_route_owner must be rusty.hostess", joined)
        self.assertIn("requested_decision.decision_status must be not_recorded", joined)
        self.assertIn("missing required review items", joined)
        self.assertIn("missing rejection terms", joined)
        self.assertIn("manifold_submission_gate.sidecar_can_submit_directly must be False", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-slice-response-operator-decision-record-expectation-sidecar-record.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source request must require operator decision", joined)
        self.assertIn("expectation_scope.operator_decision_record_status must be not_created", joined)
        self.assertIn("expectation_scope.hostess_input_status must be not_created", joined)
        self.assertIn("authority.operator_decision_record_owner must be operator", joined)
        self.assertIn("authority.handoff_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("record_status must be not_created", joined)
        self.assertIn("allowed_record_owner must be operator", joined)
        self.assertIn("missing required fields", joined)
        self.assertIn("manifold_submission_after_decision.sidecar_can_submit_directly must be False", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_slice_response_submission_envelope_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_slice_response_submission_envelope_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-slice-response-submission-envelope-expectation-sidecar-submission.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source record expectation must be ready", joined)
        self.assertIn("expectation_scope.submission_envelope_status must be not_created", joined)
        self.assertIn("expectation_scope.hostess_input_status must be not_created", joined)
        self.assertIn("authority.submission_envelope_owner_after_operator_decision must be operator", joined)
        self.assertIn("authority.submission_acceptance_owner must be rusty.manifold", joined)
        self.assertIn("envelope_status must be not_created", joined)
        self.assertIn("allowed_envelope_owner must be operator", joined)
        self.assertIn("missing required fields", joined)
        self.assertIn("manifold_intake_after_envelope.sidecar_can_submit_directly must be False", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)

    def test_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation_passes(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "valid" / "manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertTrue(result.ok, result.errors)

    def test_damaged_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation_is_rejected(self) -> None:
        expectation_path = REPO_ROOT / "fixtures" / "damaged" / "manifold-public-derivative-schema-slice-response-submission-intake-response-expectation-sidecar-response.damaged.json"
        result = validate_repo.validate_json_file(expectation_path)
        self.assertFalse(result.ok)
        joined = "\n".join(result.errors)
        self.assertIn("forbidden key fragment 'private_endpoint'", joined)
        self.assertIn("forbidden key fragment 'adb_target'", joined)
        self.assertIn("forbidden key fragment 'command_payload'", joined)
        self.assertIn("has invalid expectation_status", joined)
        self.assertIn("source envelope expectation must be ready", joined)
        self.assertIn("expectation_scope.manifold_intake_response_status must be not_created", joined)
        self.assertIn("expectation_scope.hostess_input_status must be not_created", joined)
        self.assertIn("authority.intake_response_owner must be rusty.manifold", joined)
        self.assertIn("authority.accepted_state_owner must be rusty.manifold", joined)
        self.assertIn("response_status must be not_created", joined)
        self.assertIn("allowed_response_owner must be rusty.manifold", joined)
        self.assertIn("missing required fields", joined)
        self.assertIn("manifold_acceptance_after_response.sidecar_can_create_response must be False", joined)
        self.assertIn("Hostess status must be future_lane_not_requested", joined)
        self.assertIn("privacy_boundary.contains_endpoint_values must be false", joined)


if __name__ == "__main__":
    unittest.main()
