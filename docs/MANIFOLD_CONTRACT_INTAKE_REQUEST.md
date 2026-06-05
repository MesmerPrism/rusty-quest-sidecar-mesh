# Manifold Contract Intake Request

## Decision

Prepare a descriptor-only Manifold contract-intake request from the generated
handoff package before touching the Manifold repo.

The request is a private sidecar artifact. It names the candidate intake
surfaces, validation commands, rejection terms, and authority owners that a
future Manifold-owned contract slice should consider. It does not create that
slice.

## Scope

- source Manifold handoff package pointer;
- proposed Manifold contract-intake target surfaces;
- validation and damaged-fixture evidence required before promotion;
- downstream private rehearsal approval request boundary;
- downstream Manifold route blueprint boundary;
- Manifold authority and accepted-state ownership;
- Hostess descriptor-only operator/recovery boundary;
- privacy flags proving the request is endpoint-free and command-free.

## Non-Scope

No Manifold repo change, Hostess repo change, live Quest, ADB, socket,
listener, endpoint discovery, remote desktop, file copy, install, launch,
recovery, Studio, Makepad, PMD, Polar, controller, public Rusty-XR runtime, or
accepted Manifold state is added.

## Authority

The sidecar repo prepares the request. Manifold remains the only owner that can
accept, reject, revise, lease, or audit runtime state. Hostess remains a future
operator/recovery lane after Manifold accepted state or explicit operator
request.

## Validation

```powershell
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
