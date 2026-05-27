# Plugin Evals

Evaluates skill content quality by simulating Claude Code skill injection:
loads a `SKILL.md` as the system context, sends a test prompt, then checks
the response against pattern matchers and a judge rubric.

## Setup

```bash
cd evals
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## Running

```bash
# all scenarios
python run.py

# filter by plugin
python run.py agentkit
python run.py saaskit

# filter by scenario id substring
python run.py testing-auth-setup
python run.py code-doctor

# show full responses
python run.py --verbose
python run.py agentkit --verbose
```

Exit code is `0` if all scenarios pass, `1` if any fail. Results are saved
to `evals/results/latest.json` after each run.

## Adding scenarios

Create a YAML file under `scenarios/<plugin>/`:

```yaml
id: unique-scenario-id
skill: plugins/<plugin>/skills/<skill>/SKILL.md
prompt: |
  The user message to send.
expected:
  code_patterns:
    - strings that must appear in the response
  forbidden_patterns:
    - strings that must NOT appear in the response
  rubric:
    - Plain-language criteria evaluated by a judge model
```

**`code_patterns`** and **`forbidden_patterns`** are fast, deterministic string checks.
Use them for env var names, SDK imports, package names — things with exact spellings.

**`rubric`** items are evaluated by a second Claude call. Use them for semantic
correctness: flow completeness, security posture, concept explanation quality.

## Structure

```
evals/
  run.py              Eval runner
  requirements.txt    anthropic, pyyaml
  scenarios/
    agentkit/         AgentKit plugin scenarios
    saaskit/          SaaSKit plugin scenarios
  results/
    latest.json       Results from the last run (gitignored)
    .gitkeep
```

## How it works

1. Loads `SKILL.md` as a cached system prompt (uses prompt caching to save tokens
   when running multiple scenarios against the same skill)
2. Sends the scenario prompt as the user turn
3. Runs pattern checks on the response (fast, deterministic)
4. Sends the response to a judge model with the rubric items
5. Reports pass/fail per check and overall score
