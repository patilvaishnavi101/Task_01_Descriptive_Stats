#!/usr/bin/env python3
"""Describe every CSV column using only Python's standard library."""
import argparse
import csv
import json
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path

MISSING = {'', 'n/a', 'na', 'null', 'none', 'nan'}
NUMBER = re.compile(r'^[+-]?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?(?:[eE][+-]?\d+)?$')

def clean(value):
    """Strip surrounding whitespace; preserve case in categorical values."""
    if value is None or value.strip().casefold() in MISSING:
        return None
    return value.strip()

def parse_number(value):
    if value is None:
        return None
    text = value.removeprefix('$').strip()
    if not NUMBER.fullmatch(text):
        return None
    number = float(text.replace(',', ''))
    return number if math.isfinite(number) else None

def compute_numeric_stats(values):
    """Two-pass sample standard deviation (n-1); undefined for n < 2."""
    n = len(values)
    if not n:
        return dict(count=0, mean=None, minimum=None, maximum=None, std_dev=None, median=None)
    mean = math.fsum(values) / n
    ordered = sorted(values)
    middle = n // 2
    median = ordered[middle] if n % 2 else (ordered[middle-1] + ordered[middle]) / 2
    std = math.sqrt(math.fsum((x-mean)**2 for x in values)/(n-1)) if n > 1 else None
    return dict(count=n, mean=mean, minimum=min(values), maximum=max(values), std_dev=std, median=median)

def compute_categorical_stats(values):
    # Alphabetical tie-breaking makes output deterministic.
    frequencies = sorted(Counter(values).items(), key=lambda item: (-item[1], item[0]))
    return dict(count=len(values), unique=len(frequencies),
                mode=frequencies[0][0] if frequencies else None,
                mode_frequency=frequencies[0][1] if frequencies else 0,
                top_5=frequencies[:5])

def infer_type(values):
    if not values:
        return 'empty'
    if all(parse_number(v) is not None for v in values):
        return 'integer' if all(parse_number(v).is_integer() for v in values) else 'float'
    try:
        for v in values:
            date.fromisoformat(v)
        return 'date'
    except ValueError:
        pass
    if all(v.startswith('{') and v.endswith('}') for v in values):
        return 'structured_text (dictionary-like)'
    if all(v.startswith('[') and v.endswith(']') for v in values):
        return 'structured_text (list-like)'
    return 'mixed_numeric_text' if any(parse_number(v) is not None for v in values) else 'text'

def analyze_csv(path):
    columns = {}
    count = 0
    with open(path, newline='', encoding='utf-8-sig') as handle:
        reader = csv.reader(handle)
        headers = next(reader, None)
        if not headers or len(set(headers)) != len(headers) or any(not h for h in headers):
            raise ValueError('CSV requires nonempty, unique column headers.')
        columns = {h: [] for h in headers}
        for row in reader:
            if not row:  # Ignore completely blank CSV records.
                continue
            if len(row) != len(headers):
                raise ValueError(f'CSV record ending at line {reader.line_num}: expected {len(headers)} fields, got {len(row)}.')
            count += 1
            for h, value in zip(headers, row):
                columns[h].append(clean(value))
    result = dict(rows=count, columns=len(headers), std_dev_convention='sample (ddof=1)', column_stats={})
    for h, raw in columns.items():
        present = [v for v in raw if v is not None]
        kind = infer_type(present)
        stats = dict(inferred_type=kind, missing=count-len(present))
        if kind in ('integer', 'float'):
            stats.update(compute_numeric_stats([parse_number(v) for v in present]))
        else:
            stats.update(compute_categorical_stats(present))
            if kind == 'mixed_numeric_text':
                stats['numeric_parseable_count'] = sum(parse_number(v) is not None for v in present)
        result['column_stats'][h] = stats
    return result

def print_report(report):
    print(f"Rows: {report['rows']:,} | Columns: {report['columns']}\nStandard deviation: {report['std_dev_convention']}")
    for name, stats in report['column_stats'].items():
        print('\n' + '='*72 + '\n' + name)
        for metric, value in stats.items():
            print(f'  {metric}: {json.dumps(value, ensure_ascii=False)}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_path', type=Path)
    parser.add_argument('--json-output', type=Path, help='Optional complete machine-readable report')
    args = parser.parse_args()
    try:
        report = analyze_csv(args.csv_path)
        print_report(report)
        if args.json_output:
            args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')

if __name__ == '__main__':
    main()
