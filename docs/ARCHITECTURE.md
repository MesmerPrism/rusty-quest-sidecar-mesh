# Architecture

## Decision

Model the Quest Termux peer mesh as a Rusty Quest sidecar mesh integration lane.
Termux is the first implementation profile. Rusty Manifold remains the command,
session, lease, registry, and audit authority.

## Scope

This repository owns private integration contracts for:

- sidecar agent identity and capability profiles;
- advisory observations from sidecar agents;
- proposed handoffs into Manifold-controlled surfaces;
- operator approval descriptors for private status-only rehearsals;
- descriptor-only Manifold route blueprints for future repo-owned intake;
- descriptor-only Manifold route design-review requests;
- descriptor-only Manifold route design response expectations;
- descriptor-only Manifold response implementation preflights;
- descriptor-only Manifold response handoff packages for future repo-owned
  response slices;
- descriptor-only Hostess boundary descriptor expectations for future
  Manifold-enabled Hostess consumption;
- descriptor-only private rehearsal evidence expectations for future
  operator-approved evidence, redaction, Manifold intake, and Hostess
  escalation gates;
- descriptor-only private rehearsal public derivative expectations for future
  sanitized derivative schema, redaction, Manifold intake, and Hostess
  escalation gates;
- descriptor-only Manifold public derivative schema requests for future
  Manifold-owned public derivative schema, route, review, audit, accepted-state,
  and Hostess boundary work;
- descriptor-only Manifold public derivative schema response expectations for
  future Manifold-owned accept/revision/reject response, audit, revision, and
  Hostess boundary semantics;
- descriptor-only Manifold public derivative schema implementation preflights
  for future Manifold-owned schema, route, accepted-state, audit, validation
  report, and Hostess boundary descriptor work;
- descriptor-only Manifold public derivative schema handoff packages for
  future repo-owned review of the schema implementation slice and Hostess
  boundary descriptor requirements;
- descriptor-only Manifold public derivative schema slice response expectations
  for the future Manifold-owned accept/revision/reject response to the handoff
  package;
- descriptor-only Manifold public derivative schema slice response
  implementation preflights for the future Manifold-owned response schema,
  decision event, implementation plan, accepted source-chain, accepted-state,
  audit, validation report, rollback, and Hostess boundary artifacts;
- descriptor-only Manifold public derivative schema slice response operator
  decision requests for the future go/hold/reject decision before any Manifold
  submission or Hostess input exists;
- descriptor-only Manifold public derivative schema slice response operator
  decision record expectations for the future operator-owned decision record
  before any Manifold submission, accepted state, audit, or Hostess input
  exists;
- descriptor-only Manifold public derivative schema slice response submission
  envelope expectations for the future operator-owned submission envelope
  before any Manifold submission, accepted state, audit, or Hostess input
  exists;
- descriptor-only Manifold public derivative schema slice response submission
  intake response expectations for the future Manifold-owned response before
  any accepted state, audit, validation report, or Hostess input exists;
- descriptor-only Manifold public derivative schema slice response submission
  intake response implementation preflights for the future Manifold-owned
  response implementation artifacts, route boundaries, validation slots,
  accepted-state/audit/validation report ownership, and Hostess deferral rules;
- scorecards that decide whether a sidecar mesh slice is safe to promote.

## Non-Scope

This repository does not own:

- accepted Manifold state;
- command acceptance;
- Android shell authority;
- headset recovery authority;
- cross-headset ADB;
- package install or app launch;
- high-rate sensor, media, or XR payloads;
- user-facing Studio or Hostess workflows.

## Authority

Manifold is the source of truth for accepted commands, leases, revisions,
runtime registries, command rejections, and audit records.

Sidecar agents can be:

- observers of local app and Linux-userland status;
- diagnostic processors for bounded low-rate checks;
- proposal writers for handoff fixtures;
- peer-status relays for advisory status only.

