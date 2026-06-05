# Manifold Public Derivative Schema Slice Response Expectation

## Decision

Prepare a descriptor-only expectation for the future Manifold-owned response to
the public derivative schema handoff package.

This artifact does not create a Manifold response, branch, schema, route,
accepted state, audit record, validation report, public derivative artifact, or
Hostess input. It defines the response envelope a later Manifold repo slice
should use when it accepts the handoff package, requests revisions, or rejects
it.

## Scope

- source Manifold public derivative schema handoff package pointer;
- response expectation scope proving no Manifold or Hostess artifact has been
  created;
- required Manifold-owned response fields;
- allowed decisions: `accepted_for_manifold_schema_slice`,
  `revision_requested`, and `rejected`;
- rejection, revision, audit, privacy, and validation terms;
- Hostess response gate requiring Manifold accepted state or an explicit
  operator request before Hostess can consume anything.

## Non-Scope

No Manifold repo change, branch, response, decision, schema, route, accepted
state, audit record, validation report, public derivative artifact, Hostess
route, Hostess input, live Quest work, ADB, socket, listener, endpoint
discovery, remote desktop, file copy, install, launch, recovery, Studio,
Makepad, PMD, Polar, controller, public Rusty-XR runtime, operator approval, or
private evidence is added.

## Authority

The sidecar repo owns this expectation as proposal evidence only. Manifold
remains the handoff acceptance, implementation plan, response, decision,
schema, route implementation, request acceptance, runtime/session,
accepted-state, rollback, revision, and audit authority.

Hostess remains a downstream operator/recovery lane. It may later consume
Manifold accepted state or an explicit operator request descriptor, but this
expectation cannot become direct Hostess device-action input.

## Hostess Gate

The fixture is Hostess-prepared but Hostess-inactive:

- no Hostess route is created;
- no recovery request is created;
- no sidecar direct input is allowed;
- Hostess consumption requires Manifold accepted state;
- Hostess action also requires an explicit operator request.

## Validation

```powershell
python tools\prepare_manifold_public_derivative_schema_slice_response_expectation.py --handoff-package fixtures\valid\manifold-public-derivative-schema-handoff-package.synthetic.json --now 2026-06-05T00:40:00Z --output fixtures\valid\manifold-public-derivative-schema-slice-response-expectation.synthetic.json
python tools\evaluate_integration_acceptance.py --repo-root . --now 2026-06-04T21:46:00Z --output fixtures\valid\integration-acceptance-scorecard.synthetic.json
python tools\validate_repo.py --repo-root .
python -m unittest discover -s tests -p test_*.py
git diff --check
```

## Next Gate

The next safe sidecar-only gate is the Manifold public derivative schema slice
response implementation preflight. It enumerates future Manifold-owned response
implementation artifacts without creating them. A later Hostess integration can
only consume Manifold accepted state or a separate explicit operator request
descriptor.
