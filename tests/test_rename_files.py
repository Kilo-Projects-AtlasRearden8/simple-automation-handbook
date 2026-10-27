#!/usr/bin/env python3
"""Tests for rename_files.py.

Run: python3 tests/test_rename_files.py
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import rename_files  # noqa: E402


def write_file(folder, name, content=b""):
    path = os.path.join(folder, name)
    with open(path, "wb") as fh:
        fh.write(content)
    return path


def test_dry_run_renames_nothing():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "IMG_0492.jpg", b"")
        rename_files.rename_files(tmp, prefix="vacation-", apply=False)
        assert os.path.isfile(os.path.join(tmp, "IMG_0492.jpg"))
        assert not os.path.isfile(os.path.join(tmp, "vacation-IMG_0492.jpg"))
    finally:
        shutil.rmtree(tmp)


def test_applies_prefix():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "IMG_0492.jpg", b"")
        rename_files.rename_files(tmp, prefix="vacation-", apply=True)
        assert os.path.isfile(os.path.join(tmp, "vacation-IMG_0492.jpg"))
        assert not os.path.isfile(os.path.join(tmp, "IMG_0492.jpg"))
    finally:
        shutil.rmtree(tmp)


def test_numbering():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "a.jpg", b"")
        write_file(tmp, "b.jpg", b"")
        write_file(tmp, "c.txt", b"")
        rename_files.rename_files(tmp, number=True, apply=True)
        names = sorted(os.listdir(tmp))
        assert names == ["a-001.jpg", "b-002.jpg", "c-003.txt"]
    finally:
        shutil.rmtree(tmp)


def test_spaces_to_dashes_and_lowercase():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "My Photo.jpg", b"")
        rename_files.rename_files(
            tmp, replace_spaces=True, lowercase=True, apply=True
        )
        assert os.path.isfile(os.path.join(tmp, "my-photo.jpg"))
    finally:
        shutil.rmtree(tmp)


def test_suffix():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "report.pdf", b"")
        rename_files.rename_files(tmp, suffix="-final", apply=True)
        assert os.path.isfile(os.path.join(tmp, "report-final.pdf"))
    finally:
        shutil.rmtree(tmp)


def test_skips_existing_target():
    tmp = tempfile.mkdtemp()
    try:
        write_file(tmp, "a.txt", b"")
        # Pre-create the target that prefixing a.txt would produce.
        write_file(tmp, "b-a.txt", b"existing")
        rename_files.rename_files(tmp, prefix="b-", apply=True)
        # a.txt was skipped because b-a.txt already existed.
        assert os.path.isfile(os.path.join(tmp, "a.txt"))
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    test_dry_run_renames_nothing()
    test_applies_prefix()
    test_numbering()
    test_spaces_to_dashes_and_lowercase()
    test_suffix()
    test_skips_existing_target()
    print("All rename_files tests passed.")
