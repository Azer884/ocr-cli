# ocr

Offline image-to-text CLI for Windows. Uses RapidOCR (English + Chinese), no external binary.

## Install
    pip install rapidocr-onnxruntime pillow pyperclip

Add this folder to your PATH, then:

    ocr image.png            print text
    ocr a.png b.jpg          several images
    ocr                      read image from clipboard
    ocr image.png -c         copy result to clipboard
    ocr image.png -o out.txt save to file
