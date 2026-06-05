# Manifold Route Design Response Expectation

## Decision

Prepare a descriptor-only expectation for the future Manifold-owned response to
the sidecar peer-status route design-review request.

This artifact does not create the response. It defines what a later Manifold
slice must make explicit before the sidecar mesh work can be treated as
accepted, revised, or rejected.

## Scope

- source Manifold route design-review request pointer;
- expected Manifold-owned response envelope;
- allowed response decisions: `accepted_for_manifold_slice`,
  `revision_requested`, and `rejected`;
- required response fields for IDs, decision owner, response owner, revision,
  route references, schema references, accepted-state references, audit
  references, rejection terms, revision terms, Hostess boundary references, and
  privacy review;
- required rejection and revision vocabulary;
- disallowed response content classes for endpoints, shell text, Android
  targets, pairing material, package markers, high-rate payloads, raw logs,
  and visual captures;
- Hostess response gate requiring Manifold accepted state or an explicit
  operator request;
- downstream Manifold response implementation preflight boundary.

## Non-Scope

No Manifold repo change, Manifold response, Manifold decision, Manifold route,
Manifold schema, accepted state, audit record, Hostess route, live Quest, ADB,
socket, listener, endpoint discovery, remote desktop, file copy, install,
launch, recovery, Studio, Makepad, PMD, Polar, controller, public Rusty-XR
runtime, operator approval, or private evidence is added.

## Authority

The sidecar repo prepares the response expectation. Manifold remains the owner
of the future response, decision, route implementation, request acceptance,
runtime/session authority, accepted state, rollback, and audit. Hostess remains
a future operator/recovery lane after Manifold accepted state or explicit
operator request. The sidecar remains an observer/proposer.

## Hostess Gate

Hostess integration is prepared only as a downstream consumption rule:

- Hostess may consume Manifold accepted state or an explicit operator request;
- Hostess may not consume sidecar peer messages directly;
- sidecar agents do not provide direct Hostess device-action input;
- any Hostess route remains not created in this repo.

## Validation

```powershell
python tools\prepare_manifold_route_design_response_expectation.py --design-review-request fixtures\valid\manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures\valid\manifold-route-design-response-expectation.synthetic.json
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
