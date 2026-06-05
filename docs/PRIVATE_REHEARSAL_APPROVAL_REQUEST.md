# Private Rehearsal Approval Request

## Decision

Insert a descriptor-only approval request before any private configured peer
rehearsal. The request states what an operator would need to approve later,
while keeping endpoints, ADB, commands, Hostess routes, Manifold routes, and
accepted state out of this repo.

## Scope

- source configured peer rehearsal plan;
- source Manifold contract-intake request;
- operator approval packet status;
- required private inputs and sanitized public derivatives;
- Manifold authority owners and future validation gate;
- Hostess operator/recovery boundary as descriptor-only.
- downstream Manifold route blueprint boundary.

## Non-Scope

No operator approval is granted here. No live Quest, ADB, socket, listener,
remote desktop, file copy, install, launch, recovery, shell route, Manifold
route, Hostess route, Studio, Makepad, PMD, Polar, controller, or public
Rusty-XR runtime change is added by this slice.

## Authority

The operator owns the future private approval decision. Manifold remains the
future command/session/audit and accepted-state authority. Hostess remains a
future operator/recovery lane that can act only from Manifold accepted state or
explicit operator request. The sidecar remains an observer/proposer.

## Validation

```powershell
python tools\prepare_private_rehearsal_approval.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --now 2026-06-04T22:56:00Z --output fixtures\valid\private-rehearsal-approval-request.synthetic.json
python tools\prepare_private_rehearsal_evidence_expectation.py --approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --hostess-expectation fixtures\valid\hostess-boundary-descriptor-expectation.synthetic.json --now 2026-06-04T23:52:00Z --output fixtures\valid\private-rehearsal-evidence-expectation.synthetic.json
python tools\prepare_manifold_route_blueprint.py --contract-intake-request fixtures\valid\manifold-contract-intake-request.synthetic.json --private-approval-request fixtures\valid\private-rehearsal-approval-request.synthetic.json --now 2026-06-04T23:04:00Z --output fixtures\valid\manifold-route-blueprint.synthetic.json
python tools\prepare_manifold_route_design_review.py --route-blueprint fixtures\valid\manifold-route-blueprint.synthetic.json --now 2026-06-04T23:12:00Z --output fixtures\valid\manifold-route-design-review-request.synthetic.json
python tools\prepare_manifold_route_design_response_expectation.py --design-review-request fixtures\valid\manifold-route-design-review-request.synthetic.json --now 2026-06-04T23:20:00Z --output fixtures\valid\manifold-route-design-response-expectation.synthetic.json
python tools\prepare_manifold_response_implementation_preflight.py --response-expectation fixtures\valid\manifold-route-design-response-expectation.synthetic.json --now 2026-06-04T23:28:00Z --output fixtures\valid\manifold-response-implementation-preflight.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
