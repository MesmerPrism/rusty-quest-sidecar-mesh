# Private Rehearsal Evidence Expectation

## Decision

Prepare a descriptor-only expectation for future operator-approved private peer
rehearsal evidence. This artifact defines what a private run may later produce
and what must be redacted before any Manifold handoff.

It does not approve a rehearsal, start a route, collect evidence, create a
public derivative, submit anything to Manifold, or create a Hostess route.

## Scope

- source private rehearsal approval request;
- source Hostess boundary descriptor expectation;
- private evidence requirements for an operator-approved run;
- public derivative requirements and required redaction results;
- Manifold handoff gate for a sanitized derivative;
- Hostess escalation boundary for future operator recovery;
- local validation commands and damaged-fixture policy.

## Non-Scope

No live Quest, ADB, socket, endpoint discovery, remote desktop, file copy,
install, launch, recovery, command relay, raw log capture, visual capture,
Manifold repo change, Hostess repo change, Studio, Makepad, PMD, Polar,
controller, or public Rusty-XR runtime change is added by this slice.

## Authority

The operator owns any future private evidence capture decision. The sidecar can
only prepare expectations and later propose sanitized derivatives.

Manifold remains the future command/session/audit, intake acceptance, and
accepted-state authority. Hostess remains a future operator-recovery lane that
can act only from Manifold accepted state or an explicit operator request.

## Public Derivative Gate

A future public derivative must omit endpoint values, pairing material, ADB,
commands, raw logs, visual captures, and private device identifiers. It must
state the redaction result before Manifold intake.

## Validation

```powershell
python tools\prepare_private_rehearsal_evidence_expectation.py --approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --hostess-expectation fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json --now 2026-06-04T23:52:00Z --output fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json
python tools\prepare_private_rehearsal_public_derivative_expectation.py --evidence-expectation fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json --now 2026-06-05T00:00:00Z --output fixtures\valid\private-rehearsal-public-derivative-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
