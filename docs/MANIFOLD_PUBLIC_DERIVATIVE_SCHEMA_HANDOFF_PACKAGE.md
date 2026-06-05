# Manifold Public Derivative Schema Handoff Package

## Decision

Prepare a descriptor-only handoff package for a future Manifold repo public
derivative schema slice.

This artifact packages the validated public derivative schema implementation
preflight and the sidecar evidence chain so a later Manifold-owned slice can
review or implement the response schema, input schema, route handler,
decision-event fixture, accepted-state fixture, audit fixture, validation
report fixture, and Hostess boundary descriptor without mining this sidecar
repo for implicit intent.

## Scope

- source Manifold public derivative schema implementation preflight pointer;
- package scope proving no repo, branch, response, decision, schema, route,
  accepted state, audit record, validation report, public derivative artifact,
  Hostess route, or live evidence has been created;
- source-chain manifest over public-lab drift evidence, no-network prototype
  handoff review, configured peer rehearsal plan, Manifold contract-intake
  request, private rehearsal approval/evidence/public-derivative expectations,
  public derivative schema request, response expectation, implementation
  preflight, and acceptance scorecard;
- downstream Manifold-owned artifact list copied from the preflight;
- downstream validation slots, response decisions, rejection terms, revision
  terms, route boundaries, and rollback policy;
- Hostess boundary descriptor preparation.

## Non-Scope

No Manifold repo change, branch, response, decision, schema, route, accepted
state, audit record, validation report, public derivative artifact, Hostess
route, live Quest, ADB, socket, listener, endpoint discovery, remote desktop,
file copy, install, launch, recovery, Studio, Makepad, PMD, Polar, controller,
public Rusty-XR runtime, operator approval, or private evidence is added.

## Authority

The sidecar repo owns this package as proposal evidence. Manifold remains the
handoff acceptance, implementation plan, response, decision, schema, route
implementation, request acceptance, runtime/session, accepted-state, rollback,
redaction/revision gate, and audit authority.

Hostess remains a future operator/recovery lane. It may later consume Manifold
accepted state or an explicit operator request descriptor, but sidecar public
derivative status cannot become direct Hostess device-action input.

## Hostess Gate

This package is intentionally Hostess-aware but not Hostess-active:

- no Hostess route is created;
- no device action authority is granted to the sidecar;
- Hostess consumption requires Manifold accepted state or an explicit operator
  request;
- the downstream Hostess boundary descriptor is owned by Manifold until a later
  explicit Hostess integration slice exists.

## Next Handoff

The next safe sidecar-only slice is the Manifold public derivative schema slice
response expectation. It defines the expected future Manifold accept, revision,
or reject response without creating that response. Until Manifold owns a real
response or an operator decision exists, this package is only proposal evidence
and cannot authorize sidecar commands, ADB, Hostess input, or accepted state.

## Validation

```powershell
python tools\package_manifold_public_derivative_schema_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json --now 2026-06-05T00:32:00Z --output fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json
python tools\prepare_manifold_public_derivative_schema_slice_response_expectation.py --handoff-package fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json --now 2026-06-05T00:40:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
