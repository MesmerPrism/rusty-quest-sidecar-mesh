# Public Lab Artifact Drift Review

## Decision

Review the public-safe `quest-termux-lab` intake for drift before using it as
future Manifold handoff evidence.

The drift review regenerates a sanitized status summary from declared manifest
paths and compares it with the stored sidecar intake report. It does not copy
raw artifacts, execute source validation, read private evidence, or promote
live readiness.

## Scope

- declared public-lab manifest pointer;
- stored sidecar intake report pointer;
- per-artifact schema, status-class, source-status, and summary comparison;
- proof that expected blocked lanes remain expected blocked;
- privacy and authority boundary checks.

## Non-Scope

No private evidence intake, raw log read, screenshot read, endpoint capture,
ADB, command execution, source validation execution, file copy, live Quest,
Hostess route, Manifold route, accepted Manifold state, Studio, Makepad, PMD,
Polar, controller, or public Rusty-XR runtime change is added.

## Authority

The drift review is advisory evidence. Manifold remains the future owner of
acceptance, rejection, revision, leases, and audit records. Hostess remains a
future operator/recovery lane only after Manifold accepted state or explicit
operator request.

## Validation

```powershell
python tools\review_public_lab_artifact_drift.py --manifest fixtures\valid\public-lab-artifact-intake-manifest.synthetic.json --report fixtures\valid\public-lab-artifact-intake-report.synthetic.json --source-root ..\quest-termux-lab --now 2026-06-04T21:43:00Z --output fixtures\valid\public-lab-artifact-drift-review.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