Sidecar agents are not:

- Manifold authorities;
- Android `shell` authorities unless an operator-approved ADB session grants
  that to a local ADB client for a bounded task;
- recovery authorities;
- command relays;
- install or launch authorities.

## Interfaces

The first interfaces are JSON fixtures, not runtime services:

- `agent_profile`: what a sidecar can do and cannot do.
- `observation`: advisory status sampled by one sidecar.
- `mesh_handoff`: proposal to register or review sidecar evidence in Manifold.
- `public_lab_artifact_drift_review`: generated review that confirms stored
  public-lab intake still matches current sanitized source artifacts.
- `configured_peer_rehearsal_plan`: operator-approval-gated plan for
  status-only peer exchange evidence.
- `manifold_adapter_contract_review`: candidate Manifold adapter surfaces,
  lifecycle, audit fields, rejection terms, and validation slots.
- `manifold_handoff_package`: generated descriptor that binds validated
  sidecar artifacts into a future Manifold intake unit.
- `manifold_contract_intake_request`: generated descriptor that packages the
  handoff unit as a future Manifold-repo-owned contract/schema intake request.
- `private_rehearsal_approval_request`: generated descriptor that records the
  operator decision packet for a future private status-only rehearsal while
  keeping Manifold and Hostess routes uncreated.
- `manifold_route_blueprint`: generated descriptor that names candidate
  Manifold-owned request, decision, accepted-state, and audit contracts while
  preserving Hostess as a future explicit operator/recovery lane.
- `manifold_route_design_review_request`: generated descriptor that packages
  the route blueprint for future Manifold repo design review while preserving
  all work items as Manifold-owned and not created.
- `manifold_route_design_response_expectation`: generated descriptor that
  defines the expected future Manifold-owned response envelope without creating
  the response, decision, route, accepted state, audit record, or Hostess lane.
- `manifold_response_implementation_preflight`: generated descriptor that
  enumerates the future Manifold-owned implementation artifacts, validation
  slots, route boundaries, and Hostess deferral rules without touching
  Manifold or Hostess repos.
- `manifold_response_handoff_package`: generated descriptor that binds the
  response preflight and source evidence chain into a Manifold repo handoff
  package while keeping Hostess as a future boundary descriptor.
- `hostess_boundary_descriptor_expectation`: generated descriptor that defines
  future Hostess boundary prerequisites after Manifold accepted state or an
  explicit operator request while keeping Hostess routes not created.
- `private_rehearsal_evidence_expectation`: generated descriptor that defines
  future operator-approved private evidence and sanitized public derivative
  requirements before any Manifold intake or Hostess escalation.
- `private_rehearsal_public_derivative_expectation`: generated descriptor that
  defines the sanitized public derivative contract shape before any derivative
  artifact, Manifold intake, accepted state, or Hostess route exists.
- `manifold_public_derivative_schema_request`: generated descriptor that asks
  for a future Manifold-owned public derivative schema and intake route while
  keeping repo mutation, route handlers, accepted state, audit records,
  Hostess routes, private evidence, endpoints, ADB, and commands absent.
- `manifold_public_derivative_schema_response_expectation`: generated
  descriptor that defines the expected future Manifold-owned response envelope
  for accepting, requesting revisions to, or rejecting the public derivative
  schema request while keeping response, decision, schema, route, accepted
  state, audit records, public derivative artifacts, and Hostess routes absent.
- `manifold_public_derivative_schema_implementation_preflight`: generated
  descriptor that enumerates future Manifold-owned public derivative schema
  implementation artifacts, validation slots, route boundaries, accepted-state
  and audit requirements, and Hostess deferral rules without touching Manifold
  or Hostess repos.
- `manifold_public_derivative_schema_handoff_package`: generated descriptor
  that binds the implementation preflight and sidecar evidence chain into a
  future Manifold repo review unit while keeping downstream implementation,
  schema, route, accepted state, audit, validation report, public derivative,
  and Hostess route uncreated.
