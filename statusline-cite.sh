#!/bin/bash
# Citation Dashboard Status Line for Claude Code (macOS/Linux)
# Reads state from /tmp/cite_live_state.txt

STATE_FILE="/tmp/cite_live_state.txt"

if [ -f "$STATE_FILE" ]; then
    mtime=$(stat -c %Y "$STATE_FILE" 2>/dev/null || stat -f %m "$STATE_FILE" 2>/dev/null || echo 0)
    now=$(date +%s 2>/dev/null || echo 0)
    if [ -n "$now" ] && [ "$mtime" != "0" ] && [ $((now - mtime)) -lt 30 ]; then
        cat "$STATE_FILE"
        exit 0
    fi
fi

# Fallback: show model + dir
input=$(cat 2>/dev/null)
model=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('model',{}).get('display_name','?'))" 2>/dev/null || echo "?")
dir=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('workspace',{}).get('current_dir','~').split('/')[-1] or '~')" 2>/dev/null || echo "~")
printf "\033[38;5;111m%s\033[0m  \033[38;5;214m%s\033[0m" "$model" "$dir"
