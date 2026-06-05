# No-Network Agent Prototype

## Decision

Add a private no-network Termux Python prototype as an offline generator, not as
a service.

The prototype reads the no-network recipe and recipe review fixtures, writes one
`rusty.quest.sidecar.observation.v1` file, writes one
`rusty.quest.sidecar.no_network_agent_run.v1` report, then exits.

## Scope

- standard-library Python only;
- local fixture input only;
- local JSON file output only;
- one low-rate advisory observation;
- one run report that records no-network, no-ADB, no-command boundaries;
- one future handoff-readiness block for Manifold observation intake/audit and
  Hostess operator recovery routing.

## Non-Scope

No Quest device, ADB, Hostess, Studio, Makepad, PMD, Polar, controller, socket,
endpoint discovery, central polling, peer discovery, install, launch, recovery,
remote desktop, file copy, or Manifold mutation is touched.

## Authority

The generated observation remains proposal input. The run report is local
evidence only. Manifold remains the future owner of acceptance, rejection,
revision, leases, and audit records. Hostess remains a future operator/recovery
lane that may act only after Manifold acceptance or explicit operator request;
the sidecar does not gain device-action authority.

## Validation

```powershell
python tools\run_no_network_agent.py --recipe fixtures\valid\no-network-agent-recipe.synthetic.json --review fixtures\valid\no-network-agent-recipe-review.synthetic.json --now 2026-06-04T22:12:00Z --sequence 2 --observation-output fixtures\valid\no-network-agent-observation.synthetic.json --report-output fixtures\valid\no-network-agent-run.synthetic.json
python tools\review_no_network_prototype_handoff.py --observation fixtures\valid\no-network-agent-observation.synthetic.json --run fixtures\valid\no-network-agent-run.synthetic.json --now 2026-06-04T22:18:00Z --output fixtures\valid\no-network-prototype-handoff-review.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
