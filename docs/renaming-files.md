# Renaming Files

Got a folder of files named `IMG_0492.jpg`, `document-final-v2.pdf`,
`screenshot (1).png`? This guide shows you how to rename them in bulk so they're
easy to find later.

## What this does

Renames files in a folder according to a simple pattern you choose:

- Add a prefix (e.g. `vacation-2026-IMG_0492.jpg`)
- Add a suffix (e.g. `IMG_0492-vacation-2026.jpg`)
- Add a running number (e.g. `photo-001.jpg`, `photo-002.jpg`)
- Replace spaces with dashes or underscores
- Lowercase everything

The script shows you what it *would* do before it renames anything (dry-run
mode). You only rename for real when you say so.

## Step 1: Make a test copy

Copy the folder you want to rename:

```bash
cp -r ~/Photos ~/Photos-Test
```

## Step 2: Preview the changes (dry run)

```bash
python3 scripts/rename_files.py ~/Photos-Test --prefix vacation-2026 --dry-run
```

This prints the old name → new name mapping without changing anything. Review
it carefully.

## Step 3: Rename for real

When the preview looks right, drop the `--dry-run` flag:

```bash
python3 scripts/rename_files.py ~/Photos-Test --prefix vacation-2026
```

## Step 4: Check the results

Open the folder and confirm the names look the way you want. If something's
wrong, delete the test folder and try again with different options.

## The script

See `scripts/rename_files.py`. Read it before running it — it's short and every
line is explained.

## Safety reminder

This script renames files in place (on the folder you point it at). That's why
we always test on a copy first. Your originals stay untouched until you're
sure.
