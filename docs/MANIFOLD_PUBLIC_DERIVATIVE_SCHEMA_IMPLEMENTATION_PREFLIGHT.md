# Manifold Public Derivative Schema Implementation Preflight

## Decision

Prepare a descriptor-only preflight for the future Manifold repo slice that
could implement the public derivative schema response expectation.

This artifact does not implement Manifold behavior. It enumerates the required
Manifold-owned schemas, route handler, decision fixture, accepted-state
fixture, audit fixture, validation report, and Hostess boundary descriptor
before any downstream repo is touched.

## Scope

- source Manifold public derivative schema response expectation pointer;
- required future Manifold-owned artifacts for response schema, input schema,
  route handling, decision events, accepted state, audit, validation reporting,
  and Hostess boundary description;
- required validation slots, response decisions, rejection terms, revision
  terms, route boundaries, and rollback policy;
- Hostess deferral rule requiring Manifold accepted state or an explicit
  operator request.

## Non-Scope

No Manifold repo change, branch, response, decision, schema, route handler,
accepted state, audit record, validation report, public derivative artifact,
operator approval, private evidence, live Quest, ADB, socket, endpoint
discovery, remote desktop, file copy, install, launch, recovery, command relay,
raw log capture, visual capture, Hostess repo change, Hostess route, Studio,
Makepad, PMD, Polar, controller, or public Rusty-XR runtime change is added by
this slice.

## Authority

The sidecar owns the preflight descriptor only. Manifold owns any future
implementation plan, response, decision, schema, route implementation, request
acceptance, runtime/session authority, accepted state, rollback, revision, and
audit record.

The operator owns approval and redaction review before real public derivative
evidence can be accepted. Hostess remains a future operator-recovery lane that
can act only from Manifold accepted state or an explicit operator request.

## Hostess Gate

This preflight prepares Hostess integration without giving the sidecar a direct
device-action path:

- no Hostess route is created;
- Hostess may consume only Manifold accepted state or an explicit operator
  request descriptor;
- sidecar public derivative status cannot become direct Hostess input;
- any recovery lane remains outside this repo until Manifold has accepted
  state or the operator explicitly requests recovery.

## Next Handoff

`MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_HANDOFF_PACKAGE.md` packages this preflight
and the sidecar evidence chain for future Manifold repo review. The Manifold
repo must still own any actual schema, route, accepted-state, audit,
validation, and Hostess boundary implementation.

## Validation

```powershell
python tools\prepare_manifold_public_derivative_schema_implementation_preflight.py --response-expectation fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json --now 2026-06-05T00:24:00Z --output fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json
python tools\package_manifold_public_derivative_schema_handoff.py --preflight fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json --now 2026-06-05T00:32:00Z --output fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
