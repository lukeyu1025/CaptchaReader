# Captcha Reader

This project provides a simple command line tool to recognize text-based Captchas. It uses OpenCV for image processing and the Tesseract OCR engine for character recognition.

## Purpose

The goal is to explore ways to improve the accuracy and efficiency of digit Captcha recognition. By creating a reliable recognizer we hope to strengthen website security and reduce the inconvenience to legitimate users.

## Installation

1. Install Python 3.
2. Install the following dependencies:
   ```bash
   pip install opencv-python numpy matplotlib pytesseract
   ```
3. Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and ensure the executable path matches the one specified in `Preprocessing.py`.

## Usage

Run `CaptchaBreaker.py` and follow the menu prompts:

```bash
python CaptchaBreaker.py
```

* **Preprocess image** – load a single image for preprocessing and recognition.
* **Show success rate for dataset** – evaluate a folder of captcha images.
* **Quit** – exit the program.

