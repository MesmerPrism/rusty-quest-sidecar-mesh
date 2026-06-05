# Public Lab Artifact Intake

## Decision

Use a local, declared intake manifest to summarize public-safe
`quest-termux-lab` artifacts before they appear in a private Rusty Quest
sidecar handoff.

The intake is evidence plumbing only. It does not promote peer mesh readiness,
select private endpoints, approve a live run, or mutate Manifold state.

## Scope

The first intake reads these public-safe artifact categories:

- public package readiness report;
- preflight clear review bundle;
- baseline scorecard;
- file-drop copy dry run;
- file-drop inbox intake;
- private result placeholder status.

The importer extracts:

- artifact ID and kind;
- relative source path;
- expected and observed schema;
- one declared status field;
- observed status value;
- observed status class;
- summary counts when present.

## Non-Scope

The importer does not read private evidence, raw logs, screenshots, package
identities, endpoint values, pairing material, command records, or gossip bodies.
It does not execute the source lab validators or copy source artifacts.

## Authority

The intake report is an advisory evidence summary. A sidecar handoff can
reference it, but Manifold remains the only future owner of accepted command,
session, lease, registry, and audit state.

The drift review in `docs/PUBLIC_LAB_ARTIFACT_DRIFT_REVIEW.md` should be
regenerated after intake. It compares the stored intake report with current
sanitized source artifacts while preserving the same no-copy/no-execution
boundary.

## Validation

```powershell
python tools\import_public_lab_status.py --manifest fixtures\valid\public-lab-artifact-intake-manifest.synthetic.json --source-root ..\quest-termux-lab --now 2026-06-04T21:41:00Z --output fixtures\valid\public-lab-artifact-intake-report.synthetic.json
python tools\review_public_lab_artifact_drift.py --manifest fixtures\valid\public-lab-artifact-intake-manifest.synthetic.json --report fixtures\valid\public-lab-artifact-intake-report.synthetic.json --source-root ..\quest-termux-lab --now 2026-06-04T21:43:00Z --output fixtures\valid\public-lab-artifact-drift-review.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```
