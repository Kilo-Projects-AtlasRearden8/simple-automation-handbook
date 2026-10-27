# Bill Reminders

Never miss a due date again. This guide shows you how to keep a simple list of
bills and get a reminder when one is coming up — all in a plain text file on
your own computer, no apps or accounts needed.

## What this does

Reads a `bills.txt` file you maintain and tells you which bills are due soon
(within 7 days by default) and which are already overdue.

A sample `bills.txt` looks like this:

```
# Bill name | due date (YYYY-MM-DD) | amount
Electric | 2026-11-05 | $87.30
Water | 2026-11-12 | $42.10
Internet | 2026-11-15 | $59.99
Rent | 2026-11-01 | $1,200.00
```

Lines starting with `#` are comments and ignored.

## Step 1: Create your bills file

Create `bills.txt` somewhere easy to find, like your Documents folder:

```
# My bills
Electric | 2026-11-05 | $87.30
Water | 2026-11-12 | $42.10
```

Use real dates and amounts. The date format is year-month-day (2026-11-05).

## Step 2: Run the reminder

```bash
python3 scripts/bill_reminders.py ~/Documents/bills.txt
```

You'll see something like:

```
UPCOMING (within 7 days):
- Electric — due 2026-11-05 — $87.30 (in 3 days)

OVERDUE:
- Rent — due 2026-11-01 — $1,200.00 (2 days overdue)
```

## Step 3: Make it a habit

Run the script once a week, maybe Sunday morning with coffee. Add new bills to
`bills.txt` as they arrive. Remove paid ones.

You can also set a calendar reminder on your phone to run the script weekly —
the script itself stays local and private.

## The script

See `scripts/bill_reminders.py`. It's about 40 lines and uses only Python's
built-in `datetime` module.

## Notes

- This is an organizational tool, not financial advice. If you're having
  trouble paying bills, consider speaking with a financial counselor.
- All data stays in `bills.txt` on your computer. Nothing is sent anywhere.
