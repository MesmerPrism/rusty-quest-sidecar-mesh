# Integration Roadmap

## Slice 1: Private Contract Scaffold

Status: implemented.

Deliverables:

- sidecar profile, observation, handoff, and scorecard schemas;
- synthetic valid fixtures;
- damaged boundary fixture;
- repository validator.

Validation:

```powershell
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 2: Public Lab Artifact Intake

Status: implemented.

Import only sanitized, public-safe derivatives from `quest-termux-lab`:

- package readiness status;
- peer-mesh scorecard summary;
- review-bundle status;
- file-drop dry-run status;
- private-evidence placeholder status.

Do not import raw endpoints, logs, screenshots, serials, package IDs, pairing
state, or command records.

Output:

- one `mesh_handoff` fixture that references imported status summaries;
- one scorecard that records which public lab gates are ready or blocked.

Validation:

```powershell
python tools\import_public_lab_status.py --manifest fixtures\valid\public-lab-artifact-intake-manifest.synthetic.json --source-root ..\quest-termux-lab --now 2026-06-04T21:41:00Z --output fixtures\valid\public-lab-artifact-intake-report.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 2A: Public Lab Artifact Drift Review

Status: implemented.

After importing public-safe `quest-termux-lab` status:

- regenerate a sanitized source-derived report from the declared manifest;
- compare it with the stored sidecar intake report;
- prove expected blocked lanes remain expected blocked;
- preserve no raw artifact copy, no source validation execution, no private
  evidence read, no endpoints, no ADB, and no commands.

Validation:

```powershell
python tools\review_public_lab_artifact_drift.py --manifest fixtures\valid\public-lab-artifact-intake-manifest.synthetic.json --report fixtures\valid\public-lab-artifact-intake-report.synthetic.json --source-root ..\quest-termux-lab --now 2026-06-04T21:43:00Z --output fixtures\valid\public-lab-artifact-drift-review.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 3: Manifold Adapter Proposal

Status: implemented.

Design the future Manifold surfaces without implementing them:

- sidecar observation source descriptor;
- sidecar health stream descriptor;
- handoff acceptance command descriptor;
- rejection vocabulary for stale, untrusted, forbidden-authority, and
  redaction-incomplete cases.

Keep this as docs and fixtures until a Manifold authority route exists.

Validation:

```powershell
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 4: Integration Acceptance Scorecard

Status: implemented.

Generate a local scorecard over:

- public lab intake status;
- expected ready and expected blocked artifact lanes;
- Manifold adapter proposal ownership;
- sidecar handoff approval/audit boundaries;
- damaged fixture failures.

Validation:

```powershell
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 5: No-Network Agent Recipe

Status: implemented.

Describe the future Termux agent prototype without writing runtime code:

- no inbound listener;
- no outbound transport;
- no ADB;
- no commands;
- observation-file output only;
- Manifold remains acceptance/audit owner.

Validation:

```powershell
python tools\validate_repo.py --repo-root .
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 6: No-Network Agent Recipe Review

Status: implemented.

Generate review evidence over the no-network recipe before writing runtime
code:

- Termux/Python profile remains recipe-only;
- Manifold remains acceptance and audit owner;
- network, outbound transport, ADB, and commands remain disabled;
- local file outputs remain relative;
- emissions remain low-rate sidecar observations;
- forbidden surfaces and validation slots are explicit.

Validation:

