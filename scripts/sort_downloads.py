#!/usr/bin/env python3
"""Sort files in a folder into type-based subfolders.

Safety: works on the folder you point it at. Always test on a copy first.
Never deletes files; only moves them into type folders.
"""

import os
import shutil
import sys

# Map file extensions (lowercase, with dot) to destination folder names.
EXTENSION_GROUPS = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".odt": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",
    ".bmp": "Images",
    ".svg": "Images",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".m4a": "Audio",
    ".ogg": "Audio",
    ".flac": "Audio",
    ".mp4": "Video",
    ".mov": "Video",
    ".avi": "Video",
    ".mkv": "Video",
    ".wmv": "Video",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".exe": "Installers",
    ".dmg": "Installers",
    ".pkg": "Installers",
    ".msi": "Installers",
}

DEFAULT_OTHER = "Other"


def group_for_extension(ext):
    """Return the destination folder name for a file extension."""
    return EXTENSION_GROUPS.get(ext, DEFAULT_OTHER)


def sort_folder(folder, dry_run=False):
    """Sort files directly inside `folder` into type subfolders.

    Does not recurse into subfolders. Skips folders that already exist in the
    top level so we don't try to sort our own output folders.
    """
    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        print(f"Error: not a directory: {folder}", file=sys.stderr)
        return 1

    # Names of top-level subfolders we create, so we don't sort into them.
    destination_names = set(EXTENSION_GROUPS.values()) | {DEFAULT_OTHER}

    moved = 0
    skipped = 0
    for entry in os.listdir(folder):
        entry_path = os.path.join(folder, entry)

        # Skip directories (including our destination folders).
        if os.path.isdir(entry_path):
            skipped += 1
            continue

        # Skip files with no extension.
        _, ext = os.path.splitext(entry)
        if not ext:
            skipped += 1
            continue

        dest_folder = group_for_extension(ext.lower())
        dest_path = os.path.join(folder, dest_folder, entry)

        # Avoid overwriting an existing file with the same name.
        if os.path.exists(dest_path):
            base, extension = os.path.splitext(entry)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(
                    folder, dest_folder, f"{base}-{counter}{extension}"
                )
                counter += 1

        if dry_run:
            print(f"[dry-run] would move: {entry} -> {dest_folder}/")
        else:
            os.makedirs(os.path.join(folder, dest_folder), exist_ok=True)
            shutil.move(entry_path, dest_path)
            print(f"moved: {entry} -> {dest_folder}/")
        moved += 1

    print(f"\nDone. {moved} file(s) {'would be ' if dry_run else ''}moved, "
          f"{skipped} item(s) skipped (folders or extensionless files).")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    dry_run = False
    if "--dry-run" in argv or "-n" in argv:
        dry_run = True
        argv.remove("--dry-run") if "--dry-run" in argv else None
        argv.remove("-n") if "-n" in argv else None

    if not argv:
        print("Usage: python3 sort_downloads.py <folder> [--dry-run]", file=sys.stderr)
        print("\nMoves files in <folder> into type-based subfolders "
              "(Documents, Images, Audio, Video, Archives, Installers, Other).")
        print("Use --dry-run to preview without moving anything.")
        print("\nSafety: test on a copy of your folder first.")
        return 1

    return sort_folder(argv[0], dry_run=dry_run)


if __name__ == "__main__":
    sys.exit(main())
