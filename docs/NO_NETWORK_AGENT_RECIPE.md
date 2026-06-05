# No-Network Agent Recipe

## Decision

Describe the future Termux agent prototype as a recipe before writing agent
runtime code.

The first recipe is no-network and no-ADB. It emits an observation fixture to a
local file path only. It does not start an inbound listener, poll a central
controller, use local ADB, copy files, or exchange peer gossip.

## Scope

The recipe records:

- Termux implementation profile;
- sidecar-only authority;
- local file input/output shape;
- bounded diagnostic loop assumptions;
- emitted observation schema;
- explicit forbidden surfaces.

## Non-Scope

No Python agent implementation is added in this slice. No Quest, ADB, Hostess,
Studio, Makepad, PMD, Polar, controller, socket, endpoint, install, launch,
recovery, or remote desktop route is touched.

## Authority

The recipe can only produce advisory observation files. Manifold remains the
future owner of acceptance, rejection, revision, leases, and audit records.

## Validation

```powershell
python tools\review_no_network_recipe.py --recipe fixtures\valid\no-network-agent-recipe.synthetic.json --now 2026-06-04T22:05:00Z --output fixtures\valid\no-network-agent-recipe-review.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
