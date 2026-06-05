# Manifold Adapter Contract Review

## Decision

Translate the configured peer rehearsal plan into a future Manifold adapter
contract review before touching the Manifold repo.

This review is still private sidecar evidence. It names candidate Manifold
surfaces, audit fields, lifecycle states, rejection terms, and validation slots
that a future Manifold-owned route would need to implement. It does not create
that route.

## Scope

- sidecar peer status source descriptor;
- sidecar peer status intake descriptor;
- sidecar peer rehearsal audit descriptor;
- Manifold rejection terms for stale, untrusted, endpoint-bearing, command,
  ADB, and approval-missing inputs;
- Hostess operator-recovery boundary as descriptor-only;
- validation slots that future Manifold work must satisfy.

## Non-Scope

No Manifold repo change, Hostess repo change, live Quest, ADB, socket,
listener, endpoint discovery, remote desktop, file copy, install, launch,
recovery, Studio, Makepad, PMD, Polar, controller, public Rusty-XR runtime, or
accepted Manifold state is added.

## Authority

Manifold remains the owner of command/session authority, accepted mutable
state, revisions, leases, topology, and audit records. The sidecar repo can
only prepare candidate descriptors and rejection vocabulary. Hostess remains a
future operator/recovery lane after Manifold acceptance or explicit operator
request.

## Validation

```powershell
python tools\review_manifold_adapter_contract.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --now 2026-06-04T22:32:00Z --output fixtures\valid\manifold-adapter-contract-review.synthetic.json
python tools\package_manifold_handoff.py --contract-review fixtures\valid\manifold-adapter-contract-review.synthetic.json --now 2026-06-04T22:40:00Z --output fixtures\valid\manifold-handoff-package.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
