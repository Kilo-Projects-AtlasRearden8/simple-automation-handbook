#!/usr/bin/env python3
"""Rename files in a folder using a chosen pattern.

Safety: defaults to dry-run mode (shows what it *would* do). Only renames for
real when you pass --apply. Always test on a copy first.
"""

import os
import re
import sys


def slugify(name):
    """Lowercase and replace spaces/runs of whitespace with dashes."""
    name = name.strip().lower()
    name = re.sub(r"\s+", "-", name)
    return name


def build_new_name(filename, prefix="", suffix="", number=None,
                   number_digits=3, replace_spaces=False, lowercase=False,
                   keep_extension=True):
    """Compute the new name for a single file."""
    if keep_extension:
        base, ext = os.path.splitext(filename)
    else:
        base, ext = filename, ""

    new_base = base

    if replace_spaces:
        new_base = re.sub(r"\s+", "-", new_base)

    if lowercase:
        new_base = new_base.lower()

    if prefix:
        new_base = prefix + new_base

    if suffix:
        new_base = new_base + suffix

    if number is not None:
        new_base = f"{new_base}-{number:0{number_digits}d}"

    return new_base + ext


def rename_files(folder, prefix="", suffix="", number=False,
                 number_start=1, number_digits=3, replace_spaces=False,
                 lowercase=False, apply=False):
    """Rename files directly inside `folder`.

    Returns (renamed, skipped) counts. Prints every planned change.
    """
    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        print(f"Error: not a directory: {folder}", file=sys.stderr)
        return 1

    entries = sorted(
        e for e in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, e))
    )

    counter = number_start
    renamed = 0
    skipped = 0

    for entry in entries:
        num = counter if number else None
        new_name = build_new_name(
            entry, prefix=prefix, suffix=suffix, number=num,
            number_digits=number_digits, replace_spaces=replace_spaces,
            lowercase=lowercase,
        )

        if new_name == entry:
            skipped += 1
            print(f"unchanged: {entry}")
            counter += 1 if number else 0
            continue

        src = os.path.join(folder, entry)
        dst = os.path.join(folder, new_name)

        if os.path.exists(dst):
            skipped += 1
            print(f"skip (target exists): {entry} -> {new_name}")
            counter += 1 if number else 0
            continue

        if apply:
            os.rename(src, dst)
            print(f"renamed: {entry} -> {new_name}")
        else:
            print(f"[dry-run] would rename: {entry} -> {new_name}")
        renamed += 1
        counter += 1 if number else 0

    mode = "applied" if apply else "previewed (dry-run)"
    print(f"\nDone. {renamed} file(s) {mode}, {skipped} unchanged or skipped.")
    if not apply:
        print("Pass --apply to rename for real.")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    folder = None
    prefix = ""
    suffix = ""
    number = False
    number_start = 1
    number_digits = 3
    replace_spaces = False
    lowercase = False
    apply_flag = False

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--apply", "-a"):
            apply_flag = True
        elif arg in ("--dry-run", "-n"):
            pass  # default behavior
        elif arg == "--prefix" and i + 1 < len(argv):
            prefix = argv[i + 1]
            i += 1
        elif arg == "--suffix" and i + 1 < len(argv):
            suffix = argv[i + 1]
            i += 1
        elif arg == "--number":
            number = True
        elif arg == "--start" and i + 1 < len(argv):
            number_start = int(argv[i + 1])
            i += 1
        elif arg == "--digits" and i + 1 < len(argv):
            number_digits = int(argv[i + 1])
            i += 1
        elif arg == "--spaces-to-dashes":
            replace_spaces = True
        elif arg == "--lowercase":
            lowercase = True
        elif not arg.startswith("-"):
            folder = arg
        else:
            print(f"Error: unknown option: {arg}", file=sys.stderr)
            return 1
        i += 1

    if folder is None:
        print("Usage: python3 rename_files.py <folder> [options]", file=sys.stderr)
        print("\nOptions:")
        print("  --prefix TEXT        Add text to the front of each name")
        print("  --suffix TEXT        Add text to the end of each name (before extension)")
        print("  --number             Add a running number (photo-001.jpg, ...)")
        print("  --start N            Starting number (default 1)")
        print("  --digits N           Number of digits for padding (default 3)")
        print("  --spaces-to-dashes   Replace spaces with dashes")
        print("  --lowercase          Lowercase the whole name")
        print("  --apply              Rename for real (default is dry-run preview)")
        print("\nSafety: defaults to dry-run. Test on a copy first.")
        return 1

    return rename_files(
        folder, prefix=prefix, suffix=suffix, number=number,
        number_start=number_start, number_digits=number_digits,
        replace_spaces=replace_spaces, lowercase=lowercase, apply=apply_flag,
    )


if __name__ == "__main__":
    sys.exit(main())