```powershell
python tools\review_no_network_recipe.py --recipe fixtures\valid\no-network-agent-recipe.synthetic.json --now 2026-06-04T22:05:00Z --output fixtures\valid\no-network-agent-recipe-review.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 7: Private No-Network Termux Agent Prototype

Status: implemented.

Only after the contract, adapter proposal, acceptance scorecard, and recipe
review are stable:

- run a local Termux Python process that emits an `observation` JSON file;
- keep output in app-private or operator-selected storage;
- do not open a listener;
- do not start LAN discovery;
- do not use ADB;
- write a run report that records future Manifold intake/audit ownership and
  Hostess operator-recovery routing without touching either repo.

Validation:

```powershell
python tools\run_no_network_agent.py --recipe fixtures\valid\no-network-agent-recipe.synthetic.json --review fixtures\valid\no-network-agent-recipe-review.synthetic.json --now 2026-06-04T22:12:00Z --sequence 2 --observation-output fixtures\valid\no-network-agent-observation.synthetic.json --report-output fixtures\valid\no-network-agent-run.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 8: No-Network Prototype Handoff Review

Status: implemented.

Only after the offline prototype is stable:

- map the generated observation to proposed Manifold intake fields;
- map the run report to future Manifold audit evidence fields;
- map Hostess operator-recovery needs as request descriptors only;
- keep Hostess and Manifold repos untouched until an explicit integration
  slice.

Validation:

```powershell
python tools\review_no_network_prototype_handoff.py --observation fixtures\valid\no-network-agent-observation.synthetic.json --run fixtures\valid\no-network-agent-run.synthetic.json --now 2026-06-04T22:18:00Z --output fixtures\valid\no-network-prototype-handoff-review.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 9: Configured Peer Rehearsal Plan

Status: implemented.

Only after the no-network prototype handoff review is stable:

- generate a descriptor-only plan for a configured status peer rehearsal;
- require operator approval before route start;
- keep endpoint-bearing material in private evidence only;
- keep the fixture synthetic and endpoint-free;
- map Manifold candidate intake/audit fields;
- map Hostess operator-recovery request descriptors without creating a Hostess
  route.

Validation:

```powershell
python tools\plan_configured_peer_rehearsal.py --handoff-review fixtures\valid\no-network-prototype-handoff-review.synthetic.json --now 2026-06-04T22:25:00Z --output fixtures\valid\configured-peer-rehearsal-plan.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 10: Manifold Adapter Contract Review

Status: implemented.

Only after the configured peer rehearsal plan is stable:

- generate a descriptor-only review of the future Manifold adapter contract;
- name peer status source, intake, and audit surfaces;
- require Manifold ownership of runtime authority, session authority, accepted
  state, and audit;
- keep Hostess as a descriptor-only future operator-recovery boundary;
- record rejection terms, lifecycle states, rollback owner, and validation
  slots.

Validation:

```powershell
python tools\review_manifold_adapter_contract.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --now 2026-06-04T22:32:00Z --output fixtures\valid\manifold-adapter-contract-review.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 11: Manifold Handoff Package

Status: implemented.

Only after the Manifold adapter contract review is stable:

- generate a descriptor-only handoff package;
- bind public lab intake, no-network recipe/prototype, handoff review,
  configured peer rehearsal plan, contract review, and acceptance scorecard;
- name future Manifold target surfaces and validation gates;
- keep route, live evidence, accepted state, endpoint values, and Hostess
  device action authority out of the package.

Validation:

```powershell
python tools\package_manifold_handoff.py --contract-review fixtures\valid\manifold-adapter-contract-review.synthetic.json --now 2026-06-04T22:40:00Z --output fixtures\valid\manifold-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 12: Manifold Contract Intake Request

Status: implemented.

Only after the Manifold handoff package is stable:

- generate a descriptor-only Manifold contract-intake request;
- point at the validated handoff package;
- name candidate Manifold intake surfaces, validation slots, and rejection
  terms;
- keep the Manifold repo untouched and route, live evidence, accepted state,
  endpoint values, and Hostess device action authority out of the request.

Validation:

