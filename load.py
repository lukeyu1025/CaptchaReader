"""Utility helpers for loading images."""

import cv2


def get_image(path):
    """Load an image in grayscale and derive its label from the filename.

    Parameters
    ----------
    path : str
        Path to the image file.

    Returns
    -------
    tuple[numpy.ndarray, str]
        The grayscale image and the file stem used as its label.

    Raises
    ------
    FileNotFoundError
        If the image cannot be read from ``path``.
    """
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]

    loaded_image = cv2.imread(path)
    if loaded_image is None:
        raise FileNotFoundError(f"Unable to load image from '{path}'.")
    loaded_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
    label = ((path.split('/')[-1]).split('\\')[-1]).split('.')[0]
    return loaded_image, label
