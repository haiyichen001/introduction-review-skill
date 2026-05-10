#!/usr/bin/env python3
"""
Real-time streaming citation dashboard.
Outputs one line at a time with flush() + delay ->designed for Monitor streaming.

Usage:
    python cite_stream.py <input_file>
"""

import re
import sys
import json
import os
import time
from collections import OrderedDict

PLACEHOLDER_RE = re.compile(r'\[CITE:([a-zA-Z0-9_\-]+)\]')


def flush(line):
    """Print, flush, and pause so Monitor sends each line as a separate event."""
    sys.stdout.write(line + '\n')
    sys.stdout.flush()
    time.sleep(0.25)  # ensures Monitor treats each line as a separate event


def scan_order(text):
    """Return placeholders in order of first appearance."""
    seen = OrderedDict()
    for match in PLACEHOLDER_RE.finditer(text):
        key = match.group(1)
        if key not in seen:
            seen[key] = len(seen) + 1
    return seen


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    # Load paper metadata if available
    paper_info = {}
    info_file = os.path.join(os.path.dirname(__file__), 'paper_info.json')
    if os.path.exists(info_file):
        with open(info_file, 'r', encoding='utf-8') as f:
            paper_info = json.load(f)

    placeholders = scan_order(text)
    ordered_keys = list(placeholders.keys())
    total = len(placeholders)

    # === STEP 1: Scan ===
    flush(f'--- Citation Scan ({total} found) ---')
    for i, key in enumerate(ordered_keys):
        info = paper_info.get(key, {})
        label = info.get('label', key)
        year = info.get('year', '')
        line = f'  {placeholders[key]}. [CITE:{key}] ->{label}'
        if year:
            line += f' ({year})'
        flush(line)
    flush('')

    # === STEP 2: Mapping ===
    flush('--- Number Assignment ---')
    mapping = {}
    for key in ordered_keys:
        mapping[key] = placeholders[key]
        flush(f'  [{mapping[key]}] <- [CITE:{key}]')
    flush('')

    # === STEP 3: Numbered Text ===
    flush('--- Numbered Text ---')

    def replacer(match):
        key = match.group(1)
        num = mapping.get(key)
        return f'[{num}]' if num else match.group(0)

    numbered = PLACEHOLDER_RE.sub(replacer, text)
    for line in numbered.strip().split('\n'):
        if line.strip():
            flush(line)

    flush('')
    flush('--- Complete ---')
    flush(f'{total} citations mapped. [-JSON-]')
    flush(json.dumps({f'[CITE:{k}]': f'[{v}]' for k, v in mapping.items()}))


if __name__ == '__main__':
    main()