```powershell
python tools\prepare_manifold_contract_intake.py --handoff-package fixtures\valid\manifold-handoff-package.synthetic.json --now 2026-06-04T22:48:00Z --output fixtures\valid\manifold-contract-intake-request.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 13: Private Rehearsal Approval Request

Status: implemented.

Only after the Manifold contract-intake request is stable:

- generate a descriptor-only private rehearsal approval request;
- point at the configured peer rehearsal plan and Manifold contract-intake
  request;
- record required private inputs, public derivatives, and rejection terms;
- keep operator approval unrecorded until a later explicit decision;
- keep Hostess routes, Manifold routes, accepted state, live evidence,
  endpoint values, ADB, and commands out of the request.

Validation:

```powershell
python tools\prepare_private_rehearsal_approval.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --now 2026-06-04T22:56:00Z --output fixtures\valid\private-rehearsal-approval-request.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 14: Manifold Route Blueprint

Status: implemented.

Only after the private rehearsal approval request is stable:

- generate a descriptor-only blueprint for a future Manifold peer-status route;
- name candidate Manifold request, decision-event, accepted-state, and audit
  contracts;
- keep the Manifold repo untouched and route, accepted state, audit records,
  live evidence, endpoint values, ADB, and commands out of the blueprint;
- keep Hostess as a future explicit operator/recovery lane that requires
  Manifold accepted state or an operator request.

Validation:

```powershell
python tools\prepare_manifold_route_blueprint.py --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --private-approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --now 2026-06-04T23:04:00Z --output fixtures\valid\manifold-route-blueprint.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 15: Manifold Route Design Review Request

Status: implemented.

Only after the Manifold route blueprint is stable:

- generate a descriptor-only request for future Manifold repo design review;
- name required Manifold review topics and proposed Manifold-owned work items;
- keep all schemas, route handlers, accepted-state shapes, audit records,
  Hostess boundary descriptors, live evidence, endpoint values, ADB, and
  commands not created;
- keep Hostess integration gated by Manifold accepted state or an explicit
  operator request.

Validation:

```powershell
python tools\prepare_manifold_route_design_review.py --route-blueprint fixtures\valid\manifold-route-blueprint.synthetic.json --now 2026-06-04T23:12:00Z --output fixtures\valid\manifold-route-design-review-request.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 16: Manifold Route Design Response Expectation

Status: implemented.

Only after the Manifold route design-review request is stable:

- generate a descriptor-only expectation for a future Manifold-owned response;
- require the future response to decide `accepted_for_manifold_slice`,
  `revision_requested`, or `rejected`;
- require response owner, decision owner, revision, schema, route,
  accepted-state, audit, rejection, revision, Hostess boundary, and privacy
  fields;
- keep the Manifold response, route, accepted state, audit record, Hostess
  route, live evidence, endpoint values, ADB, and commands not created;
- keep Hostess integration gated by Manifold accepted state or an explicit
  operator request.

Validation:

```powershell
python tools\prepare_manifold_route_design_response_expectation.py --design-review-request fixtures\valid\manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures\valid\manifold-route-design-response-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17: Manifold Response Implementation Preflight

Status: implemented.

Only after the Manifold route design response expectation is stable:

- generate a descriptor-only preflight for the future Manifold repo response
  slice;
- enumerate required Manifold-owned artifacts for response schema, route
  handler, decision-event fixture, accepted-state fixture, audit fixture, and
  Hostess boundary descriptor;
- name required validation slots, response decisions, rejection terms, route
  boundaries, and rollback policy;
- keep the Manifold repo, branch, response, route, accepted state, audit
  record, Hostess route, live evidence, endpoint values, ADB, and commands not
  created;
- keep Hostess integration deferred until Manifold accepted state or explicit
  operator request.

Validation:

```powershell
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17A: Manifold Response Handoff Package

Status: implemented.

Only after the Manifold response implementation preflight is stable:

- generate a descriptor-only handoff package for the future Manifold repo
  response slice;
- bind the response preflight and sidecar evidence chain into a package a
  Manifold repo agent can consume later;
- carry required Manifold-owned artifacts, validation slots, decisions,
  rejection terms, route boundaries, and rollback policy forward;
