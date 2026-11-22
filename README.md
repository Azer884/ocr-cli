# ocr-cli

A small command-line tool that turns images into text. It runs entirely on your own PC, works offline, and needs no account or API key.

It uses [RapidOCR](https://github.com/RapidAI/RapidOCR) (ONNX Runtime), so there is no separate Tesseract install. It reads English and Chinese, and handles screenshots, photos of documents, and scanned pages.

## Features

- Type `ocr image.png` in cmd and get the text back.
- Read several images in one command.
- Read straight from the clipboard: take a screenshot, then run `ocr`.
- Copy the result to the clipboard or save it to a file.
- Keeps reading order: lines are sorted top to bottom, and words on the same line are joined.
- 100% local. No image leaves your machine.

## Requirements

- Windows 10 or 11
- Python 3.9 or newer, available as `python` on your PATH

## Install

1. Clone the repo:

   ```
   git clone https://github.com/Azer884/ocr-cli.git
   cd ocr-cli
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Add the repo folder to your PATH so `ocr` works from any directory. In PowerShell:

   ```powershell
   $d = (Get-Location).Path
   $p = [Environment]::GetEnvironmentVariable("Path", "User")
   [Environment]::SetEnvironmentVariable("Path", $p.TrimEnd(";") + ";" + $d, "User")
   ```

4. Open a new cmd window and check it works:

   ```
   ocr --help
   ```

The first run loads the OCR models, which takes a few seconds. Later runs are faster.

## Usage

| Command | What it does |
| --- | --- |
| `ocr photo.png` | Print the text found in the image |
| `ocr a.png b.jpg` | Process several images, with a header line per file |
| `ocr` | Read the image currently in the clipboard |
| `ocr photo.png -c` | Print the text and copy it to the clipboard |
| `ocr photo.png -o out.txt` | Print the text and save it to `out.txt` (UTF-8) |

### Quick screenshot workflow

1. Press `Win + Shift + S` and select an area of the screen.
2. In cmd, run `ocr -c`.
3. Paste the text anywhere with `Ctrl + V`.

### Tip

Type `ocr ` in cmd, then drag an image file into the window. Windows pastes the full path for you.

## Example

```
> ocr invoice.png
ACME Corp
Invoice #10442
Total due: 1,250.00 USD
```

## Supported formats

Anything Pillow can open: PNG, JPG, JPEG, BMP, GIF, TIFF, WebP.

## Troubleshooting

- **`'ocr' is not recognized`**: open a new cmd window after changing PATH, or check that the folder is on your PATH.
- **`No image in clipboard`**: copy an image first (for example with `Win + Shift + S`), or pass a file path.
- **Garbled characters in the console**: the tool prints UTF-8. Run `chcp 65001` first, or use `-o out.txt` and open the file.
- **Poor results**: use a larger, sharper image. Very small or low-contrast text is hard to read.

## How it works

`ocr.py` loads each image with Pillow, runs RapidOCR to detect and recognise text, sorts the detected boxes by position, and prints the result. `ocr.cmd` is a one-line wrapper that calls `python ocr.py`, so the command works from any folder.

## License

No license has been chosen yet. Add one before sharing the code publicly.
