#!/usr/bin/env python3
"""Tests for bill_reminders.py.

Run: python3 tests/test_bill_reminders.py
"""

import os
import sys
import tempfile
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import bill_reminders  # noqa: E402


def write_bills(tmp, lines):
    path = os.path.join(tmp, "bills.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return path


def test_upcoming_and_overdue():
    tmp = tempfile.mkdtemp()
    try:
        today = date.today()
        soon = (today + timedelta(days=3)).isoformat()
        late = (today - timedelta(days=2)).isoformat()
        far = (today + timedelta(days=30)).isoformat()

        path = write_bills(tmp, [
            "# comment line",
            "Electric | " + soon + " | $87.30",
            "Rent | " + late + " | $1,200.00",
            "Far away | " + far + " | $10.00",
            "bad date | not-a-date | $1.00",  # should be skipped with warning
        ])

        # Just confirm it runs without crashing and parses valid bills.
        bill_reminders.check_bills(path, within_days=7)

        bills = bill_reminders.parse_bills(path)
        names = [b[0] for b in bills]
        assert "Electric" in names
        assert "Rent" in names
        assert "Far away" in names
        assert "bad date" not in names  # malformed date skipped
    finally:
        import shutil
        shutil.rmtree(tmp)


def test_empty_file():
    tmp = tempfile.mkdtemp()
    try:
        path = write_bills(tmp, ["# only a comment"])
        bill_reminders.check_bills(path)
    finally:
        import shutil
        shutil.rmtree(tmp)


if __name__ == "__main__":
    test_upcoming_and_overdue()
    test_empty_file()
    print("All bill_reminders tests passed.")