- keep the Manifold repo, branch, implementation, response, decision, route,
  accepted state, audit record, Hostess route, live evidence, endpoint values,
  ADB, and commands not created;
- prepare Hostess integration only as a future boundary descriptor owned by
  Manifold after accepted state or an explicit operator request.

Validation:

```powershell
python tools\package_manifold_response_handoff.py --preflight fixtures\valid\manifold-response-implementation-preflight.synthetic.json --now 2026-06-04T23:36:00Z --output fixtures\valid\manifold-response-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17B: Hostess Boundary Descriptor Expectation

Status: implemented.

Only after the Manifold response handoff package is stable:

- generate a descriptor-only expectation for the future Hostess boundary
  descriptor;
- keep Manifold as source of truth, accepted-state, audit, and Hostess route
  enablement authority;
- keep Hostess as a future route owner only after Manifold accepted state or an
  explicit operator request;
- require read-only status or operator-recovery descriptors, not direct sidecar
  device-action input;
- keep Manifold repo touch, Hostess repo touch, Hostess routes, accepted state,
  audit records, operator requests, live evidence, endpoint values, ADB, and
  commands not created.

Validation:

```powershell
python tools\prepare_hostess_boundary_descriptor_expectation.py --response-handoff fixtures\valid\manifold-response-handoff-package.synthetic.json --now 2026-06-04T23:44:00Z --output fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17C: Private Rehearsal Evidence Expectation

Status: implemented.

Only after the private approval request and Hostess boundary descriptor
expectation are stable:

- define what a future operator-approved private rehearsal evidence pass may
  collect;
- require private storage, duration bounds, cleanup, and redaction review;
- require sanitized public derivatives before Manifold intake;
- keep Manifold as intake acceptance, accepted-state, runtime/session, and
  audit authority;
- keep Hostess as a future operator-recovery lane that requires Manifold
  accepted state or an explicit operator request;
- keep operator approval, private evidence, public derivatives, Manifold
  submission, Hostess routes, live evidence, endpoint values, ADB, and commands
  not created.

Validation:

```powershell
python tools\prepare_private_rehearsal_evidence_expectation.py --approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --hostess-expectation fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json --now 2026-06-04T23:52:00Z --output fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17D: Private Rehearsal Public Derivative Expectation

Status: implemented.

Only after the private rehearsal evidence expectation is stable:

- define the sanitized public derivative contract that a future private
  rehearsal evidence pass may produce;
- require sanitized summary-only fields and required redaction results;
- reject endpoint values, pairing material, ADB, command text, raw logs,
  visual captures, package identifiers, and private device identifiers;
- keep Manifold as handoff acceptance, accepted-state, runtime/session, and
  audit authority;
- keep Hostess as a future operator-recovery lane that requires Manifold
  accepted state or an explicit operator request;
- keep operator approval, private evidence, public derivatives, derivative
  schema, Manifold submission, Hostess routes, live evidence, endpoint values,
  ADB, and commands not created.

Validation:

```powershell
python tools\prepare_private_rehearsal_public_derivative_expectation.py --evidence-expectation fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json --now 2026-06-05T00:00:00Z --output fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17E: Manifold Public Derivative Schema Request

Status: implemented.

Only after the private rehearsal public derivative expectation is stable:

- package a request for a future Manifold-owned public derivative schema and
  intake route;
- keep schema creation, route handlers, accepted state, audit records, public
  derivative artifacts, private evidence, operator approval, and repo mutation
  not created;
- require Manifold ownership for schema, route, review, runtime/session,
  accepted state, audit, and handoff acceptance;
- require a sanitized summary-only payload shape and explicit rejection terms
  for endpoint values, commands, ADB, stale peer status, untrusted sidecars,
  incomplete redaction, and incomplete cleanup;
- keep Hostess as a future downstream boundary that requires Manifold accepted
  state or an explicit operator request.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_request.py --public-derivative-expectation fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json --now 2026-06-05T00:08:00Z --output fixtures\valid\manifold-public-derivative-schema-request.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17F: Manifold Public Derivative Schema Response Expectation

