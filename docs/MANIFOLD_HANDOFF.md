# Manifold Handoff

Sidecar mesh data enters the Rusty architecture as a proposal. It does not
become accepted live state until a Manifold-owned route accepts it.

## Handoff Roles

- `sidecar_agent`: emits advisory observations or proposal files.
- `operator`: approves private live experiments and endpoint selection.
- `rusty.quest.sidecar_mesh`: structures sidecar evidence and pressure points.
- `rusty.manifold`: accepts, rejects, revises, leases, and audits runtime state.
- `rusty.hostess` or equivalent platform lane: executes device actions after
  explicit approval.

## Acceptable Request Types

- `register_observation_source`
- `attach_advisory_observation`
- `review_public_lab_artifact_intake`
- `review_sidecar_scorecard`
- `propose_sidecar_health_stream`
- `propose_sidecar_peer_status_rehearsal`
- `review_sidecar_peer_status_adapter_contract`
- `open_sidecar_mesh_contract_intake`
- `request_private_rehearsal_operator_approval`
- `review_sidecar_peer_status_route_blueprint`
- `request_sidecar_peer_status_route_design_review`
- `declare_expected_sidecar_peer_status_route_design_response`
- `preflight_sidecar_peer_status_response_implementation`
- `propose_private_live_run_gate`

These request types are proposals. They are not commands to execute shell text,
pair ADB, install APKs, launch apps, or recover a headset.

## Required Rejection Reasons

Future Manifold or Hostess routes should be able to reject with:

- `stale_observation`
- `untrusted_sidecar`
- `forbidden_authority`
- `redaction_incomplete`
- `operator_approval_missing`
- `endpoint_values_rejected`
- `commands_rejected`
- `adb_rejected`
- `stale_peer_status`
- `recovery_route_required`
- `payload_too_high_rate`
- `unsupported_transport`

## Audit Ownership

The sidecar handoff fixture records proposal evidence. Manifold owns the audit
record for any accepted, rejected, or revised mutation. A future accepted
Manifold record should point back to the handoff ID rather than copying private
sidecar internals into low-rate command records.

## Public Lab Intake

Public-safe `quest-termux-lab` reports enter this repo through
`rusty.quest.sidecar.public_lab_artifact_intake_report.v1`. The intake report
records only declared artifact IDs, schemas, relative paths, status values,
status classes, and summary counts. It does not import endpoint values, raw
logs, screenshots, pairing material, package identities, command payloads, or
private live evidence.

The Manifold handoff may reference the intake report as proposal evidence, but
the report does not become accepted topology, live readiness, or command
authority until a Manifold-owned route accepts it.

`rusty.quest.sidecar.public_lab_artifact_drift_review.v1` compares the stored
intake report with current sanitized source artifacts from `quest-termux-lab`.
It proves the sidecar intake has not drifted without copying raw artifacts,
executing source validation, importing private values, or changing Manifold
state.

## Hostess Integration Prep

Hostess-facing records in this repo are request descriptors only. They prepare
the future operator/recovery lane by naming required authority, expected input
state, and rejection terms. They do not create Hostess routes, perform recovery
actions, or let sidecar agents act as device authorities.

Any future Hostess lane should consume Manifold accepted state or an explicit
operator request. It should not consume sidecar peer messages, raw endpoints,
or sidecar-generated command payloads directly.

## Adapter Contract Review

`rusty.quest.sidecar.manifold_adapter_contract_review.v1` is the current
descriptor for future Manifold work. It records candidate surfaces, lifecycle
states, intake fields, audit fields, rejection terms, rollback owner, and
validation slots. It still does not create accepted state; the Manifold repo
must own any later concrete adapter route.

## Handoff Package

`rusty.quest.sidecar.manifold_handoff_package.v1` binds the sidecar artifact
chain into one descriptor for future Manifold intake. It names the source
artifacts, target surfaces, validation commands, rejection terms, privacy
flags, and non-scope flags. It is still not accepted state.

## Contract Intake Request

`rusty.quest.sidecar.manifold_contract_intake_request.v1` prepares the next
private descriptor for a future Manifold-owned schema/route slice. It points at
the generated handoff package, names candidate Manifold intake surfaces,
records required validation and rejection terms, and keeps the Manifold repo,
Hostess route, live evidence, accepted state, endpoints, ADB, and commands out
of the sidecar repo.

## Private Rehearsal Approval Request

`rusty.quest.sidecar.private_rehearsal_approval_request.v1` prepares the
operator decision packet for a later private status-only peer rehearsal. It
points at the configured peer rehearsal plan and Manifold contract-intake
request, records required private inputs and public derivatives, and keeps
Hostess routes, Manifold routes, accepted state, endpoint values, ADB, and
commands out of the sidecar repo.

## Manifold Route Blueprint

`rusty.quest.sidecar.manifold_route_blueprint.v1` prepares the current
descriptor for future Manifold repo design review. It names candidate
Manifold-owned request, decision-event, accepted-state, and audit contracts for
sidecar peer status intake. It still does not create a route, accepted state,
audit record, or Hostess lane.

## Manifold Route Design Review Request

`rusty.quest.sidecar.manifold_route_design_review_request.v1` packages the
route blueprint into a review request for a future Manifold-owned response. It
names review topics and proposed Manifold work items, but leaves every schema,
route handler, accepted-state shape, audit fixture, and Hostess boundary
descriptor not created.

## Manifold Route Design Response Expectation

`rusty.quest.sidecar.manifold_route_design_response_expectation.v1` defines the
expected envelope for that future Manifold-owned response. It requires the
response to keep decisions, route implementation, accepted state, audit, and
rollback in Manifold; it also requires Hostess to consume only Manifold
accepted state or an explicit operator request. It still does not create a
response, route, accepted state, audit record, or Hostess lane.

## Manifold Response Implementation Preflight

`rusty.quest.sidecar.manifold_response_implementation_preflight.v1` turns the
response expectation into Manifold repo slice requirements. It names the future
Manifold-owned artifacts, validation slots, route boundaries, rejection terms,
and Hostess deferral rule. It still does not touch the Manifold repo, create a
branch, create a response, create a route, create accepted state, create audit
records, or create a Hostess lane.
