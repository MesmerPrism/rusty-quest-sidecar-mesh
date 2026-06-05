# Manifold Response Implementation Preflight

## Decision

Prepare a descriptor-only preflight for the future Manifold repo slice that
would answer the sidecar peer-status route design-review request.

This artifact does not implement the Manifold slice. It makes the later
Manifold-owned work concrete enough to validate before anyone creates a route,
response schema, accepted-state fixture, audit fixture, or Hostess boundary
descriptor downstream.

## Scope

- source Manifold route design response expectation pointer;
- required future Manifold-owned artifacts:
  - response schema;
  - route handler;
  - decision-event fixture;
  - accepted-state fixture;
  - audit fixture;
  - Hostess boundary descriptor;
- required validation slots for schema contract, valid and damaged response
  fixtures, route unit tests, audit fixture, Hostess boundary descriptor, and
  privacy/rejection checks;
- required response decisions and rejection terms;
- route-boundary constraints for low-rate advisory input only;
- Hostess deferral rule requiring Manifold accepted state or an explicit
  operator request.

## Non-Scope

No Manifold repo change, branch, response, decision, Manifold route, Manifold
schema, accepted state, audit record, Hostess route, live Quest, ADB, socket,
listener, endpoint discovery, remote desktop, file copy, install, launch,
recovery, Studio, Makepad, PMD, Polar, controller, public Rusty-XR runtime,
operator approval, or private evidence is added.

## Authority

The sidecar repo prepares the preflight. Manifold remains the owner of the
future implementation plan, response, decision, route implementation, request
acceptance, runtime/session authority, accepted state, rollback, and audit.
Hostess remains a future operator/recovery lane after Manifold accepted state
or explicit operator request. The sidecar remains an observer/proposer.

## Hostess Gate

This preflight keeps Hostess deferred:

- no Hostess route is created;
- Hostess may consume only Manifold accepted state or an explicit operator
  request;
- sidecar peer status cannot become direct Hostess device-action input;
- any recovery lane remains outside this repo.

## Next Handoff

`MANIFOLD_RESPONSE_HANDOFF_PACKAGE.md` packages this preflight and the source
evidence chain into a future Manifold repo handoff unit. That handoff is still
proposal evidence only; it does not create Manifold response artifacts or a
Hostess route.

## Validation

```powershell
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\package_manifold_response_handoff.py --preflight fixtures\valid\manifold-response-implementation-preflight.synthetic.json --now 2026-06-04T23:36:00Z --output fixtures\valid\manifold-response-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