Status: implemented.

Only after the Manifold public derivative schema request is stable:

- define the expected future Manifold-owned response envelope for accepting,
  requesting revisions to, or rejecting the public derivative schema request;
- keep response, decision, schema, route, accepted state, audit records, public
  derivative artifacts, operator approval, private evidence, Hostess routes,
  and repo mutation not created;
- require Manifold ownership for response, decision, schema, route,
  runtime/session, accepted state, audit, rollback, and handoff acceptance;
- require explicit rejection, revision, audit, validation, privacy, and
  redaction terms before a future Manifold repo slice can accept anything;
- keep Hostess as a future downstream boundary that requires Manifold accepted
  state or an explicit operator request.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_response_expectation.py --schema-request fixtures\valid\manifold-public-derivative-schema-request.synthetic.json --now 2026-06-05T00:16:00Z --output fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17G: Manifold Public Derivative Schema Implementation Preflight

Status: implemented.

Only after the Manifold public derivative schema response expectation is
stable:

- generate a descriptor-only preflight for the future Manifold repo public
  derivative schema implementation slice;
- enumerate required Manifold-owned artifacts for response schema, input
  schema, route handler, decision-event fixture, accepted-state fixture, audit
  fixture, validation report fixture, and Hostess boundary descriptor;
- name required validation slots, response decisions, rejection terms,
  revision terms, route boundaries, and rollback policy;
- keep the Manifold repo, branch, response, decision, schema, route, accepted
  state, audit record, validation report, public derivative artifact, Hostess
  route, live evidence, endpoint values, ADB, and commands not created;
- keep Hostess integration deferred until Manifold accepted state or explicit
  operator request.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_implementation_preflight.py --response-expectation fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json --now 2026-06-05T00:24:00Z --output fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17H: Manifold Public Derivative Schema Handoff Package

Status: implemented.

Only after the Manifold public derivative schema implementation preflight is
stable:

- generate a descriptor-only handoff package for the future Manifold repo
  public derivative schema slice;
- bind public-lab drift evidence, no-network handoff review, configured peer
  rehearsal plan, Manifold contract intake, private approval/evidence/public
  derivative expectations, public derivative schema request, response
  expectation, implementation preflight, and acceptance scorecard into one
  package;
- carry required Manifold-owned artifacts, validation slots, response
  decisions, rejection terms, revision terms, route boundaries, and rollback
  policy forward;
- keep the Manifold repo, branch, implementation, response, decision, schema,
  route, accepted state, audit record, validation report, public derivative
  artifact, Hostess route, live evidence, endpoint values, ADB, and commands
  not created;
- prepare Hostess integration only as a future boundary descriptor owned by
  Manifold after accepted state or an explicit operator request.

Validation:

