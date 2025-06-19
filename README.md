# Captcha Recognizer

## Introduction

- A Captcha is a fully automated Turing test that distinguishes computers from humans. Although many non-text styles have been developed, text-based Captchas are still the most common.
- Captchas are widely used on websites and applications to stop malicious automation. Users typically have to enter the characters they see in an image when registering, logging in, or submitting forms.
- As technology evolves, Captchas come in forms such as image recognition, audio confirmation and puzzles. These methods aim to improve security but can also hinder user experience. Developers therefore look for more inclusive solutions that keep sites safe without sacrificing convenience.

## Motivation

- This project gave me a deeper understanding of web security challenges. Recognizing digit Captchas involves image processing and machine learning techniques. I wanted to push myself to find breakthroughs and improve accuracy.

## Goals

- Study methods to enhance Captcha recognition. Through research I hope to increase the accuracy and efficiency of digit Captcha recognition and address related challenges.
- Build a reliable recognizer that strengthens the security of websites and applications, protecting users and data from malicious bots.
- Improve the user experience so legitimate visitors can pass verification smoothly while maintaining security.

## Literature Review

- I initially planned to rely solely on Tesseract for recognition but found the accuracy extremely low. After searching online I discovered various preprocessing techniques. I ultimately chose binarization, morphological transformation, `goodFeaturesToTrack` corner detection, `copyMakeBorder` and `medianBlur`. The next section explains the advantages of these methods and the drawbacks when parameters differ.

## Our Approach

### CaptchaBreaker.py

- `menu()` – displays a menu that lets you choose among:
  - Captcha recognition
  - Show success rate for a folder of images (run recognition on each one)
  - Quit the program
  
  ![menu](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/1ed8e644-86ca-4b1e-885a-39cd4f6fca0a)

### Load.py

- `get_image(path)` – reads an image from the given path with `cv2.imread` and returns the image and file name. The label is used when evaluating datasets.

  ![load](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/d8511582-5c29-4ac9-9ba0-110f9b9a4711)

### process_manage.py

- `choose_process()` – lets you set the desired preprocessing order and returns it.
- `process(original_image, order)` – processes the original image step by step as specified by `order`, then applies Tesseract OCR to the final result. Returns the order, intermediate images and recognized text.
- `result` class – displays the results with matplotlib. The selected order determines the plot titles and the images shown. A blank white image of the same size as the original is used as a background for the recognized text.
- `show_rate()` – calculates the character accuracy and per-image accuracy over an entire dataset.

  ![result](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/e6b996d5-cee7-4a47-9507-70c61cc174b7)

### Preprocessing.py

- `bw(original_image)` – performs binarization and noise removal. Pixels at the four corners of the image determine whether to use adaptive thresholding or a fixed threshold.

  ![bw](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/ed6531c8-ad9c-4f45-952a-453eb99335d4)

- `crop_image(original_image)` – uses `goodFeaturesToTrack` to locate four corners, crops the image accordingly and pads it with `copyMakeBorder`.

  ![crop](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/380df829-9371-4ac5-a672-13f35d3a096b)

- `morph_image(original_image)` – applies closing (dilation followed by erosion) to remove small holes and dots.

  ![morph](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/1ee6e7eb-f065-43dd-baa5-0d9d077c4373)

- `blur_image(original_image)` – blurs the image using `medianBlur` with a 3×3 kernel.

  ![blur](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/0cbf13b9-442d-4de0-8122-fc8cb77b4ee1)

- `tesseract(given_image)` – runs Tesseract on the processed image. The environment variable `TESSERACT_CMD` can specify the path to the executable; otherwise `pytesseract` searches for it automatically.

## Experimental Results

- Processing an image with the order `1-2-3-4`:

  ![order1234](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/44e54142-1f67-416c-adfd-3c59d57c153d)

- When Tesseract fails:

  ![failed](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/877af4ba-68ca-42f5-9b94-94a76810ec05)

- When Tesseract succeeds:

  ![success](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/9616f533-fae7-4279-9ed7-7615839cfb53)

- Accuracy after trying all orders:

  ![accuracy](https://github.com/lukeyu1025/CaptchaReader/assets/74660025/080f3b41-bf3b-4372-9e3a-bdd5d5bfc5c4)

Observations:

- Generally, more preprocessing steps lead to higher accuracy, though exceptions exist.
- Orders containing steps 1 or 3 alone can also achieve good accuracy.
- Orders `1-3` and `3-1` produced very high accuracy on this dataset. This may be dataset-specific and not always applicable.
- If time permits, using the preprocessed images for machine learning could further improve accuracy.

## References

- [What is Captcha](https://zh.wikipedia.org/zh-tw/%E9%AA%8C%E8%AF%81%E7%A0%81)
- [Keras: Deep Learning for humans](https://keras.io/)
- [Tesseract OCR Wiki](https://github.com/UB-Mannheim/tesseract/wiki)
- [Binarization tutorial](https://steam.oxxostudio.tw/category/python/ai/opencv-threshold.html)
- [Morphological transformations](https://blog.csdn.net/qq_36560894/article/details/107667211)
- [Corner detection](https://blog.csdn.net/guduruyu/article/details/69537083)
- [copyMakeBorder](https://blog.csdn.net/qq_36560894/article/details/105416273)
- [Median blur](https://blog.csdn.net/A_Z666666/article/details/81324288)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Installation
1. It is recommended to create a Python virtual environment.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract). After installation you can modify `pytesseract.pytesseract.tesseract_cmd` in `Preprocessing.py` if necessary.
4. The `images/` directory contains sample captchas and is optional. You can remove it and use your own dataset instead.

## Usage
Run the main program and follow the prompts or use the command line options:

```bash
python CaptchaBreaker.py --process path/to/image.png
# or
python CaptchaBreaker.py --rate path/to/dataset --order 1234
```
