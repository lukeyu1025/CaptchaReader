import pytest

np = pytest.importorskip('numpy')
cv2 = pytest.importorskip('cv2')

from Preprocessing import crop_image


def test_crop_image_returns_original_when_no_corners():
    img = np.full((10, 10), 255, dtype=np.uint8)
    result = crop_image(img)
    assert np.array_equal(result, img)


def test_crop_image_returns_original_when_not_enough_corners():
    img = np.full((10, 10), 255, dtype=np.uint8)
    img[5, 5] = 0  # single black pixel to create a single corner
    result = crop_image(img)
    assert np.array_equal(result, img)


def test_crop_image_crops_with_multiple_corners():
    img = np.full((20, 20), 255, dtype=np.uint8)
    cv2.rectangle(img, (5, 5), (14, 14), 0, 1)
    result = crop_image(img)
    assert result.shape == (19, 19)
    assert not np.array_equal(result, img)
