import numpy as np
import pytesseract
import cv2
import os


def bw(original_image):
    """Binarise the image and remove noise using the background colour.

    Parameters
    ----------
    original_image : numpy.ndarray
        The grayscale image to be binarised.

    Returns
    -------
    numpy.ndarray
        The thresholded binary image.
    """

    t1 = original_image[0][0]
    t2 = original_image[0][original_image.shape[1]-1]
    t3 = original_image[original_image.shape[0]-1][0]
    t4 = original_image[original_image.shape[0]-1][original_image.shape[1]-1]
    t = min(t1, t2, t3, t4)
    if t > 250:
        bw_img = cv2.adaptiveThreshold(
            original_image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            15,
            2,
        )
    else:
        thresh, bw_img = cv2.threshold(
            original_image,
            t,
            255,
            cv2.THRESH_BINARY,
        )
    return bw_img


def crop_image(original_image):
    """Crop the image to the region that likely contains text.

    Parameters
    ----------
    original_image : numpy.ndarray
        Grayscale image to crop.

    Returns
    -------
    numpy.ndarray
        The cropped image. If no suitable crop region is found, the
        original image is returned untouched.
    """

    cut = 5  # Boundary of image that is definitely not text
    x_list, y_list = [], []
    corners = cv2.goodFeaturesToTrack(original_image, 200, 0.01, 6)

    # goodFeaturesToTrack may return None when no corners are found. In this
    # situation we simply return the original image instead of raising an
    # exception so that further processing can continue.
    if corners is None:
        return original_image

    corners = np.int0(corners)
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


def morph_image(original_image):
    """Perform morphological closing on the image.

    Parameters
    ----------
    original_image : numpy.ndarray
        Image on which closing will be applied.

    Returns
    -------
    numpy.ndarray
        Image after morphological closing.
    """

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 4))
    mor_img = cv2.morphologyEx(original_image, cv2.MORPH_CLOSE, kernel)
    return mor_img


def blur_image(original_image):
    """Apply a median blur to the image.

    Parameters
    ----------
    original_image : numpy.ndarray
        Image to blur.

    Returns
    -------
    numpy.ndarray
        Blurred image.
    """

    return cv2.medianBlur(original_image, 3)


def return_image(original_image):
    """Return the original image unchanged."""
    return original_image


def tesseract(given_image):
    """Run Tesseract OCR on the provided image.

    The path to the ``tesseract`` executable can be specified via the
    ``TESSERACT_CMD`` environment variable.

    Parameters
    ----------
    given_image : numpy.ndarray
        Image to feed into Tesseract.

    Returns
    -------
    str
        The text recognised in the image.
    """

    cmd = os.getenv('TESSERACT_CMD')
    if cmd:
        pytesseract.pytesseract.tesseract_cmd = cmd
    return pytesseract.image_to_string(given_image, lang='eng')



