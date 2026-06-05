#!/usr/bin/env python3
"""Generate a data-only review report for the no-network Termux agent recipe."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import validate_repo


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=2)
        handle.write("\n")


def check(check_id: str, passed: bool, observed: Any, expected: Any, evidence: str) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "status": "pass" if passed else "fail",
        "observed": observed,
        "expected": expected,
        "evidence": evidence,
    }


def relative_output_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def build_review(recipe_path: Path, repo_root: Path, now: str) -> dict[str, Any]:
    recipe = load_json(recipe_path)
    validation_result = validate_repo.validate_json_file(recipe_path)

    profile = recipe.get("implementation_profile", {})
    authority = recipe.get("authority", {})
    execution = recipe.get("execution", {})
    local_files = recipe.get("local_files", {})
    emissions = recipe.get("emissions", [])
    forbidden_surfaces = set(recipe.get("forbidden_surfaces", []))
    validation_slots = recipe.get("validation_slots", [])

    required_forbidden_surfaces = {
        "inbound_listener",
        "central_polling",
        "peer_discovery",
        "peer_gossip_send",
        "adb_use",
        "install_launch",
        "recovery_action",
        "remote_desktop_control",
        "high_rate_payload",
    }
    validation_commands = {slot.get("command", "") for slot in validation_slots if isinstance(slot, dict)}
    missing_forbidden = sorted(required_forbidden_surfaces - forbidden_surfaces)

    checks = [
        check(
            "recipe.schema_valid",
            validation_result.ok,
            "ok" if validation_result.ok else validation_result.errors,
            "ok",
            relative_output_path(recipe_path, repo_root),
        ),
        check(
            "recipe.termux_python_profile",
            profile.get("runtime") == "termux"
            and profile.get("language") == "python"
            and profile.get("profile_status") == "recipe_only",
            {
                "runtime": profile.get("runtime"),
                "language": profile.get("language"),
                "profile_status": profile.get("profile_status"),
            },
            {
                "runtime": "termux",
                "language": "python",
                "profile_status": "recipe_only",
            },
            "future implementation profile remains Termux/Python and recipe-only",
        ),
        check(
            "recipe.manifold_authority",
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
            "sidecar remains observer/proposer; Manifold owns future acceptance and audit",
        ),
        check(
            "recipe.no_network_no_adb_no_commands",
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
            "first runtime prototype must not carry network, ADB, or command authority",
        ),
        check(
            "recipe.relative_file_outputs",
            local_files.get("path_policy") == "relative_paths_only"
            and str(local_files.get("workspace_root", "")).startswith("relative:")
            and str(local_files.get("output_observation", "")).startswith("relative:"),
            {
                "workspace_root": local_files.get("workspace_root"),
                "output_observation": local_files.get("output_observation"),
                "path_policy": local_files.get("path_policy"),
            },
            "relative_paths_only",
            "recipe output stays in relative operator-selected or app-private storage shape",
        ),
        check(
            "recipe.low_rate_observation_emission",
            bool(emissions)
            and all(emission.get("schema") == "rusty.quest.sidecar.observation.v1" for emission in emissions)
            and all(emission.get("rate_class") == "low_rate" for emission in emissions)
            and all(emission.get("manifold_role") == "proposal_input" for emission in emissions),
            [
                {
                    "schema": emission.get("schema"),
                    "rate_class": emission.get("rate_class"),
                    "manifold_role": emission.get("manifold_role"),
                }
                for emission in emissions
            ],
            "low_rate sidecar observation proposal input",
            "future agent emits only low-rate advisory observation files",
        ),
        check(
            "recipe.forbidden_surfaces_declared",
            not missing_forbidden,
            missing_forbidden,
            [],
            "recipe declares forbidden surfaces before runtime code exists",
        ),
        check(
            "recipe.validation_slots_cover_gates",
            any("validate_repo.py" in command for command in validation_commands)
            and any("evaluate_integration_acceptance.py" in command for command in validation_commands),
            sorted(validation_commands),
            "validator and integration acceptance generator",
            "recipe validation slots keep the recipe covered by repo and integration gates",
        ),
    ]

    fail_count = sum(1 for row in checks if row["status"] == "fail")
    review_status = "ready_for_no_network_prototype" if fail_count == 0 else "blocked"

    return {
        "schema": "rusty.quest.sidecar.no_network_agent_recipe_review.v1",
        "review_id": "review.no_network_termux_agent.synthetic.001",
        "generated_at": now,
        "source_recipe": {
            "path": relative_output_path(recipe_path, repo_root),
            "recipe_id": recipe.get("recipe_id"),
            "recipe_schema": recipe.get("schema"),
            "profile_status": profile.get("profile_status"),
        },
        "review_status": review_status,
        "checks": checks,
        "summary": {
            "check_count": len(checks),
            "pass_count": len(checks) - fail_count,
            "manual_review_count": 0,
            "fail_count": fail_count,
        },
        "authority_boundary": [
            "The recipe review summarizes fixture evidence only.",
            "The recipe review does not approve live Quest work, open network transport, use ADB, execute commands, install apps, launch apps, recover devices, control remote desktops, or mutate Manifold state.",
            "The recipe review is proposal evidence; Manifold remains the future owner of acceptance, rejection, revision, lease, and audit records.",
        ],
        "next_gate": "private_no_network_termux_agent_prototype_without_transport_or_adb",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", required=True, help="No-network recipe JSON fixture.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--now", required=True, help="Deterministic generated_at timestamp.")
    parser.add_argument("--output", required=True, help="Output review JSON path.")
    args = parser.parse_args(argv)

    try:
        repo_root = Path(args.repo_root).resolve()
        review = build_review(Path(args.recipe), repo_root, args.now)
        write_json(Path(args.output), review)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"review_no_network_recipe failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"status": review["review_status"], "check_count": review["summary"]["check_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

