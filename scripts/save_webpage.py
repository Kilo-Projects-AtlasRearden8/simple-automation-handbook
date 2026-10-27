#!/usr/bin/env python3
"""Save a webpage to read offline.

Downloads the page, its linked assets (images, stylesheets), and a plain-text
version. Everything stays on your computer. No accounts, no API keys.

Requires: Python standard library only (urllib, html.parser).
"""

import html
import html.parser
import os
import re
import sys
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "SimpleAutomationHandbook/1.0 (local offline reader)"


class LinkCollector(html.parser.HTMLParser):
    """Collect src/href URLs from HTML so we can download linked assets."""

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for attr, value in attrs:
            if attr in ("src", "href") and value:
                absolute = urljoin(self.base_url, value)
                parsed = urlparse(absolute)
                if parsed.scheme in ("http", "https"):
                    self.urls.append(absolute)


def safe_filename(url):
    """Turn a URL into a safe local filename."""
    parsed = urlparse(url)
    path = parsed.path
    if not path or path == "/":
        path = "/index"
    # Replace anything not alphanumeric, dot, dash, or underscore with _
    name = re.sub(r"[^A-Za-z0-9._-]", "_", path.lstrip("/"))
    if not name:
        name = "index"
    return name


def fetch(url):
    """Fetch a URL and return (content_bytes, content_type)."""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        data = resp.read()
        content_type = resp.headers.get("Content-Type", "")
    return data, content_type


def save_webpage(url, out_dir):
    """Download `url` and its assets into `out_dir`."""
    os.makedirs(out_dir, exist_ok=True)

    page_name = safe_filename(url)
    page_html_path = os.path.join(out_dir, page_name + ".html")
    assets_dir = os.path.join(out_dir, page_name + "_files")
    os.makedirs(assets_dir, exist_ok=True)

    # 1. Fetch the HTML.
    html_bytes, content_type = fetch(url)
    html_text = html_bytes.decode("utf-8", errors="replace")

    # 2. Collect asset URLs.
    collector = LinkCollector(url)
    collector.feed(html_text)

    # 3. Download and rewrite asset references.
    asset_map = {}  # original url -> local relative path
    for asset_url in collector.urls:
        local_name = safe_filename(asset_url)
        local_path = os.path.join(assets_dir, local_name)
        rel_path = os.path.join(page_name + "_files", local_name)

        try:
            data, _ = fetch(asset_url)
            with open(local_path, "wb") as fh:
                fh.write(data)
            asset_map[asset_url] = rel_path
        except Exception as exc:  # noqa: BLE001 - skip broken assets gracefully
            print(f"Warning: could not download {asset_url}: {exc}", file=sys.stderr)

    # Rewrite src/href attributes to point to local copies.
    def rewrite(match):
        attr = match.group(1)
        quote = match.group(2)
        value = match.group(3)
        absolute = urljoin(url, value)
        if absolute in asset_map:
            return f'{attr}={quote}{asset_map[absolute]}{quote}'
        return match.group(0)

    html_text = re.sub(
        r'(src|href)=(["\'])([^"\']*)\2', rewrite, html_text
    )

    with open(page_html_path, "w", encoding="utf-8") as fh:
        fh.write(html_text)

    # 4. Plain-text version (strip tags crudely).
    text = re.sub(r"<script.*?</script>", " ", html_text, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text).strip()

    txt_path = os.path.join(out_dir, page_name + ".txt")
    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write(text)

    print(f"Saved page:      {page_html_path}")
    print(f"Saved assets:    {assets_dir}/  ({len(asset_map)} file(s))")
    print(f"Saved plain text: {txt_path}")
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    if len(argv) < 1 or len(argv) > 2:
        print("Usage: python3 save_webpage.py <URL> [out_dir]", file=sys.stderr)
        print("\nDownloads a webpage and its assets so you can read it offline.")
        print("Example: python3 save_webpage.py https://example.com/page ~/Saved-Pages")
        print("\nEverything stays on your computer. Standard library only.")
        return 1

    url = argv[0]
    out_dir = argv[1] if len(argv) == 2 else os.path.join(os.getcwd(), "Saved-Pages")

    if not (url.startswith("http://") or url.startswith("https://")):
        print("Error: URL must start with http:// or https://", file=sys.stderr)
        return 1

    return save_webpage(url, out_dir)


if __name__ == "__main__":
    sys.exit(main())
