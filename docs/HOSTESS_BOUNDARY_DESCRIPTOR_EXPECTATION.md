# Hostess Boundary Descriptor Expectation

## Decision

Prepare a descriptor-only expectation for the future Hostess boundary
descriptor that may follow a Manifold-accepted sidecar peer-status response
slice.

This artifact does not create a Hostess route. It defines the conditions a
future Manifold-owned descriptor must satisfy before Hostess can consume any
sidecar-mesh-derived state.

## Scope

- source Manifold response handoff package pointer;
- explicit proof that neither Manifold nor Hostess repos are touched;
- future ownership split between Manifold descriptor/accepted-state/audit
  authority and Hostess route ownership after enablement;
- required Hostess boundary descriptor fields;
- required Hostess-side validation slots;
- allowed read-only and operator-recovery descriptor classes;
- disallowed direct sidecar, endpoint, command, ADB, high-rate, raw-log,
  visual-capture, and pairing-material inputs;
- Manifold acceptance gate showing the current package is not accepted and no
  Hostess descriptor or route is ready.

## Non-Scope

No Hostess route, Hostess repo change, Manifold repo change, accepted state,
audit record, operator approval, live Quest, ADB, socket, listener, endpoint
discovery, remote desktop, file copy, install, launch, recovery, Studio,
Makepad, PMD, Polar, controller, public Rusty-XR runtime, or private evidence
is added.

## Authority

The sidecar repo owns this expectation as proposal evidence. Manifold remains
the source of truth, response decision, accepted-state, audit, and Hostess
route enablement authority.

Hostess remains the future route owner only after Manifold accepted state or an
explicit operator request exists. Sidecar agents remain observers/proposers and
cannot provide direct Hostess device-action input.

## Hostess Gate

The future Hostess boundary descriptor must:

- require Manifold accepted state;
- require an explicit operator request for recovery;
- reject direct sidecar peer messages as action input;
- reject endpoint values, commands, ADB, raw logs, visual captures, pairing
  material, and high-rate payloads;
- remain route-disabled until Manifold has accepted the response slice.

## Validation

```powershell
python tools\prepare_hostess_boundary_descriptor_expectation.py --response-handoff fixtures\valid\manifold-response-handoff-package.synthetic.json --now 2026-06-04T23:44:00Z --output fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json
python tools\prepare_private_rehearsal_evidence_expectation.py --approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --hostess-expectation fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json --now 2026-06-04T23:52:00Z --output fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
