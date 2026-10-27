#!/usr/bin/env python3
"""Check a bills.txt file and report upcoming and overdue bills.

All data stays in bills.txt on your computer. Nothing is sent anywhere.
Organizational tool only, not financial advice.
"""

import sys
from datetime import date, timedelta

BILL_LINE = "name | due date (YYYY-MM-DD) | amount"


def parse_bills(path):
    """Parse a bills.txt file into a list of (name, due_date, amount, line_no)."""
    bills = []
    with open(path, "r", encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                print(f"Warning: skipping malformed line {line_no}: {raw.rstrip()}",
                      file=sys.stderr)
                continue
            name, due_str, amount = parts[0], parts[1], parts[2]
            try:
                due_date = date.fromisoformat(due_str)
            except ValueError:
                print(f"Warning: bad date on line {line_no}: {due_str}",
                      file=sys.stderr)
                continue
            bills.append((name, due_date, amount, line_no))
    return bills


def check_bills(path, within_days=7):
    """Print upcoming and overdue bills from `path`."""
    today = date.today()
    limit = today + timedelta(days=within_days)

    bills = parse_bills(path)
    if not bills:
        print("No bills found in", path)
        print(f"Add lines like: {BILL_LINE}")
        return 0

    upcoming = []
    overdue = []

    for name, due_date, amount, line_no in bills:
        if due_date < today:
            overdue.append((name, due_date, amount, (today - due_date).days))
        elif due_date <= limit:
            upcoming.append((name, due_date, amount, (due_date - today).days))

    if upcoming:
        print(f"UPCOMING (within {within_days} days):")
        for name, due_date, amount, days in sorted(
            upcoming, key=lambda b: b[1]
        ):
            day_word = "today" if days == 0 else f"in {days} day(s)"
            print(f"  - {name} — due {due_date.isoformat()} — {amount} ({day_word})")
    else:
        print(f"No upcoming bills within {within_days} days.")

    if overdue:
        print("\nOVERDUE:")
        for name, due_date, amount, days in sorted(
            overdue, key=lambda b: b[1]
        ):
            print(f"  - {name} — due {due_date.isoformat()} — {amount} "
                  f"({days} day(s) overdue)")
    else:
        print("No overdue bills.")

    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    within_days = 7
    path = None

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--within" and i + 1 < len(argv):
            within_days = int(argv[i + 1])
            i += 1
        elif not arg.startswith("-"):
            path = arg
        else:
            print(f"Error: unknown option: {arg}", file=sys.stderr)
            return 1
        i += 1

    if path is None:
        print("Usage: python3 bill_reminders.py <bills.txt> [--within N]", file=sys.stderr)
        print(f"\nEach non-comment line in <bills.txt> looks like: {BILL_LINE}")
        print("Example: Electric | 2026-11-05 | $87.30")
        print("\n--within N   report bills due within N days (default 7)")
        return 1

    return check_bills(path, within_days=within_days)


if __name__ == "__main__":
    sys.exit(main())
