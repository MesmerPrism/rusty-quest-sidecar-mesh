# Integration Acceptance Scorecard

## Decision

Use a generated scorecard to decide whether the current private sidecar mesh
contract package is coherent enough for the next data-only slice.

The scorecard is not a live readiness claim. It is a local evidence gate over
schemas, fixtures, and damaged-input expectations.

## Scope

The current scorecard checks:

- public lab artifact intake is `intake_ready`;
- public lab intake contains expected ready and expected blocked artifacts;
- public lab artifact drift review is `drift_clear`;
- public lab artifact drift review preserves the no-copy/no-source-execution
  sanitized boundary;
- Manifold adapter proposal remains `not_accepted`;
- adapter surfaces keep `rusty.manifold` as acceptance owner;
- handoff fixtures require Manifold approval;
- damaged fixtures still fail validation;
- no-network recipe boundaries remain no-network, no-ADB, and no-command;
- no-network recipe review is generated and ready before any runtime prototype;
- no-network prototype emits one advisory observation and run report;
- prototype handoff readiness preserves Manifold intake/audit ownership and
  keeps Hostess as a future operator-recovery lane only;
- no-network prototype handoff review maps future Manifold and Hostess fields
  while proving no live integration route exists.
- configured peer rehearsal plan requires operator approval before route start;
- configured peer rehearsal plan prepares Manifold candidate intake/audit and
  Hostess request descriptors without endpoint, ADB, command, or route
  authority drift.
- Manifold adapter contract review is `contract_ready` while route,
  implementation, and accepted state remain not created;
- Manifold adapter contract review preserves Manifold command/session/audit
  authority and Hostess descriptor-only recovery boundaries.
- Manifold handoff package is `handoff_package_ready` while route, live
  evidence, and accepted state remain not created;
- Manifold handoff package preserves Manifold authority, Hostess boundaries,
  and public-safe privacy flags.
- Manifold contract-intake request is `ready_for_manifold_contract_intake`
  while the Manifold repo is not touched and route, live evidence, and accepted
  state remain not created.
- Manifold contract-intake request preserves Manifold authority, Hostess
  boundaries, and public-safe privacy flags.
- private rehearsal approval request requires an operator decision before
  route start and keeps accepted state not created.
- private rehearsal approval request preserves operator, Manifold, Hostess,
  no-command, no-ADB, endpoint-free, and privacy boundaries.
- Manifold route blueprint is ready for design review while route, accepted
  state, and audit records remain not created.
- Manifold route blueprint preserves Manifold route/session/audit authority
  and leaves Hostess as a future explicit lane only.
- Manifold route design-review request is ready while Manifold repo, route,
  accepted state, audit records, and Hostess route remain untouched.
- Manifold route design-review request preserves Manifold ownership of review
  topics/work items and keeps Hostess gated by Manifold accepted state or an
  explicit operator request.
- Manifold route design response expectation is ready while no response,
  decision, route, accepted state, audit record, or Hostess route is created.
- Manifold route design response expectation preserves Manifold ownership of
  response decisions and keeps Hostess behind Manifold accepted state or an
  explicit operator request.
- Manifold response implementation preflight is ready while no repo, branch,
  response, decision, route, accepted state, audit record, or Hostess route is
  created.
- Manifold response implementation preflight preserves Manifold ownership of
  required implementation artifacts and keeps Hostess deferred.
- Manifold response handoff package is ready while no repo, branch,
  implementation, response, decision, route, accepted state, audit record,
  Hostess route, or live evidence is created.
- Manifold response handoff package preserves Manifold ownership of handoff
  acceptance, downstream implementation, route, audit, accepted state,
  rollback, and Hostess boundary descriptor preparation.
- Hostess boundary descriptor expectation is ready while no Manifold repo,
  Hostess repo, Hostess route, accepted state, operator request, live evidence,
  or route enablement exists.
- Hostess boundary descriptor expectation preserves Manifold source-of-truth
  and enablement authority while keeping Hostess gated away from sidecar-direct
  device actions.
- private rehearsal evidence expectation is ready while operator approval,
  private evidence, public derivatives, Manifold intake, and Hostess routes
  remain not created.
- private rehearsal evidence expectation preserves redaction, Manifold intake
  authority, and the future Hostess operator-recovery boundary.
- private rehearsal public derivative expectation is ready while private
  evidence, public derivative artifact, derivative schema, Manifold intake,
  and Hostess routes remain not created.
- private rehearsal public derivative expectation preserves sanitized summary
  shape, redaction, Manifold authority, and Hostess deferral.
- Manifold public derivative schema request is ready while the Manifold repo,
  schema, route handler, accepted state, audit record, public derivative, and
  Hostess route remain not created.
- Manifold public derivative schema request preserves Manifold ownership of
  schema, route, review, accepted state, audit, runtime/session authority, and
  keeps Hostess behind Manifold accepted state or an explicit operator request.
- Manifold public derivative schema response expectation is ready while no
  Manifold response, decision, schema, route, accepted state, audit record,
  public derivative artifact, or Hostess route is created.
