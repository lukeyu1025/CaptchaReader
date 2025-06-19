import numpy as np
import pytesseract
import cv2
import os


"""Image preprocessing utilities."""


def bw(original_image):
    """Binarize the image and remove noise.

    Parameters
    ----------
    original_image : numpy.ndarray
        Grayscale image to process.

    Returns
    -------
    numpy.ndarray
        Thresholded binary image where pixels are either 0 or 255.
    """
    t1 = original_image[0][0]
    t2 = original_image[0][original_image.shape[1]-1]
    t3 = original_image[original_image.shape[0]-1][0]
    t4 = original_image[original_image.shape[0]-1][original_image.shape[1]-1]
    t = min(t1, t2, t3, t4)
    if t > 250:
        bw_img = cv2.adaptiveThreshold(original_image, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 15, 2)
    else:
        thresh, bw_img = cv2.threshold(original_image, t, 255,
                                       cv2.THRESH_BINARY)
    return bw_img


def crop_image(original_image):
    """Crop away whitespace using corner detection.

    Parameters
    ----------
    original_image : numpy.ndarray
        Image to crop.

    Returns
    -------
    numpy.ndarray
        Cropped image padded with a 5 pixel border. If no corners are
        detected the original image is returned.
    """
    cut = 5  # Boundary of image that is definitely not text
    x_list, y_list = [], []
    corners = cv2.goodFeaturesToTrack(original_image, 200, 0.01, 6)

    # goodFeaturesToTrack may return None when no corners are found. In this
    # situation we simply return the original image instead of raising an
    # exception so that further processing can continue.
    if corners is None:
        return original_image

    corners = corners.astype(int)
    for i in corners:
        x, y = i.ravel()
        if x > cut and y > cut:
            x_list.append(x)
            y_list.append(y)

    # When no valid corners are detected after filtering, skip cropping.
    if not x_list or not y_list:
        return original_image

    xl = min(x_list)
    xr = max(x_list)
    yt = min(y_list)
    yb = max(y_list)

    cr_img = cv2.copyMakeBorder(
        original_image[yt:yb, xl:xr], 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=255
    )
    return cr_img


# Closing (Dilation -> Erosion)
def morph_image(original_image):
    """Apply a closing operation to remove small holes."""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 4))
    mor_img = cv2.morphologyEx(original_image, cv2.MORPH_CLOSE, kernel)
    return mor_img


# Blur image
def blur_image(original_image):
    """Blur the image with a 3×3 median filter."""
    return cv2.medianBlur(original_image, 3)


# Return original image
def return_image(original_image):
    """Return the image unchanged."""
    return original_image


def tesseract(given_image):
    """Run Tesseract OCR on the supplied image.

    The environment variable ``TESSERACT_CMD`` can be used to override the
    tesseract executable path.

    Parameters
    ----------
    given_image : numpy.ndarray
        Image to recognise.

    Returns
    -------
    str
        The text recognised by Tesseract.
    """
    cmd = os.getenv('TESSERACT_CMD')
    if cmd:
        pytesseract.pytesseract.tesseract_cmd = cmd
    return pytesseract.image_to_string(given_image, lang='eng')



