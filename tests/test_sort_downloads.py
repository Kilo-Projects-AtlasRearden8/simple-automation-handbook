#!/usr/bin/env python3
"""Tests for sort_downloads.py.

Run: python3 tests/test_sort_downloads.py
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import sort_downloads  # noqa: E402


def write_file(folder, name, content=b""):
    path = os.path.join(folder, name)
    with open(path, "wb") as fh:
        fh.write(content)
    return path


def test_groups_files_by_extension():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "resume.pdf", b"%PDF")
        write_file(tmp, "photo.jpg", b"\xff\xd8")
        write_file(tmp, "song.mp3", b"ID3")
        write_file(tmp, "video.mp4", b"\x00\x00\x00")
        write_file(tmp, "archive.zip", b"PK")
        write_file(tmp, "setup.exe", b"MZ")
        write_file(tmp, "mystery.xyz", b"weird")
        write_file(tmp, "noextension", b"data")

        sort_downloads.sort_folder(tmp)

        assert os.path.isfile(os.path.join(tmp, "Documents", "resume.pdf"))
        assert os.path.isfile(os.path.join(tmp, "Images", "photo.jpg"))
        assert os.path.isfile(os.path.join(tmp, "Audio", "song.mp3"))
        assert os.path.isfile(os.path.join(tmp, "Video", "video.mp4"))
        assert os.path.isfile(os.path.join(tmp, "Archives", "archive.zip"))
        assert os.path.isfile(os.path.join(tmp, "Installers", "setup.exe"))
        assert os.path.isfile(os.path.join(tmp, "Other", "mystery.xyz"))
        assert os.path.isfile(os.path.join(tmp, "noextension"))  # untouched
    finally:
        shutil.rmtree(tmp)


def test_does_not_move_originals_unless_pointed_at_them():
    """The script only touches the folder you explicitly pass."""
    tmp = tempfile.mkdtemp()
    try:
        real = os.path.join(tmp, "Real")
        os.makedirs(real)
        write_file(os.path.join(real), "keep.pdf", b"%PDF")

        # Point at a *copy* instead.
        copy = os.path.join(tmp, "Copy")
        shutil.copytree(real, copy)
        sort_downloads.sort_folder(copy)

        # Original untouched.
        assert os.path.isfile(os.path.join(real, "keep.pdf"))
        # Copy sorted.
        assert os.path.isfile(os.path.join(copy, "Documents", "keep.pdf"))
    finally:
        shutil.rmtree(tmp)


def test_dry_run_moves_nothing():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "a.pdf", b"%PDF")
        sort_downloads.sort_folder(tmp, dry_run=True)
        assert os.path.isfile(os.path.join(tmp, "a.pdf"))  # still in place
        assert not os.path.isdir(os.path.join(tmp, "Documents"))
    finally:
        shutil.rmtree(tmp)


def test_avoids_overwriting_duplicates():
    tmp = tempfile.mkdtemp()
    try:
        # Pre-place a file with the same name in the destination folder.
        os.makedirs(os.path.join(tmp, "Documents"))
        write_file(os.path.join(tmp, "Documents"), "a.pdf", b"existing")
        write_file(tmp, "a.pdf", b"new")
        sort_downloads.sort_folder(tmp)
        assert os.path.isfile(os.path.join(tmp, "Documents", "a.pdf"))
        assert os.path.isfile(os.path.join(tmp, "Documents", "a-1.pdf"))
    finally:
        shutil.rmtree(tmp)


def test_skips_existing_destination_folders():
    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, "Documents"))
        write_file(tmp, "a.pdf", b"%PDF")
        sort_downloads.sort_folder(tmp)
        # Should still sort a.pdf into Documents (it already exists, fine).
        assert os.path.isfile(os.path.join(tmp, "Documents", "a.pdf"))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    test_groups_files_by_extension()
    test_does_not_move_originals_unless_pointed_at_them()
    test_dry_run_moves_nothing()
    test_avoids_overwriting_duplicates()
    test_skips_existing_destination_folders()
    print("All sort_downloads tests passed.")
