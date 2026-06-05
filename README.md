# Rusty Quest Sidecar Mesh

Private integration repo for Quest-hosted Linux sidecar mesh work in the
refactored Rusty stack.

The first concrete implementation profile is Termux on Quest. The repo name is
deliberately broader: Termux is a normal Android app and Linux userland sidecar,
not the architecture authority. This lane belongs under Rusty Quest and hands
off proposals to Rusty Manifold.

## Decision

Start with a private, data-only integration surface:

- `rusty.quest.sidecar.agent_profile.v1`
- `rusty.quest.sidecar.configured_peer_rehearsal_plan.v1`
- `rusty.quest.sidecar.hostess_boundary_descriptor_expectation.v1`
- `rusty.quest.sidecar.integration_acceptance_scorecard.v1`
- `rusty.quest.sidecar.no_network_agent_run.v1`
- `rusty.quest.sidecar.no_network_agent_recipe.v1`
- `rusty.quest.sidecar.no_network_agent_recipe_review.v1`
- `rusty.quest.sidecar.no_network_prototype_handoff_review.v1`
- `rusty.quest.sidecar.observation.v1`
- `rusty.quest.sidecar.mesh_handoff.v1`
- `rusty.quest.sidecar.manifold_adapter_contract_review.v1`
- `rusty.quest.sidecar.manifold_contract_intake_request.v1`
- `rusty.quest.sidecar.manifold_handoff_package.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_handoff_package.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_implementation_preflight.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_response_expectation.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_request.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_expectation.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_handoff_package.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_implementation_preflight.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_operator_decision_request.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_envelope_expectation.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_handoff_package.v1`
- `rusty.quest.sidecar.manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.v1`
- `rusty.quest.sidecar.manifold_response_implementation_preflight.v1`
- `rusty.quest.sidecar.manifold_response_handoff_package.v1`
- `rusty.quest.sidecar.manifold_route_blueprint.v1`
- `rusty.quest.sidecar.manifold_route_design_response_expectation.v1`
- `rusty.quest.sidecar.manifold_route_design_review_request.v1`
- `rusty.quest.sidecar.private_rehearsal_approval_request.v1`
- `rusty.quest.sidecar.private_rehearsal_evidence_expectation.v1`
- `rusty.quest.sidecar.private_rehearsal_public_derivative_expectation.v1`
- `rusty.quest.sidecar.public_lab_artifact_drift_review.v1`
- `rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1`
- `rusty.quest.sidecar.public_lab_artifact_intake_report.v1`
- `rusty.quest.sidecar.manifold_adapter_proposal.v1`
- `rusty.quest.sidecar.validation_scorecard.v1`

These contracts describe what a Quest sidecar can observe or propose. They do
not execute commands, start LAN transport, perform ADB operations, install APKs,
launch apps, or mutate Manifold state.

## Authority Split

- Rusty Manifold owns command/session authority, accepted mutable state,
  leases, revisions, audit, command decisions, and live registry truth.
- Rusty Quest owns Quest platform behavior, sidecar app constraints, local
  lifecycle facts, and headset-hosted operator affordances.
- Sidecar agents observe, summarize, process bounded diagnostics, and propose
  handoffs.
- Central operators or Hostess-style lanes perform recovery and device actions
  through explicit approved routes.

## Current Scope

- Architecture and roadmap docs.
- JSON schemas and synthetic fixtures.
- Public-safe `quest-termux-lab` artifact status intake.
- Generated public-lab artifact drift review fixtures that compare stored
  intake with current sanitized source artifacts without copying raw evidence.
- Manifold adapter proposal fixtures for sidecar observation sources, health
  streams, handoff acceptance, and rejection vocabulary.
- Integration acceptance scorecard fixtures over intake, adapter, handoff, and
  damaged-boundary evidence.
- No-network Termux agent recipe fixtures before any runtime implementation.
- Generated no-network recipe review fixtures before any runtime implementation.
- Offline no-network Termux agent prototype fixtures that write one observation
  file and one run report.
- Generated no-network prototype handoff review fixtures for future Manifold
  intake/audit and Hostess operator-recovery request descriptors.
- Generated configured peer rehearsal plan fixtures for approval-gated,
  endpoint-free, status-only peer rehearsal preparation.
- Generated Manifold adapter contract review fixtures for future
  Manifold-owned peer-status intake, audit, lifecycle, rejection, and
  validation slots.
- Generated Manifold handoff package fixtures that bind the validated artifact
  chain into a future Manifold intake unit.
- Generated Manifold contract-intake request fixtures that prepare a future
  Manifold-owned schema/route slice without touching that repo.
- Generated private rehearsal approval request fixtures that prepare the
  operator decision packet while keeping Hostess and Manifold routes uncreated.
- Generated private rehearsal evidence expectation fixtures that define the
  future operator-approved private evidence, redaction, Manifold intake, and
  Hostess escalation gates without collecting evidence.
- Generated private rehearsal public derivative expectation fixtures that
  define the sanitized derivative contract and Manifold/Hostess gates without
  creating derivative evidence.
