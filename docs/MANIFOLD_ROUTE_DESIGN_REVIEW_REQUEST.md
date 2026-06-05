# Manifold Route Design Review Request

## Decision

Prepare a descriptor-only request for future Manifold repo design review of the
sidecar peer-status route. The request consumes the Manifold route blueprint
and turns it into a review packet that a Manifold-owned slice can accept,
revise, or reject later.

## Scope

- source Manifold route blueprint pointer;
- Manifold-owned review topics for schema, decision event, accepted state,
  audit, Hostess boundary, privacy, and rejection terms;
- proposed Manifold work items that remain not created;
- Hostess integration preconditions that require Manifold accepted state or an
  explicit operator request;
- downstream Manifold route design response expectation boundary;
- validation and damaged-fixture evidence.

## Non-Scope

No Manifold repo change, Hostess repo change, live Quest, ADB, socket,
listener, endpoint discovery, remote desktop, file copy, install, launch,
recovery, shell route, Manifold schema, Manifold route, Hostess route, Studio,
Makepad, PMD, Polar, controller, public Rusty-XR runtime, operator approval,
private evidence, or accepted Manifold state is added.

## Authority

The sidecar repo prepares the request. Manifold remains the owner of design
review, route implementation, request acceptance, runtime/session authority,
accepted state, rollback, and audit. Hostess remains a future operator/recovery
lane after Manifold accepted state or explicit operator request. The sidecar
remains an observer/proposer.

## Validation

```powershell
python tools\prepare_manifold_route_design_review.py --route-blueprint fixtures\valid\manifold-route-blueprint.synthetic.json --now 2026-06-04T23:12:00Z --output fixtures\valid\manifold-route-design-review-request.synthetic.json
python tools\prepare_manifold_route_design_response_expectation.py --design-review-request fixtures\valid\manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures\valid\manifold-route-design-response-expectation.synthetic.json
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
