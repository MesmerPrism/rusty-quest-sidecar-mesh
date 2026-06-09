# Rusty Quest Sidecar Mesh Agent Notes

This is a public-safe integration repository for Quest-hosted Linux sidecar
mesh work. The first implementation profile is Termux on Quest, but the
architecture surface is `Rusty Quest sidecar mesh` so Termux remains an adapter
profile, not a top-level Rusty domain.

Rusty Morphospace is the top-level project/platform umbrella. This repo remains
a Quest sidecar integration lane inside that umbrella; it may rehearse evidence
and handoffs but must not become Morphospace, Lattice, Manifold, or Hostess
authority.

Project-owned source in this repo is licensed `AGPL-3.0-or-later`. Keep
third-party dependencies, Termux or Linux-sidecar packages, generated evidence,
captured data, private endpoints, device logs, binary releases, APKs, and
external tools under their own provenance and notice requirements; see
`docs/LICENSING.md`.

## Purpose

Use this repository to integrate the Quest Termux outbound-agent and peer-mesh
research into the refactored Rusty architecture without changing live Hostess,
Studio, Makepad, PMD, Polar, controller, or public Rusty-XR runtime behavior.

Rusty Lattice is the target lane for generic situated relation contracts:
spaces, transforms, tracked poses, view sets, spatial input roles, frame-state
binding, calibration, validity, confidence, and runtime capability snapshots.
This sidecar repo may propose or rehearse relation evidence, but it must not
become Lattice contract authority or Manifold command/session authority.

The initial slice is data-only:

- sidecar agent profiles;
- advisory status observations;
- sanitized public-lab artifact intake;
- public-lab artifact drift reviews;
- proposed Manifold handoffs;
- Manifold adapter proposal fixtures;
- Manifold adapter contract reviews;
- Manifold handoff packages;
- Manifold contract-intake requests;
- private rehearsal approval requests;
- Manifold route blueprints;
- Manifold route design-review requests;
- Manifold route design response expectations;
- Manifold response implementation preflights;
- Manifold response handoff packages;
- Hostess boundary descriptor expectations;
- private rehearsal evidence expectations;
- private rehearsal public derivative expectations;
- Manifold public derivative schema requests;
- Manifold public derivative schema response expectations;
- Manifold public derivative schema implementation preflights;
- Manifold public derivative schema handoff packages;
- Manifold public derivative schema slice response expectations;
- Manifold public derivative schema slice response implementation preflights;
- Manifold public derivative schema slice response handoff packages;
- Manifold public derivative schema slice response operator decision requests;
- Manifold public derivative schema slice response operator decision record expectations;
- Manifold public derivative schema slice response submission envelope expectations;
- Manifold public derivative schema slice response submission intake response expectations;
- Manifold public derivative schema slice response submission intake response implementation preflights;
- Manifold public derivative schema slice response submission intake response handoff packages;
- integration acceptance scorecards;
- no-network prototype run reports;
- no-network prototype handoff reviews;
- configured peer rehearsal plans;
- no-network agent recipes;
- no-network recipe reviews;
- validation scorecards;
- boundary checks that reject command authority, ADB authority, pairing
  material, private endpoints, and launch/install requests.

## Read Order

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/INTEGRATION_ROADMAP.md`
4. `docs/TERMUX_CAPABILITY_MAP.md`
5. `docs/PUBLIC_LAB_ARTIFACT_INTAKE.md`
6. `docs/PUBLIC_LAB_ARTIFACT_DRIFT_REVIEW.md`
7. `docs/MANIFOLD_HANDOFF.md`
8. `docs/NO_NETWORK_AGENT_RECIPE.md`
9. `docs/NO_NETWORK_AGENT_RECIPE_REVIEW.md`
10. `docs/NO_NETWORK_AGENT_PROTOTYPE.md`
11. `docs/NO_NETWORK_PROTOTYPE_HANDOFF_REVIEW.md`
12. `docs/CONFIGURED_PEER_REHEARSAL_PLAN.md`
13. `docs/MANIFOLD_ADAPTER_CONTRACT_REVIEW.md`
14. `docs/MANIFOLD_HANDOFF_PACKAGE.md`
15. `docs/MANIFOLD_CONTRACT_INTAKE_REQUEST.md`
16. `docs/PRIVATE_REHEARSAL_APPROVAL_REQUEST.md`
17. `docs/MANIFOLD_ROUTE_BLUEPRINT.md`
18. `docs/MANIFOLD_ROUTE_DESIGN_REVIEW_REQUEST.md`
19. `docs/MANIFOLD_ROUTE_DESIGN_RESPONSE_EXPECTATION.md`
20. `docs/MANIFOLD_RESPONSE_IMPLEMENTATION_PREFLIGHT.md`
21. `docs/MANIFOLD_RESPONSE_HANDOFF_PACKAGE.md`
22. `docs/HOSTESS_BOUNDARY_DESCRIPTOR_EXPECTATION.md`
23. `docs/PRIVATE_REHEARSAL_EVIDENCE_EXPECTATION.md`
24. `docs/PRIVATE_REHEARSAL_PUBLIC_DERIVATIVE_EXPECTATION.md`
25. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_REQUEST.md`
26. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_RESPONSE_EXPECTATION.md`
27. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_IMPLEMENTATION_PREFLIGHT.md`
28. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_HANDOFF_PACKAGE.md`
29. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_EXPECTATION.md`
30. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_IMPLEMENTATION_PREFLIGHT.md`
31. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_HANDOFF_PACKAGE.md`
32. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_OPERATOR_DECISION_REQUEST.md`
33. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_OPERATOR_DECISION_RECORD_EXPECTATION.md`
34. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_ENVELOPE_EXPECTATION.md`
35. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_INTAKE_RESPONSE_EXPECTATION.md`
36. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_INTAKE_RESPONSE_IMPLEMENTATION_PREFLIGHT.md`
37. `docs/MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_SLICE_RESPONSE_SUBMISSION_INTAKE_RESPONSE_HANDOFF_PACKAGE.md`
38. `fixtures/README.md`

## Architecture Rules

- Rusty Manifold owns command/session authority, accepted mutable state,
  revisions, leases, command decisions, audit records, and live topology truth.
- Rusty Quest owns Quest platform behavior, sidecar app constraints, lifecycle,
  local filesystem affordances, and headset-hosted operator surfaces.
- Sidecar agents may observe, process bounded diagnostics, propose handoffs,
  and exchange advisory peer status.
- Sidecar agents do not own Android shell authority, recovery authority,
  cross-headset ADB authority, install/launch authority, or Manifold command
  acceptance.
- Peer mesh messages are status and evidence hints only. They must not carry
  shell text, command payloads, ADB targets, pairing material, package IDs,
  launch requests, install requests, raw endpoint values, screenshots, or logs.
- Prefer schemas, fixtures, and validation gates before any live LAN discovery,
  socket transport, file copy, Android service, or device command path.

## Validation

Run this before treating the repo as coherent:

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

Live Quest, ADB, APK, logcat, screenshot, Perfetto, or bridge-port work is out
of scope for this repo until a later explicitly approved live run.
