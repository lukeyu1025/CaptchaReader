import pytest

np = pytest.importorskip('numpy')
cv2 = pytest.importorskip('cv2')

from Preprocessing import bw, morph_image, blur_image


def test_bw_returns_binary_image():
    img = np.full((10, 10), 255, dtype=np.uint8)
    result = bw(img)
    assert result.dtype == np.uint8
    assert set(np.unique(result)).issubset({0, 255})


def test_morph_image_closing():
    img = np.zeros((5, 5), dtype=np.uint8)
    img[1:4, 1:4] = 255
    img[2, 2] = 0
    result = morph_image(img)
    assert result[2, 2] == 255


def test_blur_image_removes_noise():
    img = np.full((5, 5), 255, dtype=np.uint8)
    img[2, 2] = 0
    result = blur_image(img)
    assert result[2, 2] == 255
