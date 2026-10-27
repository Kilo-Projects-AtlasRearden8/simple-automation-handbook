# STATUS — Simple Automation Handbook

## What was built

A beginner-friendly manual on safe, everyday automation, published by **Asdale
Dynamics, LLC** (credit to Dylan Asdale, registered nurse turned AI author and
founder of Asdale Dynamics, LLC).

**Project contents**

- `README.md` — overview and how to use the handbook; credits Asdale Dynamics,
  LLC.
- `LICENSE` — MIT License, copyright line exactly
  `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `docs/` — beginner manual in Markdown:
  - `overview.md` — welcome and table of contents
  - `safety.md` — safety first (test on copies, never move originals)
  - `sorting-downloads.md` — sort Downloads by file type
  - `renaming-files.md` — bulk rename with prefixes, numbers, etc.
  - `bill-reminders.md` — upcoming/overdue bill reminders from `bills.txt`
  - `saving-webpages.md` — save pages for offline reading
- `scripts/` — tiny, auditable Python scripts (standard library only):
  - `sort_downloads.py`
  - `rename_files.py`
  - `bill_reminders.py`
  - `save_webpage.py`
- `tests/` — test suite for each script:
  - `test_sort_downloads.py`
  - `test_rename_files.py`
  - `test_bill_reminders.py`
  - `test_save_webpage.py`
- `static/` — static HTML site mirroring the docs:
  - `index.html`, `safety.html`, `sorting-downloads.html`,
    `renaming-files.html`, `bill-reminders.html`,
    `saving-webpages.html`, `checklist.html`, `style.css`
- `static/checklist.html` — printable checklist with checkboxes
- `STATUS.md` — this file

## How to run it

### Read the manual
- Markdown: open any file in `docs/`.
- HTML: open `static/index.html` in a browser. The site is fully static (no
  build step, no server needed).

### Run the scripts
Each script is plain Python 3, standard library only — no `pip install`
required.

```
python3 scripts/sort_downloads.py <folder> [--dry-run]
python3 scripts/rename_files.py <folder> [options] [--apply]
python3 scripts/bill_reminders.py <bills.txt> [--within N]
python3 scripts/save_webpage.py <URL> [out_dir]
```

**Safety:** every script defaults to a non-destructive preview (dry-run) or
works on the folder you explicitly point it at. Always test on a copy first.
See `docs/safety.md`.

### Run the tests
```
python3 tests/test_sort_downloads.py
python3 tests/test_rename_files.py
python3 tests/test_bill_reminders.py
python3 tests/test_save_webpage.py
```

### Print the checklist
Open `static/checklist.html` and print from your browser (Letter size). It's
designed to be printed and ticked off by hand.

## Verification results

All checks pass:

- `tests/test_sort_downloads.py` — PASS (extension grouping, copy-only
  behavior, dry-run moves nothing, duplicate avoidance, destination-folder
  skipping)
- `tests/test_rename_files.py` — PASS (dry-run, prefix, numbering,
  spaces-to-dashes + lowercase, suffix, existing-target skip)
- `tests/test_bill_reminders.py` — PASS (upcoming/overdue parsing, malformed
  dates skipped, empty file)
- `tests/test_save_webpage.py` — PASS (URL-to-filename, link collection,
  asset path rewriting)

End-to-end CLI smoke tests also pass, including `save_webpage.py` against
`https://example.com` over the network (page + 1 asset + plain text saved
successfully). No build step, no dependencies beyond Python 3.

## Known gaps

- `save_webpage.py` strips tags crudely for the plain-text version; heavily
  JavaScript-driven or paywalled/login-only pages may not save perfectly.
- The HTML site is hand-written (not generated from Markdown), so `docs/` and
  `static/` must be kept in sync manually.
- No test currently exercises `save_webpage.py` against the network (the test
  suite avoids network calls); network behavior was verified manually only.
- Bill reminders is an organizational tool, not financial advice (noted in the
  docs).
- No `.github/workflows` files (by design — none were requested).