- `manifold_public_derivative_schema_slice_response_expectation`: generated
  descriptor that defines the expected future Manifold-owned response to the
  handoff package while keeping response, decision, schema, route, accepted
  state, audit, validation report, public derivative artifacts, and Hostess
  input uncreated.
- `manifold_public_derivative_schema_slice_response_implementation_preflight`:
  generated descriptor that enumerates future Manifold-owned slice response
  implementation artifacts, validation slots, route boundaries,
  accepted-state/source-chain/audit requirements, and Hostess deferral rules
  without touching Manifold or Hostess repos.
- `manifold_public_derivative_schema_slice_response_handoff_package`: generated
  descriptor that binds the slice response preflight and sidecar evidence chain
  into a future Manifold repo review unit while keeping response, decision,
  accepted state, audit, validation report, public derivative artifacts,
  Hostess route, and Hostess input uncreated.
- `manifold_public_derivative_schema_slice_response_operator_decision_request`:
  generated descriptor that prepares the operator go/hold/reject packet for
  submitting the handoff package to Manifold while keeping submission,
  response, accepted state, audit, Hostess route, and Hostess input uncreated.
- `manifold_public_derivative_schema_slice_response_operator_decision_record_expectation`:
  generated descriptor that defines the future operator-owned decision record
  shape while keeping submission, response, accepted state, audit, Hostess
  route, and Hostess input uncreated.
- `manifold_public_derivative_schema_slice_response_submission_envelope_expectation`:
  generated descriptor that defines the future operator-owned submission
  envelope shape while keeping the envelope, submission, response, accepted
  state, audit, Hostess route, and Hostess input uncreated.
- `manifold_public_derivative_schema_slice_response_submission_intake_response_expectation`:
  generated descriptor that defines the future Manifold-owned intake response
  shape while keeping the response, accepted state, audit, validation report,
  Hostess route, and Hostess input uncreated.
- `manifold_public_derivative_schema_slice_response_submission_intake_response_implementation_preflight`:
  generated descriptor that enumerates future Manifold-owned intake response
  implementation artifacts, validation slots, route boundaries,
  accepted-state/audit/validation report requirements, and Hostess deferral
  rules without touching Manifold or Hostess repos.
- `validation_scorecard`: compact promotion and pressure-point summary.

The schema namespace is `rusty.quest.sidecar.*`. Manifold references stay in
fields such as `target_manifold_surfaces`; this repo does not define
`rusty.manifold.*` schemas.

## Observability

Sidecar observations should record:

- source agent;
- observed agent;
- timestamp;
- transport mode;
- staleness policy;
- whether the record is synthetic, private, or sanitized;
- why the record is advisory instead of source-of-truth.

Manifold-facing handoffs should record:

- requested Manifold surface;
- request type;
- approval state;
- audit ownership;
- rejection or pressure points.

Hostess-facing descriptors should record:

- that Hostess is a future operator/recovery lane;
- that device actions require Manifold accepted state or explicit operator
  request;
- that any Hostess route is downstream of Manifold route design review or an
  operator decision;
- that private rehearsal approval does not create a Hostess route;
- that the sidecar has no Hostess route or recovery authority.

## Validation

The local validation gate checks:

- required docs, schemas, fixtures, and tests exist;
- all JSON parses;
- valid fixtures use approved schema IDs;
- damaged fixtures fail for expected reasons;
- sidecar fixtures do not contain forbidden command, ADB, pairing, endpoint,
  install, launch, secret, screenshot, or log fields;
- handoffs require Manifold or operator approval before accepted mutation;
- Manifold route blueprints keep route/session/audit authority in Manifold and
  leave Hostess device actions behind a future explicit gate.
- Manifold route design-review requests keep proposed schemas, route handlers,
  audit fixtures, and Hostess boundary descriptors not created until Manifold
  owns the response.