- Generated Manifold public derivative schema request fixtures that prepare a
  future Manifold-owned public derivative schema, intake route, review gate,
  audit path, accepted-state mapping, and Hostess escalation boundary without
  touching Manifold or Hostess repos.
- Generated Manifold public derivative schema response expectation fixtures
  that define future Manifold-owned accept/revision/reject response semantics,
  audit/revision terms, and Hostess deferral without creating response,
  schema, route, accepted state, public derivative artifacts, or Hostess input.
- Generated Manifold public derivative schema implementation preflight fixtures
  that enumerate future Manifold-owned schemas, route, accepted-state, audit,
  validation report, and Hostess boundary descriptor requirements without
  touching Manifold or Hostess repos.
- Generated Manifold public derivative schema handoff package fixtures that
  bind the public derivative schema preflight and sidecar evidence chain into a
  future Manifold repo review unit while preserving Hostess as a downstream
  boundary descriptor only.
- Generated Manifold public derivative schema slice response expectation
  fixtures that define the future Manifold-owned response to that handoff
  package while keeping response, decision, schema, route, accepted state,
  audit, validation report, public derivative artifacts, and Hostess input
  uncreated.
- Generated Manifold public derivative schema slice response implementation
  preflight fixtures that enumerate the future Manifold-owned response schema,
  decision event, implementation plan descriptor, accepted source-chain,
  accepted-state, audit, validation report, rollback, and Hostess boundary
  artifacts without touching Manifold or Hostess repos.
- Generated Manifold public derivative schema slice response handoff package
  fixtures that bind the slice response preflight and sidecar evidence chain
  into a future Manifold repo review unit while preserving Hostess as a
  downstream boundary descriptor only.
- Generated Manifold public derivative schema slice response operator decision
  request fixtures that prepare the go/hold/reject packet for submitting the
  handoff package to Manifold while keeping Manifold submission, response,
  accepted state, audit, Hostess route, and Hostess input not created.
- Generated Manifold public derivative schema slice response operator decision
  record expectation fixtures that define the future operator-owned decision
  record shape while preserving Manifold submission/acceptance authority and
  Hostess as a downstream route owner only.
- Generated Manifold public derivative schema slice response submission
  envelope expectation fixtures that define the future operator-owned
  submission envelope shape while preserving Manifold intake authority and
  Hostess as a downstream route owner only.
- Generated Manifold public derivative schema slice response submission intake
  response expectation fixtures that define the future Manifold-owned intake
  response shape while preserving accepted-state/audit authority and Hostess as
  a downstream route owner only.
- Generated Manifold public derivative schema slice response submission intake
  response implementation preflight fixtures that enumerate the future
  Manifold-owned response implementation artifacts, validation slots, route
  boundaries, accepted-state/audit/validation report ownership, and Hostess
  deferral rules without touching Manifold or Hostess repos.
- Generated Manifold public derivative schema slice response submission intake
  response handoff package fixtures that bind the preflight and sidecar
  evidence chain into a future Manifold repo review unit while preserving
  Hostess as a downstream boundary descriptor only.
- Generated Manifold route blueprint fixtures that name candidate
  Manifold-owned request, decision, accepted-state, and audit contracts while
  keeping Hostess as a future explicit lane.
- Generated Manifold route design-review request fixtures that package the
  route blueprint for future Manifold repo review without creating schemas,
  routes, accepted state, audit records, or Hostess lanes.
- Generated Manifold route design response expectation fixtures that define
  the future Manifold-owned response envelope while keeping decisions, routes,
  accepted state, audit records, and Hostess lanes uncreated.
- Generated Manifold response implementation preflight fixtures that enumerate
  the future Manifold-owned artifacts, validation slots, route boundaries, and
  Hostess deferral rules without touching Manifold or Hostess repos.
- Generated Manifold response handoff package fixtures that bind the response
  preflight and sidecar evidence chain into a future Manifold repo slice while
  preserving Hostess as a downstream boundary descriptor.
- Generated Hostess boundary descriptor expectation fixtures that prepare a
  future Manifold-enabled Hostess boundary while keeping Hostess routes,
  accepted state, operator requests, endpoint values, ADB, and commands absent.
- A local validation tool that enforces authority and privacy boundaries.
- Damaged fixtures that prove the validator rejects command-like sidecar data.

## Non-Scope

- Live Quest or ADB work.
- Termux service implementation.
- LAN discovery, sockets, SSH, VNC, or remote desktop control.
- Cross-headset ADB.
- Install, launch, recovery, or command execution.
- Hostess, Studio, Makepad, PMD, Polar, controller, or public Rusty-XR runtime
  changes.

## Validation

