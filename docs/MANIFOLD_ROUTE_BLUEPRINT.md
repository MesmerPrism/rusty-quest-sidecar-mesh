# Manifold Route Blueprint

## Decision

Prepare a descriptor-only blueprint for the future Manifold-owned route and
schema slice. The blueprint names candidate request, event, state, and audit
contracts without touching the Manifold repo or creating any route.

## Scope

- source Manifold contract-intake request;
- source private rehearsal approval request;
- candidate Manifold route name and validation slots;
- candidate request, event, accepted-state, and audit schemas;
- required rejection terms and rollback owner;
- Hostess operator/recovery boundary as descriptor-only;
- downstream Manifold route design-review request boundary;
- downstream Manifold route design response expectation boundary.

## Non-Scope

No Manifold repo change, Hostess repo change, live Quest, ADB, socket,
listener, endpoint discovery, remote desktop, file copy, install, launch,
recovery, shell route, Manifold route, Hostess route, Studio, Makepad, PMD,
Polar, controller, public Rusty-XR runtime, operator approval, private
evidence, or accepted Manifold state is added.

## Authority

The sidecar repo prepares the blueprint. Manifold remains the only owner that
can implement a route, accept or reject requests, create accepted state, revise
state, lease resources, or write audit records. Hostess remains a future
operator/recovery lane after Manifold accepted state or explicit operator
request. The sidecar remains an observer/proposer.

## Validation

```powershell
python tools\prepare_manifold_route_blueprint.py --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --private-approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --now 2026-06-04T23:04:00Z --output fixtures\valid\manifold-route-blueprint.synthetic.json
python tools\prepare_manifold_route_design_review.py --route-blueprint fixtures\valid\manifold-route-blueprint.synthetic.json --now 2026-06-04T23:12:00Z --output fixtures\valid\manifold-route-design-review-request.synthetic.json
python tools\prepare_manifold_route_design_response_expectation.py --design-review-request fixtures\valid\manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures\valid\manifold-route-design-response-expectation.synthetic.json
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
