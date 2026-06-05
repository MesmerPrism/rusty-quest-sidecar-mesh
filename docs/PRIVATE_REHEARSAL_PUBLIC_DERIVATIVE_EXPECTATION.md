# Private Rehearsal Public Derivative Expectation

## Decision

Prepare a descriptor-only expectation for the future sanitized public
derivative that may be produced after an operator-approved private peer
rehearsal.

This artifact does not create the derivative. It defines the public-safe shape,
redaction rules, and Manifold/Hostess gates that a future derivative must
satisfy before it can be submitted for Manifold review.

## Scope

- source private rehearsal evidence expectation;
- expected sanitized derivative schema shape;
- allowed summary fields and prohibited private fields;
- required redaction results;
- Manifold handoff gate;
- Hostess escalation boundary;
- local validation commands and damaged-fixture policy.

## Non-Scope

No operator approval, private evidence, public derivative artifact, live Quest,
ADB, socket, endpoint discovery, remote desktop, file copy, install, launch,
recovery, command relay, raw log capture, visual capture, Manifold repo change,
Hostess repo change, Studio, Makepad, PMD, Polar, controller, or public
Rusty-XR runtime change is added by this slice.

## Authority

The sidecar may define the expected public-safe derivative shape. The operator
owns redaction review after a future private evidence pass.

Manifold remains the future command/session/audit, handoff acceptance, and
accepted-state authority. Hostess remains a future operator-recovery lane that
can act only from Manifold accepted state or an explicit operator request.

## Public Shape

A future public derivative may contain only sanitized summaries such as
participant counts, message class, route health, stale peer count, cleanup
status, redaction status, rejected input classes, and validation evidence.

It must reject endpoint values, pairing material, ADB details, command text,
raw logs, visual captures, package identifiers, and private device identifiers.

## Validation

```powershell
python tools\prepare_private_rehearsal_public_derivative_expectation.py --evidence-expectation fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json --now 2026-06-05T00:00:00Z --output fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json
python tools\prepare_manifold_public_derivative_schema_request.py --public-derivative-expectation fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json --now 2026-06-05T00:08:00Z --output fixtures\valid\manifold-public-derivative-schema-request.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Next Slice

The next data-only slice is
`manifold_public_derivative_schema_request`: a sidecar-owned request artifact
for future Manifold repo review. It must not define live Manifold routes or
Hostess actions inside this repo.
