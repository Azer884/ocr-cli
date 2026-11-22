"""Local offline image-to-text (OCR) CLI.

Usage:
  ocr image.png [more.jpg ...]   print text found in image(s)
  ocr                            read image from clipboard
  ocr image.png -c               also copy text to clipboard
  ocr image.png -o out.txt       save text to file
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageGrab
from rapidocr_onnxruntime import RapidOCR


def to_text(engine, img):
    result, _ = engine(img)
    if not result:
        return ""
    # result item: [box, text, score]; sort top-to-bottom, left-to-right
    items = sorted(result, key=lambda r: (round(r[0][0][1] / 10), r[0][0][0]))
    lines, last_row = [], None
    for box, text, _score in items:
        row = round(box[0][1] / 10)
        if last_row is not None and row == last_row:
            lines[-1] += " " + text
        else:
            lines.append(text)
        last_row = row
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="ocr", description="Offline image to text.")
    p.add_argument("images", nargs="*", help="image file(s); none = clipboard")
    p.add_argument("-c", "--copy", action="store_true", help="copy text to clipboard")
    p.add_argument("-o", "--out", help="save text to file")
    a = p.parse_args()

    sources = []
    if a.images:
        for path in a.images:
            try:
                sources.append((path, np.array(Image.open(path).convert("RGB"))))
            except Exception as e:
                print(f"Cannot open {path}: {e}", file=sys.stderr)
    else:
        clip = ImageGrab.grabclipboard()
        if isinstance(clip, Image.Image):
            sources.append(("clipboard", np.array(clip.convert("RGB"))))
        elif isinstance(clip, list) and clip:
            try:
                sources.append((clip[0], np.array(Image.open(clip[0]).convert("RGB"))))
            except Exception as e:
                print(f"Cannot open {clip[0]}: {e}", file=sys.stderr)
        else:
            print("No image in clipboard. Pass a file: ocr image.png", file=sys.stderr)
            return 1
    if not sources:
        return 1

    engine = RapidOCR()
    parts = []
    for name, img in sources:
        text = to_text(engine, img)
        parts.append(f"=== {name} ===\n{text}" if len(sources) > 1 else text)
    out = "\n\n".join(parts)
    print(out)

    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out + "\n")
    if a.copy:
        import pyperclip
        pyperclip.copy(out)
        print("(copied to clipboard)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
