#!/usr/bin/env python3
"""
Eval runner for claude-code-authstack plugins.

Simulates Claude Code skill injection: loads SKILL.md as system context,
sends a test prompt, checks the response against patterns and a judge rubric.

Usage:
  python run.py                    # run all scenarios
  python run.py agentkit           # filter by plugin name
  python run.py testing-auth-setup # filter by scenario id substring
  python run.py --verbose          # show full responses
"""

import json
import re
import sys
from pathlib import Path

import anthropic
import yaml

REPO_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = Path(__file__).parent / "scenarios"
RESULTS_DIR = Path(__file__).parent / "results"
MODEL = "claude-sonnet-4-6"

client = anthropic.Anthropic()


def load_skill(skill_path: str) -> str:
    path = REPO_ROOT / skill_path
    if not path.exists():
        raise FileNotFoundError(f"Skill not found: {skill_path}")
    return path.read_text()


def load_scenario(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def generate(skill_content: str, prompt: str) -> tuple[str, dict]:
    """Call Claude with skill as cached system context. Returns (response_text, usage)."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": skill_content,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_read": getattr(response.usage, "cache_read_input_tokens", 0),
        "cache_write": getattr(response.usage, "cache_creation_input_tokens", 0),
    }
    return response.content[0].text, usage


def check_patterns(response: str, expected: dict) -> dict[str, bool]:
    results = {}
    for pattern in expected.get("code_patterns", []):
        results[f"contains: {pattern}"] = pattern in response
    for pattern in expected.get("forbidden_patterns", []):
        results[f"forbidden: {pattern}"] = pattern not in response
    return results


def judge(response: str, rubric: list[str]) -> dict[str, bool]:
    """Ask Claude to evaluate the response against the rubric. Returns pass/fail per item."""
    if not rubric:
        return {}

    items = "\n".join(f"{i+1}. {item}" for i, item in enumerate(rubric))
    prompt = f"""Evaluate this response against each rubric item. Return a JSON object where each key is the rubric item (exact text) and the value is true (passes) or false (fails). Return only valid JSON, nothing else.

Response to evaluate:
<response>
{response}
</response>

Rubric:
{items}"""

    result = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    text = result.content[0].text.strip()

    # strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        raw = json.loads(text)
        # normalise: match rubric items by position if keys differ
        if len(raw) == len(rubric):
            return dict(zip(rubric, raw.values()))
        return {item: raw.get(item, False) for item in rubric}
    except json.JSONDecodeError:
        return {item: False for item in rubric}


def run_scenario(scenario_path: Path, verbose: bool = False) -> dict:
    scenario = load_scenario(scenario_path)
    skill_content = load_skill(scenario["skill"])
    expected = scenario.get("expected", {})

    response, usage = generate(skill_content, scenario["prompt"])
    pattern_results = check_patterns(response, expected)
    judge_results = judge(response, expected.get("rubric", []))

    all_checks = {**pattern_results, **judge_results}
    passed_count = sum(1 for v in all_checks.values() if v)
    total_count = len(all_checks)

    return {
        "id": scenario["id"],
        "skill": scenario["skill"],
        "prompt": scenario["prompt"],
        "response": response if verbose else response[:300] + "…",
        "checks": all_checks,
        "score": f"{passed_count}/{total_count}",
        "passed": all(all_checks.values()),
        "usage": usage,
    }


def print_result(result: dict, verbose: bool = False) -> None:
    status = "✓ PASS" if result["passed"] else "✗ FAIL"
    print(f"  {status}  ({result['score']})  {result['id']}")
    for check, ok in result["checks"].items():
        if not ok:
            print(f"         FAIL: {check}")
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
    total_tokens = 0

    for path in scenario_files:
        plugin = path.parent.name
        print(f"\n[{plugin}] {path.stem}")
        try:
            result = run_scenario(path, verbose=verbose)
            results.append(result)
            print_result(result, verbose=verbose)
            total_tokens += result["usage"]["input_tokens"] + result["usage"]["output_tokens"]
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({"id": path.stem, "passed": False, "error": str(e)})

    # summary
    passed = sum(1 for r in results if r.get("passed"))
    total = len(results)
    print(f"\n{'─'*40}")
    print(f"  {passed}/{total} scenarios passed  (~{total_tokens:,} tokens used)")

    # save results
    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / "latest.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to evals/results/latest.json")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
