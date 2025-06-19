import cv2

# Get image from external file(path)
def get_image(path):
    # Remove quotes from the provided path if present
    if path.startswith('"') and path.endswith('"'):
        path = path[1:-1]

    loaded_image = cv2.imread(path)
    if loaded_image is None:
        raise FileNotFoundError(f"Unable to load image from '{path}'.")
    loaded_image = cv2.cvtColor(loaded_image, cv2.COLOR_BGR2GRAY)
    label = ((path.split('/')[-1]).split('\\')[-1]).split('.')[0]
    return loaded_image, label
