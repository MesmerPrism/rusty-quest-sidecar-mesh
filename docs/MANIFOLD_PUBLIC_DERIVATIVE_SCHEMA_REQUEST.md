# Manifold Public Derivative Schema Request

## Decision

Prepare a descriptor-only request for a future Manifold-owned public derivative
schema and intake route.

This artifact does not touch the Manifold repo. It packages the sanitized
public derivative contract, requested Manifold ownership, rejection terms, and
Hostess deferral rules so a future Manifold repo agent can review the slice.

## Scope

- source private rehearsal public derivative expectation;
- future Manifold schema and route ownership;
- required sanitized fields and prohibited private/action fields;
- required rejection terms and validation gates;
- Manifold review gate;
- Hostess escalation boundary.

## Non-Scope

No Manifold repo change, branch, schema, route handler, accepted state, audit
record, operator approval, private evidence, public derivative artifact, live
Quest, ADB, socket, endpoint discovery, remote desktop, file copy, install,
launch, recovery, command relay, raw log capture, visual capture, Hostess repo
change, Studio, Makepad, PMD, Polar, controller, or public Rusty-XR runtime
change is added by this slice.

## Authority

The sidecar owns the request artifact only. Manifold owns any future schema,
route, review, handoff acceptance, runtime/session authority, accepted state,
and audit records.

The operator owns approval and redaction review before real public derivative
evidence can be submitted. Hostess remains a future operator-recovery lane that
can act only from Manifold accepted state or an explicit operator request.

## Validation

```powershell
python tools\prepare_manifold_public_derivative_schema_request.py --public-derivative-expectation fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json --now 2026-06-05T00:08:00Z --output fixtures\valid\manifold-public-derivative-schema-request.synthetic.json
python tools\prepare_manifold_public_derivative_schema_response_expectation.py --schema-request fixtures\valid\manifold-public-derivative-schema-request.synthetic.json --now 2026-06-05T00:16:00Z --output fixtures\valid\manifold-public-derivative-schema-response-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Next Slice

The next data-only slice is
`manifold_public_derivative_schema_response_expectation`: a sidecar-owned
expectation artifact for future Manifold response semantics. It must not create
Manifold routes, accepted state, audit records, public derivative artifacts, or
Hostess actions inside this repo.