```powershell
python tools\import_public_lab_status.py --manifest fixtures\valid\public-lab-artifact-intake-manifest.synthetic.json --source-root ..\quest-termux-lab --now 2026-06-04T21:41:00Z --output fixtures\valid\public-lab-artifact-intake-report.synthetic.json
python tools\review_public_lab_artifact_drift.py --manifest fixtures\valid\public-lab-artifact-intake-manifest.synthetic.json --report fixtures\valid\public-lab-artifact-intake-report.synthetic.json --source-root ..\quest-termux-lab --now 2026-06-04T21:43:00Z --output fixtures\valid\public-lab-artifact-drift-review.synthetic.json
python tools\review_no_network_recipe.py --recipe fixtures\valid\no-network-agent-recipe.synthetic.json --now 2026-06-04T22:05:00Z --output fixtures\valid\no-network-agent-recipe-review.synthetic.json
python tools\run_no_network_agent.py --recipe fixtures\valid\no-network-agent-recipe.synthetic.json --review fixtures\valid\no-network-agent-recipe-review.synthetic.json --now 2026-06-04T22:12:00Z --sequence 2 --observation-output fixtures\valid\no-network-agent-observation.synthetic.json --report-output fixtures\valid\no-network-agent-run.synthetic.json
python tools\review_no_network_prototype_handoff.py --observation fixtures\valid\no-network-agent-observation.synthetic.json --run fixtures\valid\no-network-agent-run.synthetic.json --now 2026-06-04T22:18:00Z --output fixtures\valid\no-network-prototype-handoff-review.synthetic.json
python tools\plan_configured_peer_rehearsal.py --handoff-review fixtures\valid\no-network-prototype-handoff-review.synthetic.json --now 2026-06-04T22:25:00Z --output fixtures\valid\configured-peer-rehearsal-plan.synthetic.json
python tools\review_manifold_adapter_contract.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --now 2026-06-04T22:32:00Z --output fixtures\valid\manifold-adapter-contract-review.synthetic.json
python tools\package_manifold_handoff.py --contract-review fixtures\valid\manifold-adapter-contract-review.synthetic.json --now 2026-06-04T22:40:00Z --output fixtures\valid\manifold-handoff-package.synthetic.json
python tools\prepare_manifold_contract_intake.py --handoff-package fixtures\valid\manifold-handoff-package.synthetic.json --now 2026-06-04T22:48:00Z --output fixtures\valid\manifold-contract-intake-request.synthetic.json
python tools\prepare_private_rehearsal_approval.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --now 2026-06-04T22:56:00Z --output fixtures\valid\private-rehearsal-approval-request.synthetic.json
python tools\prepare_manifold_route_blueprint.py --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --private-approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --now 2026-06-04T23:04:00Z --output fixtures\valid\manifold-route-blueprint.synthetic.json
python tools\prepare_manifold_route_design_review.py --route-blueprint fixtures\valid\manifold-route-blueprint.synthetic.json --now 2026-06-04T23:12:00Z --output fixtures\valid\manifold-route-design-review-request.synthetic.json
python tools\prepare_manifold_route_design_response_expectation.py --design-review-request fixtures\valid\manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures\valid\manifold-route-design-response-expectation.synthetic.json
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\package_manifold_response_handoff.py --preflight fixtures\valid\manifold-response-implementation-preflight.synthetic.json --now 2026-06-04T23:36:00Z --output fixtures\valid\manifold-response-handoff-package.synthetic.json
python tools\prepare_hostess_boundary_descriptor_expectation.py --response-handoff fixtures\valid\manifold-response-handoff-package.synthetic.json --now 2026-06-04T23:44:00Z --output fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json
python tools\prepare_private_rehearsal_evidence_expectation.py --approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --hostess-expectation fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json --now 2026-06-04T23:52:00Z --output fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json
python tools\prepare_private_rehearsal_public_derivative_expectation.py --evidence-expectation fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json --now 2026-06-05T00:00:00Z --output fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_request.py --public-derivative-expectation fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json --now 2026-06-05T00:08:00Z --output fixtures\valid\manifold-public-derivative-schema-request.synthetic.json
python tools\prepare_manifold_public_derivative_schema_response_expectation.py --schema-request fixtures\valid\manifold-public-derivative-schema-request.synthetic.json --now 2026-06-05T00:16:00Z --output fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_implementation_preflight.py --response-expectation fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json --now 2026-06-05T00:24:00Z --output fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json
python tools\package_manifold_public_derivative_schema_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json --now 2026-06-05T00:32:00Z --output fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_expectation.py --handoff-package fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json --now 2026-06-05T00:40:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-expectation.synthetic.json --now 2026-06-05T00:48:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json
python tools\package_manifold_public_derivative_schema_slice_response_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json --now 2026-06-05T00:56:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.py --handoff-package fixtures\valid\manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json --now 2026-06-05T01:04:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.py --decision-request fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json --now 2026-06-05T01:12:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_submission_envelope_expectation.py --record-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json --now 2026-06-05T01:20:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.py --envelope-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json --now 2026-06-05T01:28:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.py --intake-response-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json --now 2026-06-05T01:36:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json
python tools\package_manifold_public_derivative_schema_slice_response_submission_intake_response_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json --now 2026-06-05T01:44:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Next Slice

After the generated submission intake response handoff package remains stable,
the next safe data-only step is a real Manifold-repo-owned submission intake
response slice or an operator submission envelope path that Manifold can
accept, reject, or revise. Hostess integration stays prepared, but it should
only consume Manifold accepted state or a separate explicit operator request
descriptor.
