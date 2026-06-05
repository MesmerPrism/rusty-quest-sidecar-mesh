#!/usr/bin/env python3
"""Generate a handoff review for the offline no-network prototype outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


HANDOFF_REVIEW_SCHEMA = "rusty.quest.sidecar.no_network_prototype_handoff_review.v1"
OBSERVATION_SCHEMA = "rusty.quest.sidecar.observation.v1"
RUN_SCHEMA = "rusty.quest.sidecar.no_network_agent_run.v1"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=2)
        handle.write("\n")


def relative_output_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def check(check_id: str, passed: bool, observed: Any, expected: Any, evidence: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "pass" if passed else "fail",
        "observed": observed,
        "expected": expected,
        "evidence": evidence,
    }


def build_review(observation_path: Path, run_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    observation = load_json(observation_path)
    run = load_json(run_path)
    observation_result = validate_repo.validate_json_file(observation_path)
    run_result = validate_repo.validate_json_file(run_path)

    manifold_ready = run.get("handoff_readiness", {}).get("manifold_observation_intake", {})
    hostess_ready = run.get("handoff_readiness", {}).get("hostess_operator_recovery", {})

    integration_status = {
        "manifold_repo_touched": False,
        "hostess_repo_touched": False,
        "live_device_used": False,
        "runtime_route_created": False,
        "hostess_route_created": False,
    }
    manifold_mapping = {
        "mapping_id": "mapping.no_network_observation_to_manifold_intake.synthetic.001",
        "status": "candidate",
        "authority_owner": "rusty.manifold",
        "audit_owner": "rusty.manifold.audit",
        "source_schema": OBSERVATION_SCHEMA,
        "source_path": relative_output_path(observation_path, repo_root),
        "source_role": "proposal_input",
        "proposed_intake_fields": {
            "source_agent_id": observation.get("source_agent_id"),
            "observed_agent_id": observation.get("observed_agent_id"),
            "observed_at": observation.get("observed_at"),
            "status": observation.get("status"),
            "truth_level": observation.get("advisory", {}).get("truth_level"),
            "transport_mode": observation.get("transport", {}).get("mode"),
            "redaction_class": observation.get("redaction", {}).get("privacy_class"),
        },
        "proposed_audit_fields": {
            "run_id": run.get("run_id"),
            "prototype_status": run.get("prototype_status"),
            "observation_id": observation.get("observation_id"),
            "acceptance_status": "not_implemented",
            "accepted_state_owner": "rusty.manifold",
        },
        "rejection_terms": [
            "stale_observation",
            "untrusted_sidecar",
            "redaction_incomplete",
            "forbidden_authority",
            "operator_approval_missing",
        ],
    }
    hostess_mapping = {
        "mapping_id": "mapping.no_network_run_to_hostess_operator_recovery.synthetic.001",
        "status": "future_lane_not_requested",
        "role": "operator_recovery_after_manifold_acceptance",
        "device_action_authority": "not_in_sidecar",
        "source_schema": RUN_SCHEMA,
        "source_path": relative_output_path(run_path, repo_root),
        "input_role": "manifold_accepted_state_or_operator_request",
        "request_descriptor_fields": {
            "source_run_id": run.get("run_id"),
            "required_authority": "rusty.manifold_or_operator",
            "allowed_action_class": "operator_recovery_request_descriptor",
            "implementation_status": "not_implemented",
        },
        "rejection_terms": [
            "manifold_acceptance_missing",
            "operator_request_missing",
            "sidecar_device_action_forbidden",
        ],
    }

    checks = [
        check(
            "handoff.observation_valid",
            observation_result.ok
            and observation.get("schema") == OBSERVATION_SCHEMA
            and observation.get("advisory", {}).get("truth_level") == "advisory_cached_view"
            and observation.get("redaction", {}).get("contains_endpoint_values") is False,
            {
                "schema": observation.get("schema"),
                "truth_level": observation.get("advisory", {}).get("truth_level"),
                "contains_endpoint_values": observation.get("redaction", {}).get("contains_endpoint_values"),
            },
            {
                "schema": OBSERVATION_SCHEMA,
                "truth_level": "advisory_cached_view",
                "contains_endpoint_values": False,
            },
            relative_output_path(observation_path, repo_root),
        ),
        check(
            "handoff.run_valid",
            run_result.ok
            and run.get("schema") == RUN_SCHEMA
            and run.get("prototype_status") == "prototype_complete"
            and run.get("summary", {}).get("fail_count") == 0,
            {
                "schema": run.get("schema"),
                "prototype_status": run.get("prototype_status"),
                "fail_count": run.get("summary", {}).get("fail_count"),
            },
            {
                "schema": RUN_SCHEMA,
                "prototype_status": "prototype_complete",
                "fail_count": 0,
            },
            relative_output_path(run_path, repo_root),
        ),
        check(
            "handoff.manifold_mapping_candidate",
            manifold_ready.get("authority_owner") == "rusty.manifold"
            and manifold_ready.get("audit_owner") == "rusty.manifold.audit"
            and manifold_mapping["status"] == "candidate"
            and manifold_mapping["proposed_audit_fields"]["acceptance_status"] == "not_implemented",
            {
                "authority_owner": manifold_ready.get("authority_owner"),
                "audit_owner": manifold_ready.get("audit_owner"),
                "mapping_status": manifold_mapping["status"],
                "acceptance_status": manifold_mapping["proposed_audit_fields"]["acceptance_status"],
            },
            {
                "authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "mapping_status": "candidate",
                "acceptance_status": "not_implemented",
            },
            "future Manifold intake/audit mapping remains proposal-only",
        ),
        check(
            "handoff.hostess_mapping_future_only",
            hostess_ready.get("status") == "future_lane_not_requested"
            and hostess_ready.get("device_action_authority") == "not_in_sidecar"
            and hostess_mapping["status"] == "future_lane_not_requested"
            and hostess_mapping["device_action_authority"] == "not_in_sidecar",
            {
                "source_status": hostess_ready.get("status"),
                "source_device_action_authority": hostess_ready.get("device_action_authority"),
                "mapping_status": hostess_mapping["status"],
                "mapping_device_action_authority": hostess_mapping["device_action_authority"],
            },
            {
                "source_status": "future_lane_not_requested",
                "source_device_action_authority": "not_in_sidecar",
                "mapping_status": "future_lane_not_requested",
                "mapping_device_action_authority": "not_in_sidecar",
            },
            "future Hostess operator-recovery mapping remains descriptor-only",
        ),
        check(
            "handoff.no_live_integration",
            not any(integration_status.values()),
            integration_status,
            {
                "manifold_repo_touched": False,
                "hostess_repo_touched": False,
                "live_device_used": False,
                "runtime_route_created": False,
                "hostess_route_created": False,
            },
            "handoff review does not touch live repos or runtime routes",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    return {
        "schema": HANDOFF_REVIEW_SCHEMA,
        "review_id": "review.no_network_prototype_handoff.synthetic.001",
        "generated_at": now,
        "review_status": "handoff_review_ready" if fail_count == 0 else "blocked",
        "source_observation": {
            "path": relative_output_path(observation_path, repo_root),
            "schema": observation.get("schema"),
            "observation_id": observation.get("observation_id"),
            "truth_level": observation.get("advisory", {}).get("truth_level"),
        },
        "source_run": {
            "path": relative_output_path(run_path, repo_root),
            "schema": run.get("schema"),
            "run_id": run.get("run_id"),
            "prototype_status": run.get("prototype_status"),
        },
        "integration_status": integration_status,
        "manifold_mapping": manifold_mapping,
        "hostess_mapping": hostess_mapping,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": len(checks) - fail_count,
            "manual_review_count": 0,
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "The no-network prototype handoff review is mapping evidence only.",
            "The review does not add Manifold routes, Hostess routes, live Quest work, ADB, network transport, install, launch, recovery, remote desktop control, file copy, or command execution.",
            "Manifold remains the future owner of acceptance, rejection, revision, lease, and audit records; Hostess remains a future operator-recovery lane after Manifold acceptance or explicit operator request.",
        ],
        "next_gate": "private_configured_peer_rehearsal_requires_operator_approval",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observation", required=True, help="Generated no-network observation fixture.")
    parser.add_argument("--run", required=True, help="Generated no-network prototype run fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output handoff review path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        review = build_review(Path(args.observation), Path(args.run), repo_root, args.now)
        write_json(Path(args.output), review)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"review_no_network_prototype_handoff failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": review["review_status"], "check_count": review["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

