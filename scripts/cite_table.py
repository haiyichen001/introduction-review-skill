#!/usr/bin/env python3
"""
Citation reference table generator.
Reads text with [CITE:xxx] placeholders, assigns numbers, extracts
the surrounding sentence for each citation, and prints a reference table.

Usage:
    python cite_table.py <input_file>
"""

import re
import sys
import json
import os
from collections import OrderedDict

PLACEHOLDER_RE = re.compile(r'\[CITE:([a-zA-Z0-9_\-]+)\]')


def scan_order(text):
    seen = OrderedDict()
    for match in PLACEHOLDER_RE.finditer(text):
        key = match.group(1)
        if key not in seen:
            seen[key] = len(seen) + 1
    return seen


def extract_context(text, start, end, max_len=50):
    """Extract the sentence containing the citation, truncated to max_len chars."""
    # Find sentence boundaries around the match
    before = text[:start]
    after = text[end:]

    # Go back to last sentence end or beginning
    sent_start = 0
    for sep in ['. ', '.\n', '! ', '?\n', '!\n', '?\n']:
        idx = before.rfind(sep)
        if idx > sent_start:
            sent_start = idx + len(sep)

    # Go forward to next sentence end
    sent_end = len(text)
    for sep in ['. ', '.\n', '! ', '? ', '!\n', '?\n', '.\n\n', '.\n']:
        idx = after.find(sep)
        if idx != -1 and idx + end < sent_end:
            sent_end = idx + end + 1
            break

    sentence = text[sent_start:sent_end].strip()
    # Replace placeholder with its number later, keep original for now
    sentence = sentence.replace('\n', ' ').strip()

    if len(sentence) > max_len:
        sentence = sentence[:max_len-3] + '...'

    return sentence


def format_author(key):
    """Format author name from cite key: 'smith2023' -> 'Smith'"""
    # Split on digits
    name = re.split(r'\d', key)[0]
    # Capitalize first letter
    if name and name[0].islower():
        name = name[0].upper() + name[1:]
    return name


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    placeholders = scan_order(text)
    mapping = {}
    ordered_keys = list(placeholders.keys())

    for key in ordered_keys:
        mapping[key] = placeholders[key]

    # Build occurrence list
    occurrences = []
    for match in PLACEHOLDER_RE.finditer(text):
        key = match.group(1)
        num = mapping[key]
        context = extract_context(text, match.start(), match.end())

        # Replace placeholder with number in context
        context = context.replace(f'[CITE:{key}]', f'[{num}]')

        status = '正确'
        first_occ_for_key = not any(
            o['key'] == key for o in occurrences
        )

        # Check if this is the first occurrence of this key
        prev_same_key = [o for o in occurrences if o['key'] == key]
        if prev_same_key:
            status = f'重复引用(首次为[{num}])'
        elif not first_occ_for_key:
            status = '正确'

        occurrences.append({
            'num': num,
            'key': key,
            'context': context,
            'status': status,
        })

    # Print the reference table
    print()
    print(f'{"序号":<6} {"作者":<20} {"正文引用(首次出现)":<52} {"状态":<20}')
    print('-' * 100)

    seen_keys = set()
    for occ in occurrences:
        key = occ['key']
        if key in seen_keys:
            continue  # only show first occurrence per paper
        seen_keys.add(key)

        author = format_author(key)
        num = occ['num']
        ctx = occ['context']
        status = occ['status']

        print(f'[{num}]{" ":<4} {author:<20} {ctx:<52} {status:<20}')

    print('-' * 100)
    print(f'{len(seen_keys)} references total.')


if __name__ == '__main__':
    main()
