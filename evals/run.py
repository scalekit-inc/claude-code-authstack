#!/usr/bin/env python3
"""
Eval runner for claude-code-authstack plugins.

Uses `claude --plugin-dir` to load each plugin and run test prompts,
then judges responses with a second `claude` call. No API key needed —
reuses your existing Claude Code session.

Usage:
  python run.py                    # run all scenarios
  python run.py agentkit           # filter by plugin name
  python run.py testing-auth-setup # filter by scenario id substring
  python run.py --verbose          # show full responses
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = Path(__file__).parent / "scenarios"
RESULTS_DIR = Path(__file__).parent / "results"


def claude(args: list[str], prompt: str) -> str:
    """Run claude CLI and return stdout. Raises on non-zero exit."""
    result = subprocess.run(
        ["claude", *args, "-p", prompt, "--print"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "claude exited non-zero")
    return result.stdout.strip()


def generate(plugin: str, prompt: str) -> str:
    plugin_dir = str(REPO_ROOT / "plugins" / plugin)
    return claude(["--plugin-dir", plugin_dir], prompt)


def judge(response: str, rubric: list[str]) -> dict[str, bool]:
    if not rubric:
        return {}

    items = "\n".join(f"{i+1}. {item}" for i, item in enumerate(rubric))
    judge_prompt = f"""Evaluate this response against each rubric item. Return a JSON object where each key is the exact rubric item text and the value is true (passes) or false (fails). Return only valid JSON, nothing else.

Response to evaluate:
<response>
{response}
</response>

Rubric:
{items}"""

    raw = claude([], judge_prompt)
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw)

    try:
        parsed = json.loads(raw)
        # normalise by position if keys don't match exactly
        if len(parsed) == len(rubric):
            return dict(zip(rubric, parsed.values()))
        return {item: bool(parsed.get(item, False)) for item in rubric}
    except json.JSONDecodeError:
        return {item: False for item in rubric}


def check_patterns(response: str, expected: dict) -> dict[str, bool]:
    results = {}
    for pattern in expected.get("code_patterns", []):
        results[f"contains: {pattern}"] = pattern in response
    for pattern in expected.get("forbidden_patterns", []):
        results[f"forbidden: {pattern}"] = pattern not in response
    return results


def load_scenario(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def run_scenario(path: Path, verbose: bool = False) -> dict:
    scenario = load_scenario(path)
    plugin = scenario["plugin"]
    expected = scenario.get("expected", {})

    response = generate(plugin, scenario["prompt"])
    pattern_results = check_patterns(response, expected)
    judge_results = judge(response, expected.get("rubric", []))

    all_checks = {**pattern_results, **judge_results}
    passed_count = sum(1 for v in all_checks.values() if v)
    total_count = len(all_checks)

    return {
        "id": scenario["id"],
        "plugin": plugin,
        "prompt": scenario["prompt"],
        "response": response if verbose else response[:400] + "…",
        "checks": all_checks,
        "score": f"{passed_count}/{total_count}",
        "passed": all(all_checks.values()),
    }


def print_result(result: dict, verbose: bool = False) -> None:
    status = "✓ PASS" if result["passed"] else "✗ FAIL"
    print(f"  {status}  ({result['score']})  {result['id']}")
    for check, ok in result["checks"].items():
        if not ok:
            print(f"         ✗ {check}")
    if verbose:
        print(f"\n  Response:\n{result['response']}\n")


def main() -> None:
    args = sys.argv[1:]
    verbose = "--verbose" in args
    filter_terms = [a for a in args if not a.startswith("--")]

    scenario_files = sorted(SCENARIOS_DIR.rglob("*.yaml"))
    if filter_terms:
        scenario_files = [
            f for f in scenario_files
            if any(t in str(f) for t in filter_terms)
        ]

    if not scenario_files:
        print("No matching scenarios found.")
        sys.exit(1)

    results = []

    for path in scenario_files:
        plugin = path.parent.name
        print(f"\n[{plugin}] {path.stem}")
        try:
            result = run_scenario(path, verbose=verbose)
            results.append(result)
            print_result(result, verbose=verbose)
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"id": path.stem, "passed": False, "error": str(e)})

    passed = sum(1 for r in results if r.get("passed"))
    total = len(results)
    print(f"\n{'─' * 40}")
    print(f"  {passed}/{total} scenarios passed")

    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / "latest.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results → evals/results/latest.json")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
