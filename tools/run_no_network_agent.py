#!/usr/bin/env python3
"""Run the local no-network sidecar prototype and write JSON evidence files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


OBSERVATION_SCHEMA = "rusty.quest.sidecar.observation.v1"
RUN_SCHEMA = "rusty.quest.sidecar.no_network_agent_run.v1"
RECIPE_SCHEMA = "rusty.quest.sidecar.no_network_agent_recipe.v1"
REVIEW_SCHEMA = "rusty.quest.sidecar.no_network_agent_recipe_review.v1"


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


def build_observation(now: str, sequence: int, agent_id: str) -> dict[str, Any]:
    return {
        "schema": OBSERVATION_SCHEMA,
        "observation_id": f"observation.no_network.synthetic.{sequence:03d}",
        "source_agent_id": agent_id,
        "observed_agent_id": agent_id,
        "observed_at": now,
        "sequence": sequence,
        "status": "available",
        "transport": {
            "mode": "local_file_only",
            "route_id": "route.no_network.local_file",
            "scope": "synthetic_no_network",
        },
        "health": {
            "central_reachable": "not_checked",
            "local_python_available": True,
            "local_adb_available": "not_used",
            "battery_percent": "not_sampled",
            "last_command_status": "none",
        },
        "advisory": {
            "truth_level": "advisory_cached_view",
            "source_of_truth": "rusty.manifold_after_acceptance",
            "staleness_policy": "discard_after_30_seconds",
        },
        "redaction": {
            "privacy_class": "synthetic",
            "contains_endpoint_values": False,
            "contains_private_package_ids": False,
        },
    }


def build_run_report(
    recipe_path: Path,
    review_path: Path,
    observation_output: Path,
    repo_root: Path,
    now: str,
    observation: dict[str, Any],
    recipe: dict[str, Any],
    review: dict[str, Any],
) -> dict[str, Any]:
    recipe_result = validate_repo.validate_json_file(recipe_path)
    review_result = validate_repo.validate_json_file(review_path)
    observation_result = validate_repo.ValidationResult(Path("<pending-observation>"), True, validate_repo.validate_fixture(observation))

    execution = recipe.get("execution", {})
    authority = recipe.get("authority", {})
    review_summary = review.get("summary", {})

    checks = [
        check(
            "prototype.recipe_valid",
            recipe_result.ok and recipe.get("schema") == RECIPE_SCHEMA,
            "ok" if recipe_result.ok else recipe_result.errors,
            "ok",
            relative_output_path(recipe_path, repo_root),
        ),
        check(
            "prototype.review_ready",
            review_result.ok
            and review.get("schema") == REVIEW_SCHEMA
            and review.get("review_status") == "ready_for_no_network_prototype"
            and review_summary.get("fail_count") == 0,
            {
                "review_status": review.get("review_status"),
                "fail_count": review_summary.get("fail_count"),
            },
            {
                "review_status": "ready_for_no_network_prototype",
                "fail_count": 0,
            },
            relative_output_path(review_path, repo_root),
        ),
        check(
            "prototype.no_network_no_adb_no_commands",
            execution.get("network_policy") == "no_inbound_listener"
            and execution.get("outbound_transport_policy") == "disabled_for_recipe"
            and execution.get("adb_policy") == "no_adb"
            and execution.get("command_policy") == "no_commands",
            {
                "network_policy": execution.get("network_policy"),
                "outbound_transport_policy": execution.get("outbound_transport_policy"),
                "adb_policy": execution.get("adb_policy"),
                "command_policy": execution.get("command_policy"),
            },
            {
                "network_policy": "no_inbound_listener",
                "outbound_transport_policy": "disabled_for_recipe",
                "adb_policy": "no_adb",
                "command_policy": "no_commands",
            },
            "prototype inherits the reviewed recipe execution boundary",
        ),
        check(
            "prototype.manifold_authority_preserved",
            authority.get("role") == "sidecar_observer"
            and authority.get("acceptance_owner") == "rusty.manifold"
            and authority.get("audit_owner") == "rusty.manifold.audit"
            and authority.get("proposal_status") == "not_accepted",
            {
                "role": authority.get("role"),
                "acceptance_owner": authority.get("acceptance_owner"),
                "audit_owner": authority.get("audit_owner"),
                "proposal_status": authority.get("proposal_status"),
            },
            {
                "role": "sidecar_observer",
                "acceptance_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "proposal_status": "not_accepted",
            },
            "prototype can produce proposal input only",
        ),
        check(
            "prototype.observation_valid",
            observation_result.ok,
            "ok" if observation_result.ok else observation_result.errors,
            "ok",
            relative_output_path(observation_output, repo_root),
        ),
    ]
    fail_count = sum(1 for row in checks if row["status"] == "fail")

    return {
        "schema": RUN_SCHEMA,
        "run_id": "run.no_network_termux_agent.synthetic.001",
        "generated_at": now,
        "prototype_status": "prototype_complete" if fail_count == 0 else "blocked",
        "source_recipe": {
            "path": relative_output_path(recipe_path, repo_root),
            "recipe_id": recipe.get("recipe_id"),
            "recipe_schema": recipe.get("schema"),
        },
        "source_review": {
            "path": relative_output_path(review_path, repo_root),
            "review_id": review.get("review_id"),
            "review_schema": review.get("schema"),
            "review_status": review.get("review_status"),
        },
        "runtime": {
            "implementation_profile": "termux_python_standard_library",
            "execution_mode": "local_static_file_generation",
            "network_policy": "no_inbound_listener",
            "outbound_transport_policy": "disabled",
            "adb_policy": "no_adb",
            "command_policy": "no_commands",
        },
        "authority": {
            "role": "sidecar_observer",
            "mutation_policy": "write_observation_file_only",
            "acceptance_owner": "rusty.manifold",
            "audit_owner": "rusty.manifold.audit",
            "proposal_status": "not_accepted",
        },
        "handoff_readiness": {
            "manifold_observation_intake": {
                "status": "candidate",
                "authority_owner": "rusty.manifold",
                "audit_owner": "rusty.manifold.audit",
                "input_schema": OBSERVATION_SCHEMA,
                "input_role": "proposal_input",
            },
            "hostess_operator_recovery": {
                "status": "future_lane_not_requested",
                "role": "operator_recovery_after_manifold_acceptance",
                "device_action_authority": "not_in_sidecar",
                "input_role": "manifold_accepted_state_or_operator_request",
            },
        },
        "outputs": {
            "observation_path": relative_output_path(observation_output, repo_root),
            "observation_schema": observation.get("schema"),
            "observation_id": observation.get("observation_id"),
            "emission_rate_class": "low_rate",
        },
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": len(checks) - fail_count,
            "manual_review_count": 0,
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "The no-network prototype writes local JSON evidence only.",
            "The no-network prototype does not open network transport, use ADB, execute commands, install apps, launch apps, recover devices, control remote desktops, copy files, or mutate Manifold state.",
            "The generated observation is proposal input; Manifold remains the future owner of acceptance, rejection, revision, lease, and audit records.",
        ],
        "next_gate": "no_network_prototype_handoff_review_before_configured_peer_rehearsal",
    }


def build_outputs(
    recipe_path: Path,
    review_path: Path,
    observation_output: Path,
    repo_root: Path,
    now: str,
    sequence: int,
    agent_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    recipe = load_json(recipe_path)
    review = load_json(review_path)
    observation = build_observation(now, sequence, agent_id)
    report = build_run_report(recipe_path, review_path, observation_output, repo_root, now, observation, recipe, review)
    return observation, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", required=True, help="No-network recipe JSON fixture.")
    parser.add_argument("--review", required=True, help="No-network recipe review JSON fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic timestamp.")
    parser.add_argument("--sequence", type=int, default=1, help="Observation sequence number.")
    parser.add_argument("--agent-id", default="agent.quest_sidecar.synthetic_alpha", help="Synthetic sidecar agent id.")
    parser.add_argument("--observation-output", required=True, help="Observation output path.")
    parser.add_argument("--report-output", required=True, help="Run report output path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        observation_output = Path(args.observation_output)
        report_output = Path(args.report_output)
        observation, report = build_outputs(
            Path(args.recipe),
            Path(args.review),
            observation_output,
            repo_root,
            args.now,
            args.sequence,
            args.agent_id,
        )
        write_json(observation_output, observation)
        write_json(report_output, report)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"run_no_network_agent failed: {exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": report["prototype_status"],
                "observation_id": observation["observation_id"],
                "check_count": report["summary"]["check_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
