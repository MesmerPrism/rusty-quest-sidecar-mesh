# Manifold Public Derivative Schema Response Expectation

## Decision

Prepare a descriptor-only expectation for the future Manifold-owned response to
the public derivative schema request.

This artifact does not touch the Manifold repo. It defines the response
envelope, allowed decisions, rejection terms, revision terms, audit terms, and
Hostess deferral rules that a future Manifold repo slice should own.

## Scope

- source Manifold public derivative schema request;
- future Manifold response and decision ownership;
- accepted, revision-requested, and rejected decision vocabulary;
- required response fields, rejection terms, revision terms, and audit terms;
- disallowed private/action content;
- Hostess response gate.

## Non-Scope

No Manifold repo change, branch, schema, route handler, accepted state, audit
record, operator approval, private evidence, public derivative artifact, live
Quest, ADB, socket, endpoint discovery, remote desktop, file copy, install,
launch, recovery, command relay, raw log capture, visual capture, Hostess repo
change, Hostess route, Studio, Makepad, PMD, Polar, controller, or public
Rusty-XR runtime change is added by this slice.

## Authority

The sidecar owns the expectation artifact only. Manifold owns any future
response, decision, schema, route implementation, handoff acceptance,
runtime/session authority, accepted state, rollback, and audit record.

The operator owns approval and redaction review before real public derivative
evidence can be accepted. Hostess remains a future operator-recovery lane that
can act only from Manifold accepted state or an explicit operator request.

## Next Slice

`MANIFOLD_PUBLIC_DERIVATIVE_SCHEMA_IMPLEMENTATION_PREFLIGHT.md` converts this
response expectation into a descriptor-only checklist for a future
Manifold-owned implementation slice. That preflight prepares Hostess boundary
requirements but still creates no Hostess route or direct sidecar input.

## Validation

```powershell
python tools\prepare_manifold_public_derivative_schema_response_expectation.py --schema-request fixtures\valid\manifold-public-derivative-schema-request.synthetic.json --now 2026-06-05T00:16:00Z --output fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_implementation_preflight.py --response-expectation fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json --now 2026-06-05T00:24:00Z --output fixtures\valid\manifold-public-derivative-schema-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