- Manifold route design response expectations keep accepted/revised/rejected
  decisions in Manifold and keep Hostess consumption behind Manifold accepted
  state or an explicit operator request.
- Manifold response implementation preflights keep implementation artifacts,
  validation, route ownership, audit, accepted state, and rollback in Manifold
  while keeping Hostess deferred.
- Manifold response handoff packages keep handoff acceptance, downstream
  implementation, response, decision, route, audit, accepted state, rollback,
  and Hostess boundary descriptor ownership in Manifold.
- Hostess boundary descriptor expectations keep Manifold as source of truth
  and route enablement owner while Hostess remains a future consumer/route
  owner after accepted state or explicit operator request.
- Manifold public derivative schema requests keep schema, route, review,
  accepted state, runtime/session authority, and audit ownership in Manifold
  while Hostess remains gated behind Manifold accepted state or an explicit
  operator request.
- Manifold public derivative schema response expectations keep response,
  decision, schema, route, audit, accepted state, rollback, and
  runtime/session authority in Manifold while Hostess remains gated behind
  Manifold accepted state or an explicit operator request.
- Manifold public derivative schema implementation preflights keep future
  implementation artifacts, validation, route ownership, accepted state,
  audit, rollback, and Hostess boundary descriptors in Manifold while Hostess
  remains deferred behind accepted state or an explicit operator request.
- Manifold public derivative schema handoff packages keep handoff acceptance,
  downstream implementation, schema, route, accepted state, audit, validation
  report, rollback, and Hostess boundary descriptor ownership in Manifold while
  Hostess remains deferred.
- Manifold public derivative schema slice response expectations keep response,
  decision, implementation plan, schema, route, accepted state, validation
  report, rollback, and audit ownership in Manifold while Hostess remains
  deferred behind accepted state or an explicit operator request.
- Manifold public derivative schema slice response implementation preflights
  keep future response schema, decision event, implementation plan,
  accepted source-chain, accepted-state, audit, validation report, rollback,
  and Hostess boundary artifacts in Manifold while Hostess remains deferred.
- Manifold public derivative schema slice response operator decision requests
  keep the operator decision unrecorded, Manifold submission unsubmitted,
  accepted state/audit/response uncreated, and Hostess input uncreated while
  naming Hostess as a future route owner only after Manifold accepted state or
  a separate explicit operator request descriptor.
- Manifold public derivative schema slice response operator decision record
  expectations keep the record uncreated, preserve operator ownership of the
  future record, preserve Manifold submission/acceptance/state/audit authority,
  and keep Hostess consumption behind Manifold accepted state or a separate
  explicit operator request descriptor.
- Manifold public derivative schema slice response submission envelope
  expectations keep the envelope uncreated, preserve operator ownership of the
  future envelope, preserve Manifold intake/acceptance/state/audit authority,
  and keep Hostess consumption behind Manifold accepted state or a separate
  explicit operator request descriptor.
- Manifold public derivative schema slice response submission intake response
  expectations keep the response uncreated, preserve Manifold response,
  acceptance, accepted-state, validation-report, and audit authority, and keep
  Hostess consumption behind Manifold accepted state or a separate explicit
  operator request descriptor.
- Manifold public derivative schema slice response submission intake response
  implementation preflights keep future response implementation artifacts,
  validation, route ownership, accepted state, audit, validation report,
  rollback, and Hostess boundary descriptors in Manifold while Hostess remains
  deferred.

## Reference Lessons

Borrowed from `quest-termux-lab`:

- outbound agents and peer gossip should be status-only first;
- file-drop and HTTP routes should be modeled as dry runs before live network
  transport;
- private evidence and public derivatives need separate gates.

Rejected overreach:

- making Termux a broker;
- making peer mesh messages carry commands;
- relying on Termux as reboot recovery;
- routing cross-headset ADB through peer agents;
- putting high-rate payloads into JSON command paths.
