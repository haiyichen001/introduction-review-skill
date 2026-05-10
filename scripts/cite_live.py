#!/usr/bin/env python3
"""
Citation mapping dashboard — scans [CITE:xxx] placeholders and displays
progressive tables showing scan order, number assignment, and final text.

Usage:
    python cite_live.py <input_file>
    echo "text with [CITE:xxx]..." | python cite_live.py
"""

import re
import sys
import json
import os
from collections import OrderedDict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

PLACEHOLDER_RE = re.compile(r'\[CITE:([a-zA-Z0-9_\-]+)\]')


def scan_order(text):
    """Return placeholders in order of first appearance."""
    seen = OrderedDict()
    for match in PLACEHOLDER_RE.finditer(text):
        key = match.group(1)
        if key not in seen:
            seen[key] = len(seen) + 1
    return seen


def _t(text, **kwargs):
    """Wrap plain text to avoid rich markup parsing issues with brackets."""
    return Text(text, **kwargs)


def main():
    console = Console()

    # Read input
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
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
    mapping = {}
    ordered_keys = list(placeholders.keys())
    total = len(placeholders)

    # === STEP 1: Placeholder scan ===
    scan_table = Table(
        title='[bold cyan]Step 1/3: Citation Scan[/]',
        caption=f'Found {total} unique placeholders in text',
        border_style='bright_black',
    )
    scan_table.add_column('Order', style='cyan', width=6)
    scan_table.add_column('Placeholder', style='yellow', width=28)
    for i, key in enumerate(ordered_keys):
        scan_table.add_row(str(placeholders[key]), f'[CITE:{key}]')
    console.print(scan_table)
    console.print()

    # === STEP 2: Number assignment ===
    map_table = Table(
        title='[bold cyan]Step 2/3: Number Assignment[/]',
        caption='Numbers assigned by first-appearance order',
        border_style='bright_black',
    )
    map_table.add_column('#', style='bold green', width=5)
    map_table.add_column('Key', style='dim yellow', width=22)
    map_table.add_column('Paper', style='white', width=38)
    map_table.add_column('Meta', style='dim', width=15)

    for key in ordered_keys:
        mapping[key] = placeholders[key]
        info = paper_info.get(key, {})
        paper_label = info.get('label', key)
        meta = info.get('year', '')
        map_table.add_row(
            str(mapping[key]),
            f'[CITE:{key}]',
            paper_label,
            meta,
        )
    console.print(map_table)
    console.print()

    # === STEP 3: Replacement + numbered text ===
    def replacer(match):
        key = match.group(1)
        num = mapping.get(key)
        return f'[{num}]' if num else match.group(0)

    numbered = PLACEHOLDER_RE.sub(replacer, text)

    console.print(Panel(
        numbered.strip(),
        title='[bold cyan]Step 3/3: Numbered Text[/]',
        border_style='green',
    ))

    # Output JSON for downstream (Phase 5)
    print('\n--- JSON ---')
    print(json.dumps({f'[CITE:{k}]': f'[{v}]' for k, v in mapping.items()},
                     indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
