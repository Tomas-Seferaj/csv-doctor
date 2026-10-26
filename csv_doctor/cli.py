"""Command-line interface: python -m csv_doctor input.csv [options]"""
import argparse
import sys

import pandas as pd

from .core import clean, diagnose


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="csv-doctor", description="Find and fix problems in messy CSV files."
    )
    parser.add_argument("input", help="path to the CSV file")
    parser.add_argument("-o", "--output", help="save the cleaned CSV here")
    parser.add_argument("-n", "--numbers", nargs="*", default=[], help="columns that should be numbers")
    parser.add_argument("-d", "--dates", nargs="*", default=[], help="columns that should be dates")
    args = parser.parse_args(argv)

    try:
        df = pd.read_csv(args.input, dtype=str, skip_blank_lines=False)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1

    missing = [c for c in args.numbers + args.dates if c not in df.columns]
    if missing:
        print(f"Error: column(s) not found: {', '.join(missing)}", file=sys.stderr)
        return 1

    if args.output:
        cleaned, report = clean(df, args.numbers, args.dates)
        cleaned.to_csv(args.output, index=False)
        print(report.summary())
        print(f"\nCleaned file saved to {args.output}")
    else:
        print(diagnose(df, args.numbers, args.dates).summary())
        print("\nTip: add -o cleaned.csv to save a fixed copy.")
    return 0