```powershell
python tools\package_manifold_public_derivative_schema_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json --now 2026-06-05T00:32:00Z --output fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17I: Manifold Public Derivative Schema Slice Response Expectation

Status: implemented.

Only after the Manifold public derivative schema handoff package is stable:

- define the expected future Manifold-owned response envelope for accepting,
  requesting revisions to, or rejecting the handoff package;
- keep response, decision, implementation plan, schema, route, accepted state,
  audit record, validation report, public derivative artifact, Hostess route,
  live evidence, endpoint values, ADB, and commands not created;
- require Manifold ownership for handoff acceptance, implementation plan,
  response, decision, schema, route, runtime/session, accepted state, audit,
  rollback, and redaction review;
- require explicit rejection, revision, audit, validation, privacy, and
  source-chain terms before a future Manifold repo slice can accept anything;
- keep Hostess as a future downstream boundary that requires Manifold accepted
  state or an explicit operator request.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_expectation.py --handoff-package fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json --now 2026-06-05T00:40:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17J: Manifold Public Derivative Schema Slice Response Implementation Preflight

Status: implemented.

Only after the Manifold public derivative schema slice response expectation is
stable:

- generate a descriptor-only preflight for the future Manifold-owned response
  implementation to the public derivative schema handoff package;
- enumerate required Manifold-owned artifacts for response schema,
  decision-event schema, implementation plan descriptor, accepted source-chain
  fixture, accepted-state fixture, audit fixture, validation report fixture,
  Hostess boundary descriptor, and rollback descriptor;
- name validation slots, response decisions, rejection terms, revision terms,
  audit terms, route boundaries, source-chain digest requirements, and rollback
  policy;
- keep the Manifold repo, branch, implementation plan, response, decision,
  schema, route, accepted state, audit record, validation report, public
  derivative artifact, Hostess route, live evidence, endpoint values, ADB, and
  commands not created;
- keep Hostess integration deferred until Manifold accepted state or explicit
  operator request.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-expectation.synthetic.json --now 2026-06-05T00:48:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json
python tools\package_manifold_public_derivative_schema_slice_response_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json --now 2026-06-05T00:56:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17K: Manifold Public Derivative Schema Slice Response Handoff Package

Status: implemented.

Only after the Manifold public derivative schema slice response implementation
preflight is stable:

- generate a descriptor-only handoff package for the future Manifold-owned
  public derivative schema slice response;
- bind the sidecar evidence chain, public derivative schema handoff package,
  slice response expectation, and slice response implementation preflight into
  one future Manifold repo review unit;
- carry Manifold-owned response schema, decision-event schema,
  implementation-plan descriptor, accepted source-chain, accepted state, audit,
  validation report, rollback, and Hostess boundary artifact requirements
  forward;
- require validation slots, response decisions, rejection terms, revision
  terms, audit terms, route boundaries, source-chain digest requirements, and
  rollback policy before future Manifold acceptance;
- keep the Manifold repo, branch, implementation plan, response, decision,
  schema, route, accepted state, audit record, validation report, public
  derivative artifact, Hostess route/input, live evidence, endpoint values,
  ADB, and commands not created;
- keep Hostess integration deferred until Manifold accepted state or explicit
  operator request.

Validation:

```powershell
python tools\package_manifold_public_derivative_schema_slice_response_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-slice-response-implementation-preflight.synthetic.json --now 2026-06-05T00:56:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17L: Manifold Public Derivative Schema Slice Response Operator Decision Request

Status: implemented.

Only after the Manifold public derivative schema slice response handoff package
is stable:

- generate a descriptor-only request for an operator go/hold/reject decision;
- point at the validated handoff package;
- keep the operator decision unrecorded and Manifold submission not submitted;
- keep Manifold response, decision, accepted state, audit record, validation
  report, and public derivative artifact not created;
- keep Hostess route and Hostess input not created while naming Hostess as a
  future route owner after Manifold accepted state or a separate explicit
  operator request descriptor;
- keep live evidence, endpoint values, ADB, commands, and sidecar-direct
  Hostess input absent.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_operator_decision_request.py --handoff-package fixtures\valid\manifold-public-derivative-schema-slice-response-handoff-package.synthetic.json --now 2026-06-05T01:04:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17M: Manifold Public Derivative Schema Slice Response Operator Decision Record Expectation

Status: implemented.

Only after the Manifold public derivative schema slice response operator
decision request is stable:

- generate a descriptor-only expectation for the future operator-owned decision
  record;
- define the required decision record fields and allowed decisions without
  creating the record;
- keep Manifold submission, response, decision, accepted state, audit record,
  validation report, and public derivative artifact not created;
- keep Hostess route and Hostess input not created while naming Hostess as a
  future route owner that can only consume Manifold accepted state or a
  separate explicit operator request descriptor;
- keep live evidence, endpoint values, ADB, commands, and sidecar-direct
  Hostess input absent.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_operator_decision_record_expectation.py --decision-request fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-request.synthetic.json --now 2026-06-05T01:12:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17N: Manifold Public Derivative Schema Slice Response Submission Envelope Expectation

