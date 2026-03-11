#!/bin/bash
SKILL="${1:-unknown}"
INPUT=$(cat)

SESSION_ID=$(echo "$INPUT" | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('session_id','anonymous'))" \
  2>/dev/null || echo "anonymous")

curl -s -o /dev/null --max-time 5 \
  -X POST https://ph.scalekit.com/i/v0/e/ \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"phc_85pLP8gwYvRCQdxgLQP24iqXHPRGaLgEw4S4dgZHJZ\",\
\"event\":\"plugin_skill_used\",\
\"distinct_id\":\"${SESSION_ID}\",\
\"properties\":{\"skill\":\"${SKILL}\",\"coding_agent\":\"claude_code\"}}"
