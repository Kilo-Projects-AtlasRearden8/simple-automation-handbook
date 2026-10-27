# Sorting Your Downloads

Your Downloads folder is probably a mess: PDFs, images, installers, and who
knows what else all in one pile. This guide shows you how to sort them into
neat folders by file type — safely, one step at a time.

## What this does

Looks at every file in a folder and moves it into a subfolder named after its
type:

- `Documents/` — .pdf, .doc, .docx, .txt, .rtf
- `Images/` — .jpg, .jpeg, .png, .gif, .webp, .bmp
- `Audio/` — .mp3, .wav, .m4a, .ogg
- `Video/` — .mp4, .mov, .avi, .mkv
- `Archives/` — .zip, .rar, .7z, .tar, .gz
- `Installers/` — .exe, .dmg, .pkg, .msi
- `Other/` — anything that doesn't match the above

Files without extensions (and folders already in Downloads) are left alone.

## Step 1: Make a test copy

Copy your Downloads folder to a test location first:

- **Windows:** copy `Downloads` to `Downloads Test`
- **Mac:** right-click `Downloads` → Duplicate
- **Linux:** `cp -r ~/Downloads ~/Downloads-Test`

## Step 2: Run the sorter

```bash
python3 scripts/sort_downloads.py ~/Downloads-Test
```

Look at the result. Are files in the right folders? Did anything unexpected
happen?

## Step 3: Run on your real Downloads (optional)

Once you're happy, point it at your real Downloads folder:

```bash
python3 scripts/sort_downloads.py ~/Downloads
```

Or keep using the test folder forever. There's no rush.

## The script

See `scripts/sort_downloads.py`. It's about 40 lines and you can read it end to
end before running it.

## Customizing

Want a folder for spreadsheets? Add `.xlsx` and `.csv` to the `Documents`
group in the script. Want to keep installers out? Remove the `Installers`
group and they'll fall into `Other`. It's your script — edit it.