Status: implemented.

Only after the Manifold public derivative schema slice response operator
decision record expectation is stable:

- generate a descriptor-only expectation for the future operator-owned
  submission envelope;
- define the required submission-envelope fields without creating the envelope;
- keep operator decision record, Manifold submission, response, decision,
  accepted state, audit record, validation report, and public derivative
  artifact not created;
- keep Hostess route and Hostess input not created while naming Hostess as a
  future route owner that can only consume Manifold accepted state or a
  separate explicit operator request descriptor;
- keep live evidence, endpoint values, ADB, commands, and sidecar-direct
  Hostess input absent.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_submission_envelope_expectation.py --record-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-operator-decision-record-expectation.synthetic.json --now 2026-06-05T01:20:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17O: Manifold Public Derivative Schema Slice Response Submission Intake Response Expectation

Status: implemented.

Only after the Manifold public derivative schema slice response submission
envelope expectation is stable:

- generate a descriptor-only expectation for the future Manifold-owned intake
  response;
- define the required Manifold response fields and allowed decisions without
  creating the response;
- keep submission envelope, Manifold response, decision, accepted state, audit
  record, validation report, and public derivative artifact not created;
- keep Hostess route and Hostess input not created while naming Hostess as a
  future route owner that can only consume Manifold accepted state or a
  separate explicit operator request descriptor;
- keep live evidence, endpoint values, ADB, commands, and sidecar-direct
  Hostess input absent.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_expectation.py --envelope-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-submission-envelope-expectation.synthetic.json --now 2026-06-05T01:28:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 17P: Manifold Public Derivative Schema Slice Response Submission Intake Response Implementation Preflight

Status: implemented.

Only after the Manifold public derivative schema slice response submission
intake response expectation is stable:

- generate a descriptor-only preflight for the future Manifold-owned
  submission intake response implementation;
- enumerate required Manifold-owned artifacts for response schema, route
  handler, decision-event schema, submission envelope schema binding,
  accepted-state candidate fixture, audit fixture, validation report fixture,
  rejection fixture, revision fixture, Hostess boundary descriptor, and
  rollback descriptor;
- name validation slots, response decisions, rejection terms, revision terms,
  audit terms, route boundaries, source-chain/redaction requirements, and
  rollback policy;
- keep the Manifold repo, branch, implementation plan, submission envelope,
  submission, response, decision, schema, route, accepted state, audit record,
  validation report, public derivative artifact, Hostess boundary descriptor,
  Hostess route, Hostess input, live evidence, ADB, and commands not created;
- keep Hostess integration deferred until Manifold accepted state or explicit
  operator request.

Validation:

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight.py --intake-response-expectation fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-expectation.synthetic.json --now 2026-06-05T01:36:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-submission-intake-response-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Slice 18: Private Configured Peer Rehearsal

Only after an explicit operator approval decision:

- use configured peer IDs and explicit private endpoints;
- exchange status-only gossip;
- record route health and cleanup evidence;
- keep endpoint values in private evidence only;
- produce sanitized derivative fixtures separately.

## Slice 19: Manifold-Gated Live Integration

Only after Manifold owns the acceptance route:

- sidecar agents submit observations or proposals;
- Manifold accepts or rejects with audit records;
- Hostess or an operator lane owns device actions and recovery;
- Studio may display review status but does not become authority.

## Pressure Points

- Termux can run Python and Linux userland, but it is still a normal Android
  app with lifecycle and permission constraints.
- WiFi ADB from Termux depends on explicit operator/user authorization and is
  not guaranteed to survive reboot.
- Peer mesh status can improve resilience and observability, but stale peer
  views must remain advisory.
- Remote desktop is useful for inspection, but headless CLI/status agents are
  the better default control-plane fit.
- The system must preserve a direct central recovery path for every headset.
