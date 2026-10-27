# Saving Webpages

Found an article or recipe you want to keep? This guide shows you how to save
a webpage to your computer so you can read it later, offline, without relying
on a bookmark that might break.

## What this does

Downloads a webpage you specify and saves it as an HTML file plus a folder of
images and stylesheets, so the page looks right even offline. It also saves a
plain-text version so you can read just the words.

## Step 1: Get the webpage address

Copy the URL of the page you want to save, e.g.

```
https://example.com/some-recipe
```

## Step 2: Run the saver

```bash
python3 scripts/save_webpage.py https://example.com/some-recipe ~/Saved-Pages
```

This creates `~/Saved-Pages/` with:

- `some-recipe.html` — the full page
- `some-recipe_files/` — images, stylesheets, scripts
- `some-recipe.txt` — plain text, words only

Open `some-recipe.html` in your browser to read it offline.

## Step 3: Organize your saved pages

Create folders inside `Saved-Pages` by topic:

```
Saved-Pages/
  Recipes/
  Research/
  Fun/
```

Move saved pages into the right folder so they're easy to find later.

## Requirements

The webpage saver needs Python's standard library plus `urllib` (built in) and
`html.parser` (built in). No `pip install` required.

## Notes

- Only save pages you have the right to keep for personal use. Don't republish
  saved pages without permission.
- Some pages (paywalled, login-only, heavily JavaScript-driven) may not save
  perfectly. If a page looks off after saving, that's normal — try saving the
  plain-text `.txt` version instead.
- Nothing is sent to Asdale Dynamics or anyone else. The page goes directly
  from the website to your computer.
