#!/usr/bin/env python3
"""Import public-safe quest-termux-lab status summaries into a sidecar report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


READY_VALUES = {
    "package_ready",
    "review_ready",
    "file_drop_staging_ready",
    "file_drop_copy_dry_run_ready",
    "file_drop_inbox_intake_ready",
    "cleanup_plan_ready",
    "fixture_index_ready",
    "fixture_ready",
    "ready",
    "synthetic_ready",
    "topology_ready",
    "regression_clear",
}

BLOCKED_VALUES = {
    "blocked",
    "review_blocked",
    "not_ready",
    "topology_blocked",
    "redaction_blocked",
    "import_blocked",
    "result_placeholders_blocked",
    "acceptance_blocked",
    "rejected",
    "untrusted",
}

MANUAL_VALUES = {
    "manual_review",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=2)
        handle.write("\n")


def require_relative_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        raise ValueError(f"artifact path must be relative: {raw_path}")
    if ".." in path.parts:
        raise ValueError(f"artifact path must not contain '..': {raw_path}")
    return path


def value_at_path(document: Any, dotted_path: str) -> Any:
    current = document
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise KeyError(f"missing status field: {dotted_path}")
        current = current[part]
    return current


def classify_status(value: Any) -> str:
    text = str(value)
    if text in READY_VALUES:
        return "ready"
    if text in BLOCKED_VALUES:
        return "blocked"
    if text in MANUAL_VALUES:
        return "manual_review"
    return "manual_review"


def summarize_artifact(ref: dict[str, Any], source_root: Path) -> dict[str, Any]:
    relative_path = require_relative_path(ref["path"])
    source_path = source_root / relative_path
    if not source_path.exists():
        status = "failed" if ref.get("required", True) else "manual_review"
        return {
            "artifact_id": ref["artifact_id"],
            "artifact_kind": ref["artifact_kind"],
            "path": ref["path"],
            "expected_schema": ref["expected_schema"],
            "observed_schema": "",
            "status_field": ref["status_field"],
            "source_status": "missing",
            "expected_status_class": ref["expected_status_class"],
            "observed_status_class": "missing",
            "status": status,
            "required": bool(ref.get("required", True)),
            "summary": {},
        }

    document = load_json(source_path)
    observed_schema = document.get("schema", "")
    try:
        source_status = value_at_path(document, ref["status_field"])
    except KeyError:
        source_status = "missing"
    observed_class = classify_status(source_status)

    status = "passed"
    if observed_schema != ref["expected_schema"]:
        status = "failed" if ref.get("required", True) else "manual_review"
    elif observed_class != ref["expected_status_class"]:
        status = "failed" if ref.get("required", True) else "manual_review"

    return {
        "artifact_id": ref["artifact_id"],
        "artifact_kind": ref["artifact_kind"],
        "path": ref["path"],
        "expected_schema": ref["expected_schema"],
        "observed_schema": observed_schema,
        "status_field": ref["status_field"],
        "source_status": source_status,
        "expected_status_class": ref["expected_status_class"],
        "observed_status_class": observed_class,
        "status": status,
        "required": bool(ref.get("required", True)),
        "summary": document.get("summary", {}),
    }


def build_report(manifest: dict[str, Any], source_root: Path, now: str) -> dict[str, Any]:
    if manifest.get("schema") != "rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1":
        raise ValueError("manifest schema must be rusty.quest.sidecar.public_lab_artifact_intake_manifest.v1")

    artifacts = [summarize_artifact(ref, source_root) for ref in manifest["artifact_refs"]]
    failed = [artifact for artifact in artifacts if artifact["status"] == "failed"]
    manual = [artifact for artifact in artifacts if artifact["status"] == "manual_review"]
    ready = [artifact for artifact in artifacts if artifact["observed_status_class"] == "ready"]
    expected_blocked = [
        artifact
        for artifact in artifacts
        if artifact["observed_status_class"] == "blocked" and artifact["expected_status_class"] == "blocked"
    ]
    missing_required = [
        artifact
        for artifact in artifacts
        if artifact["required"] and artifact["observed_status_class"] == "missing"
    ]
    schema_mismatches = [
        artifact
        for artifact in artifacts
        if artifact["observed_schema"] and artifact["observed_schema"] != artifact["expected_schema"]
    ]
    status_mismatches = [
        artifact
        for artifact in artifacts
        if artifact["observed_status_class"] != artifact["expected_status_class"]
    ]

    if failed:
        overall_status = "intake_blocked"
    elif manual:
        overall_status = "manual_review"
    else:
        overall_status = "intake_ready"

    return {
        "schema": "rusty.quest.sidecar.public_lab_artifact_intake_report.v1",
        "intake_id": manifest["intake_id"],
        "generated_at": now,
        "source_repo": manifest["source_repo"],
        "overall_status": overall_status,
        "artifacts": artifacts,
        "summary": {
            "artifact_count": len(artifacts),
            "required_artifact_count": sum(1 for artifact in artifacts if artifact["required"]),
            "passed_count": sum(1 for artifact in artifacts if artifact["status"] == "passed"),
            "failed_count": len(failed),
            "manual_review_count": len(manual),
            "ready_artifact_count": len(ready),
            "expected_blocked_artifact_count": len(expected_blocked),
            "missing_required_count": len(missing_required),
            "schema_mismatch_count": len(schema_mismatches),
            "status_mismatch_count": len(status_mismatches),
        },
        "redaction": {
            "privacy_class": "public_safe_synthetic",
            "contains_endpoint_values": False,
            "contains_commands": False,
            "contains_pairing_material": False,
            "contains_raw_logs": False,
            "contains_image_captures": False,
        },
        "authority_boundary": manifest["authority_boundary"],
        "manifold_handoff_role": "proposal_evidence_only",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Public lab intake manifest.")
    parser.add_argument("--source-root", required=True, help="quest-termux-lab repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output report path.")
    args = parser.parse_args(argv)

    try:
        manifest = load_json(Path(args.manifest))
        report = build_report(manifest, Path(args.source_root).resolve(), args.now)
        write_json(Path(args.output), report)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"import_public_lab_status failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": report["overall_status"], "artifact_count": report["summary"]["artifact_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
