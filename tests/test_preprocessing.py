import pytest

np = pytest.importorskip('numpy')
cv2 = pytest.importorskip('cv2')

from Preprocessing import bw, morph_image, blur_image


def test_bw_threshold_path():
    # image with black corners -> threshold should use global thresholding
    img = np.full((3, 3), 255, dtype=np.uint8)
    img[0, 0] = img[0, 2] = img[2, 0] = img[2, 2] = 0
    result = bw(img)
    # corners remain black, others white
    expected = img.copy()
    expected[1, 0] = expected[0, 1] = expected[1, 2] = expected[2, 1] = 255
    expected[1, 1] = 255
    assert np.array_equal(result, expected)


def test_bw_adaptive_path():
    # image entirely white -> adaptive threshold keeps it white
    img = np.full((3, 3), 255, dtype=np.uint8)
    result = bw(img)
    assert np.array_equal(result, img)


def test_morph_image_closing_fills_hole():
    img = np.full((5, 5), 255, dtype=np.uint8)
    img[2, 2] = 0
    result = morph_image(img)
    assert result[2, 2] == 255


def test_blur_image_median():
    img = np.full((3, 3), 255, dtype=np.uint8)
    img[1, 1] = 0
    result = blur_image(img)
    assert result[1, 1] == 255
