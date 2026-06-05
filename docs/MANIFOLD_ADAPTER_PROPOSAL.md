# Manifold Adapter Proposal

## Decision

Describe the future Manifold adapter surface for Quest sidecar mesh work as a
proposal fixture. Do not implement a Manifold route yet.

## Scope

The proposal covers four low-rate surfaces:

- sidecar observation source descriptor;
- sidecar health stream descriptor;
- public lab intake review input;
- sidecar handoff acceptance command descriptor.

The later contract review covers the peer-status rehearsal adapter candidate in
more detail:

- peer status source descriptor;
- peer status intake descriptor;
- peer rehearsal audit descriptor;
- lifecycle, audit fields, rollback owner, and validation slots.

## Non-Scope

The proposal does not add runtime sockets, Manifold command handlers, leases,
Hostess execution, Studio UI, ADB, endpoint selection, install, launch, recovery
or remote desktop control.

## Authority

Manifold is the future owner of:

- accepting or rejecting a sidecar observation source;
- accepting or rejecting a sidecar health stream;
- accepting or rejecting handoff review requests;
- revisions, leases, and audit records.

The sidecar role remains observer/proposer. The adapter proposal is not
accepted state.

## Rejection Vocabulary

The first proposed rejection reasons are:

- `stale_observation`
- `untrusted_sidecar`
- `forbidden_authority`
- `redaction_incomplete`
- `operator_approval_missing`
- `endpoint_values_rejected`
- `high_rate_payload_rejected`
- `unsupported_transport`

These are proposal terms until Manifold owns a concrete acceptance command.

## Validation

```powershell
python tools\review_manifold_adapter_contract.py --peer-plan fixtures\valid\configured-peer-rehearsal-plan.synthetic.json --now 2026-06-04T22:32:00Z --output fixtures\valid\manifold-adapter-contract-review.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
