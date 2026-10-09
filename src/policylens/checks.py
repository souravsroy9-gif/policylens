"""Policy data quality checks. Blank cells are unknown, never guessed."""
import argparse
import json

import pandas as pd


def load(path):
    return pd.read_excel(path)


def blank_cells(df):
    blanks = {}
    for col in df.columns:
        idx = df[df[col].isna()].index.tolist()
        if idx:
            blanks[col] = idx
    return blanks


def duplicates(df, keys):
    keys = [k for k in keys if k in df.columns]
    if not keys:
        return []
    dup_mask = df.duplicated(subset=keys, keep=False)
    return df[dup_mask].index.tolist()


def expiry_warnings(df, date_cols):
    cols = [c for c in date_cols if c in df.columns]
    return {
        "note": "Expiry dates are historical only. Verify status with the customer.",
        "columns": cols,
    }


def report(path, keys=("Customer Name", "Phone"), date_cols=("Expiry Date",)):
    df = load(path)
    return {
        "rows": len(df),
        "blank_cells": blank_cells(df),
        "duplicate_rows": duplicates(df, list(keys)),
        "expiry_dates": expiry_warnings(df, list(date_cols)),
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Policy data quality report")
    ap.add_argument("xlsx")
    ap.add_argument("--keys", default="Customer Name,Phone")
    ap.add_argument("--date-cols", default="Expiry Date")
    a = ap.parse_args()
    print(json.dumps(report(a.xlsx, tuple(a.keys.split(",")), tuple(a.date_cols.split(","))), indent=2, default=str))
