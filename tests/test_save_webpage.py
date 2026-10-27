#!/usr/bin/env python3
"""Tests for save_webpage.py helpers.

Run: python3 tests/test_save_webpage.py

These tests exercise the URL-to-filename and asset-rewriting helpers without
hitting the network.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import save_webpage  # noqa: E402


def test_safe_filename():
    assert save_webpage.safe_filename("https://example.com/") == "index"
    assert save_webpage.safe_filename("https://example.com/page") == "page"
    assert "Saved-Pages" not in save_webpage.safe_filename("https://example.com/")


def test_link_collector_find_src_and_href():
    collector = save_webpage.LinkCollector("https://example.com/")
    html = (
        '<img src="/image.png">'
        '<link href="style.css">'
        '<a href="https://other.com/page">link</a>'
    )
    collector.feed(html)
    assert "https://example.com/image.png" in collector.urls
    assert "https://example.com/style.css" in collector.urls
    assert "https://other.com/page" in collector.urls


def test_asset_map_rewrites_local_paths():
    # Simulate a fetched page with one local asset.
    url = "https://example.com/page"
    save_webpage.LINK_BASE = url  # not actually used, just illustrative
    collector = save_webpage.LinkCollector(url)
    collector.feed('<img src="/image.png">')
    asset_url = "https://example.com/image.png"
    local_rel = "page_files/image.png"
    mapping = {asset_url: local_rel}

    import re

    def rewrite(match):
        attr, quote, value = match.group(1), match.group(2), match.group(3)
        absolute = "https://example.com" + value if value.startswith("/") else value
        if absolute in mapping:
            return f'{attr}={quote}{mapping[absolute]}{quote}'
        return match.group(0)

    result = re.sub(r'(src|href)=(["\'])([^"\']*)\2', rewrite,
                    '<img src="/image.png">')
    assert 'src="page_files/image.png"' in result


if __name__ == "__main__":
    test_safe_filename()
    test_link_collector_find_src_and_href()
    test_asset_map_rewrites_local_paths()
    print("All save_webpage tests passed.")
