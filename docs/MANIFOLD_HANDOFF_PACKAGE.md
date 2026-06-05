# Manifold Handoff Package

## Decision

Bundle the validated sidecar mesh artifacts into a descriptor-only handoff
package for a future Manifold-owned adapter route.

The package is not an implementation. It is a stable manifest of which sidecar
contracts, fixtures, reviews, damaged-boundary examples, and validation
commands are ready to be consumed by future Manifold work.

## Scope

- contract review source pointer;
- ordered artifact set for future Manifold intake;
- proposed destination surfaces and required owner;
- validation evidence summary;
- downstream contract-intake and private rehearsal approval descriptors;
- downstream Manifold route blueprint descriptor;
- privacy and authority boundaries;
- Hostess descriptor-only recovery boundary.

## Non-Scope

No Manifold repo change, Hostess repo change, live Quest, ADB, socket,
listener, endpoint discovery, remote desktop, file copy, install, launch,
recovery, Studio, Makepad, PMD, Polar, controller, public Rusty-XR runtime, or
accepted Manifold state is added.

## Authority

The sidecar repo prepares the package. Manifold remains the only owner that can
accept, reject, revise, lease, or audit runtime state. Hostess remains a future
operator/recovery lane after Manifold acceptance or explicit operator request.

## Validation

```powershell
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
