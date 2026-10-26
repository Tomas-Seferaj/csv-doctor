"""Core logic for diagnosing and cleaning CSV data."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class Report:
    """Summary of the problems found (and fixed) in a dataset."""

    rows_before: int = 0
    rows_after: int = 0
    empty_rows: int = 0
    duplicate_rows: int = 0
    whitespace_cells: int = 0
    bad_numbers: dict[str, int] = field(default_factory=dict)
    bad_dates: dict[str, int] = field(default_factory=dict)

    @property
    def total_issues(self) -> int:
        return (
            self.empty_rows
            + self.duplicate_rows
            + self.whitespace_cells
            + sum(self.bad_numbers.values())
            + sum(self.bad_dates.values())
        )

    def summary(self) -> str:
        lines = [
            f"Rows: {self.rows_before} -> {self.rows_after}",
            f"Empty rows removed:      {self.empty_rows}",
            f"Duplicate rows removed:  {self.duplicate_rows}",
            f"Cells with extra spaces: {self.whitespace_cells}",
        ]
        for col, n in self.bad_numbers.items():
            lines.append(f"Invalid numbers in '{col}': {n}")
        for col, n in self.bad_dates.items():
            lines.append(f"Invalid dates in '{col}':   {n}")
        lines.append(f"Total issues: {self.total_issues}")
        return "\n".join(lines)


def _strip_whitespace(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Trim spaces in text cells and count how many cells changed."""
    changed = 0
    df = df.copy()
    for col in df.select_dtypes(include=["object", "string"]).columns:
        original = df[col]
        stripped = original.str.strip()
        changed += int(((original != stripped) & original.notna()).sum())
        df[col] = stripped.replace("", pd.NA)
    return df, changed


def _to_numeric(series: pd.Series) -> tuple[pd.Series, int]:
    """Convert values like '1,200' or '$30' to numbers; count failures."""
    cleaned = series.astype("string").str.replace(r"[,\s$€]", "", regex=True)
    numbers = pd.to_numeric(cleaned, errors="coerce")
    bad = int((numbers.isna() & series.notna()).sum())
    return numbers, bad


def _to_dates(series: pd.Series) -> tuple[pd.Series, int]:
    """Parse dates in mixed formats; count values that couldn't be parsed."""
    dates = pd.to_datetime(series, errors="coerce", format="mixed")
    bad = int((dates.isna() & series.notna()).sum())
    return dates, bad


def _process(df, number_cols, date_cols):
    report = Report(rows_before=len(df))

    df, report.whitespace_cells = _strip_whitespace(df)

    empty_mask = df.isna().all(axis=1)
    report.empty_rows = int(empty_mask.sum())
    df = df[~empty_mask].copy()

    for col in number_cols:
        df[col], bad = _to_numeric(df[col])
        if bad:
            report.bad_numbers[col] = bad

    for col in date_cols:
        df[col], bad = _to_dates(df[col])
        if bad:
            report.bad_dates[col] = bad

    dup_mask = df.duplicated()
    report.duplicate_rows = int(dup_mask.sum())
    df = df[~dup_mask].reset_index(drop=True)

    report.rows_after = len(df)
    return df, report


def diagnose(df: pd.DataFrame, number_cols=(), date_cols=()) -> Report:
    """Return a report of problems without changing the original data."""
    _, report = _process(df.copy(), number_cols, date_cols)
    return report


def clean(df: pd.DataFrame, number_cols=(), date_cols=()) -> tuple[pd.DataFrame, Report]:
    """Return a cleaned copy of the data plus a report of what was fixed."""
    return _process(df.copy(), number_cols, date_cols)