- Manifold public derivative schema response expectation preserves Manifold
  ownership of response, decision, schema, route, audit, accepted state,
  rollback, and runtime/session authority while keeping Hostess behind Manifold
  accepted state or an explicit operator request.
- Manifold public derivative schema implementation preflight is ready while no
  Manifold repo, branch, response, decision, schema, route, accepted state,
  audit record, validation report, public derivative artifact, or Hostess route
  is created.
- Manifold public derivative schema implementation preflight preserves
  Manifold ownership of implementation artifacts, route boundaries, accepted
  state, audit, rollback, validation, and Hostess boundary descriptors while
  keeping Hostess behind Manifold accepted state or an explicit operator
  request.
- Manifold public derivative schema handoff package is ready while no Manifold
  repo, branch, implementation, response, decision, schema, route, accepted
  state, audit record, validation report, public derivative artifact, Hostess
  route, or live evidence is created.
- Manifold public derivative schema handoff package preserves Manifold
  ownership of handoff acceptance, downstream implementation, schema, route,
  audit, accepted state, rollback, validation report, and Hostess boundary
  descriptor preparation.
- Manifold public derivative schema slice response expectation is ready while
  no Manifold response, decision, implementation plan, schema, route, accepted
  state, audit record, validation report, public derivative artifact, Hostess
  route, or live evidence is created.
- Manifold public derivative schema slice response expectation preserves
  Manifold ownership of response, decision, implementation plan, schema, route,
  accepted state, audit, rollback, and redaction review while keeping Hostess
  behind Manifold accepted state or an explicit operator request.
- Manifold public derivative schema slice response implementation preflight is
  ready while no Manifold repo, branch, implementation plan, response,
  decision, schema, route, accepted state, audit record, validation report,
  public derivative artifact, Hostess route, or live evidence is created.
- Manifold public derivative schema slice response implementation preflight
  preserves Manifold ownership of response implementation artifacts, route
  boundaries, source-chain mapping, accepted state, audit, rollback, validation,
  and Hostess boundary descriptors while keeping Hostess behind Manifold
  accepted state or an explicit operator request.
- Manifold public derivative schema slice response handoff package is ready
  while no Manifold repo, branch, implementation plan, response, decision,
  schema, route, accepted state, audit record, validation report, public
  derivative artifact, Hostess route, Hostess input, or live evidence is
  created.
- Manifold public derivative schema slice response handoff package preserves
  Manifold ownership of response implementation artifacts, handoff acceptance,
  response, decision, schema, route, accepted state, audit, rollback,
  validation report, and Hostess boundary descriptor preparation.
- Manifold public derivative schema slice response operator decision request
  is ready while no operator decision, Manifold submission, Manifold response,
  accepted state, audit record, Hostess route, Hostess input, ADB, or command
  action is created.
- Manifold public derivative schema slice response operator decision request
  preserves Manifold submission/acceptance authority and prepares Hostess as a
  future route owner only after Manifold accepted state or a separate explicit
  operator request descriptor.
- Manifold public derivative schema slice response operator decision record
  expectation is ready while no operator decision record, Manifold submission,
  Manifold response, accepted state, audit record, Hostess route, Hostess
  input, ADB, or command action is created.
- Manifold public derivative schema slice response operator decision record
  expectation preserves operator ownership of the future record, Manifold
  submission/acceptance/state/audit authority, and Hostess as a downstream
  route owner that only consumes Manifold accepted state or a separate explicit
  operator request descriptor.
- Manifold public derivative schema slice response submission envelope
  expectation is ready while no submission envelope, Manifold submission,
  Manifold response, accepted state, audit record, Hostess route, Hostess
  input, ADB, or command action is created.
- Manifold public derivative schema slice response submission envelope
  expectation preserves operator ownership of the future envelope, Manifold
  intake/acceptance/state/audit authority, and Hostess as a downstream route
  owner that only consumes Manifold accepted state or a separate explicit
  operator request descriptor.
- Manifold public derivative schema slice response submission intake response
  expectation is ready while no submission envelope, Manifold response,
  accepted state, audit record, validation report, Hostess route, Hostess
  input, ADB, or command action is created.
- Manifold public derivative schema slice response submission intake response
  expectation preserves Manifold ownership of the future response, accepted
  state, validation report, and audit while keeping Hostess as a downstream
  route owner that only consumes Manifold accepted state or a separate explicit
  operator request descriptor.
- Manifold public derivative schema slice response submission intake response
  implementation preflight is ready while no response implementation, route,
  accepted state, audit record, validation report, Hostess input, ADB, or
  command action is created.
- Manifold public derivative schema slice response submission intake response
  implementation preflight preserves Manifold ownership of implementation
  artifacts, route boundaries, accepted state, audit, validation report,
  rollback, and Hostess boundary descriptors while keeping Hostess deferred.

## Non-Scope

The scorecard does not start sidecar agents, open sockets, select endpoints,
run ADB, install APKs, launch apps, collect private evidence, execute Manifold
commands, or prove a live fleet.

## Authority

The scorecard is advisory evidence. Manifold remains the future owner of
acceptance, rejection, revision, leases, and audit records.

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
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
