# Configured Peer Rehearsal Plan

## Decision

Prepare the first peer-mesh rehearsal as an operator-approved, private evidence
run while keeping repository fixtures endpoint-free and command-free.

The plan is a generated descriptor. It proves that the sidecar mesh can move
from an offline local observation into a configured status-only peer rehearsal
without making Termux, Hostess, or the peer mesh the authority.

## Scope

- synthetic peer roles and peer-count expectations;
- route-health and cleanup evidence slots;
- Manifold candidate intake and audit fields;
- Hostess operator-recovery request descriptors;
- explicit redaction rules for any future private evidence;
- downstream private rehearsal approval request fields;
- downstream Manifold route blueprint fields;
- rejection terms for endpoint, command, ADB, and approval drift.

## Non-Scope

No endpoint values, live Quest, ADB, socket, listener, remote desktop, file
copy, install, launch, recovery, shell route, Manifold route, Hostess route,
Studio, Makepad, PMD, Polar, controller, or public Rusty-XR runtime change is
added by this slice.

## Authority

Manifold remains the future owner of acceptance, rejection, revision, leases,
audit, and accepted topology. Hostess remains a future operator/recovery lane
that can act only from Manifold accepted state or explicit operator request.
Sidecars may only exchange low-rate advisory status after explicit operator
approval and must emit sanitized derivatives for repo fixtures.

## Validation

```powershell
python tools\plan_configured_peer_rehearsal.py --handoff-review fixtures\valid\no-network-prototype-handoff-review.synthetic.json --now 2026-06-04T22:25:00Z --output fixtures\valid\configured-peer-rehearsal-plan.synthetic.json
python tools\review_manifold_adapter_contract.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --now 2026-06-04T22:32:00Z --output fixtures\valid\manifold-adapter-contract-review.synthetic.json
python tools\package_manifold_handoff.py --contract-review fixtures\valid\manifold-adapter-contract-review.synthetic.json --now 2026-06-04T22:40:00Z --output fixtures\valid\manifold-handoff-package.synthetic.json
python tools\prepare_manifold_contract_intake.py --handoff-package fixtures\valid\manifold-handoff-package.synthetic.json --now 2026-06-04T22:48:00Z --output fixtures\valid\manifold-contract-intake-request.synthetic.json
python tools\prepare_private_rehearsal_approval.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --now 2026-06-04T22:56:00Z --output fixtures\valid\private-rehearsal-approval-request.synthetic.json
python tools\prepare_manifold_route_blueprint.py --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --private-approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --now 2026-06-04T23:04:00Z --output fixtures\valid\manifold-route-blueprint.synthetic.json
python tools\prepare_manifold_route_design_review.py --route-blueprint fixtures\valid\manifold-route-blueprint.synthetic.json --now 2026-06-04T23:12:00Z --output fixtures\valid\manifold-route-design-review-request.synthetic.json
python tools\prepare_manifold_route_design_response_expectation.py --design-review-request fixtures\valid\manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures\valid\manifold-route-design-response-expectation.synthetic.json
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
