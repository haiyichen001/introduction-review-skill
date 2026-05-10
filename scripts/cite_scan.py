#!/usr/bin/env python3
"""
Citation placeholder scanner and numbering pass engine.

Reads text with [CITE:key] placeholders, assigns sequential numbers
by first-appearance order, replaces all placeholders, outputs the
numbered text + mapping table.

Usage:
    python cite_scan.py < input.txt
    python cite_scan.py input.txt
    python cite_scan.py input.txt --output output.txt
    python cite_scan.py input.txt --json   # JSON output with mapping
"""

import re
import sys
import json
import argparse
from collections import OrderedDict

PLACEHOLDER_RE = re.compile(r'\[CITE:([a-zA-Z0-9_\-]+)\]')


def scan(text):
    """Find all unique placeholders in order of first appearance."""
    seen = OrderedDict()
    for match in PLACEHOLDER_RE.finditer(text):
        key = match.group(1)
        if key not in seen:
            seen[key] = len(seen) + 1
    return seen


def replace(text, mapping):
    """Replace all [CITE:key] with [N] using the mapping."""
    def replacer(match):
        key = match.group(1)
        num = mapping.get(key)
        if num is None:
            return f"[CITE:{key}]"  # unknown placeholder, leave as-is
        return f"[{num}]"

    return PLACEHOLDER_RE.sub(replacer, text)


def extract_keys(text):
    """Extract all placeholder keys with positions."""
    results = []
    for match in PLACEHOLDER_RE.finditer(text):
        results.append({
            'key': match.group(1),
            'position': match.start(),
            'span': (match.start(), match.end()),
        })
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Citation placeholder numbering pass'
    )
    parser.add_argument('input', nargs='?', help='Input file (or stdin)')
    parser.add_argument('--output', '-o', help='Output file for numbered text')
    parser.add_argument('--json', action='store_true', help='Output JSON with mapping')
    parser.add_argument('--mapping-only', action='store_true',
                        help='Only output the mapping table')
    args = parser.parse_args()

    # Read input
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    # Scan for placeholders
    mapping = scan(text)
    occurrences = extract_keys(text)

    if args.mapping_only:
        result = {f'[CITE:{k}]': f'[{v}]' for k, v in mapping.items()}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.json:
        output = {
            'unique_placeholders': len(mapping),
            'total_occurrences': len(occurrences),
            'mapping': {f'[CITE:{k}]': f'[{v}]' for k, v in mapping.items()},
            'in_order': [f'[CITE:{k}]' for k in mapping.keys()],
            'occurrences': [
                {'key': f'[CITE:{o["key"]}]', 'number': mapping[o['key']],
                 'reuse': i > 0 and occurrences[i-1]['key'] != o['key'] and
                 any(e['key'] == o['key'] for e in occurrences[:i])}
                for i, o in enumerate(occurrences)
            ],
        }
        output['numbered_text'] = replace(text, mapping)
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # Stream output
    print(f'--- Cite Scan ---')
    print(f'Scanning for [CITE:xxx] placeholders...')

    # Show each unique placeholder found
    def ordinal(n):
        if 11 <= (n % 100) <= 13:
            return f'{n}th'
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        return f'{n}{suffixes.get(n % 10, "th")}'

    ordered_keys = list(mapping.keys())
    for i, key in enumerate(ordered_keys):
        print(f'  {ordinal(i+1)}: [CITE:{key}]')
    print(f'Found {len(mapping)} unique placeholders, '
          f'{len(occurrences)} total occurrences.')
    print()

    # Show mapping
    print('Mapping table:')
    for key, num in mapping.items():
        print(f'  [CITE:{key}] -> [{num}]')
    print()

    # Show replacement
    print('Replacing...')
    numbered = replace(text, mapping)
    for i, occ in enumerate(occurrences):
        key = occ['key']
        num = mapping[key]
        reuse = ''
        if i > 0:
            prev_matches = [o for o in occurrences[:i] if o['key'] == key]
            if prev_matches:
                reuse = ' (reuse)'
        print(f'  [{i+1}/{len(occurrences)}] [CITE:{key}] -> [{num}]{reuse} [OK]')
    print(f'All {len(occurrences)} occurrences replaced.')
    print()

    # Output numbered text
    print('--- Numbered Text ---')
    print(numbered)
    print('--- End ---')

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(numbered)
        print(f'Saved to {args.output}')


if __name__ == '__main__':
    main()
