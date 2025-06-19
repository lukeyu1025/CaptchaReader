import process_manage
import cv2
from load import get_image

def menu():
    """Prompt the user for an action and return the chosen option.

    Returns
    -------
    int
        The selected menu item where ``1`` preprocesses an image,
        ``2`` shows the dataset success rate and ``3`` quits the
        application.
    """

    print('Choose operation')
    print('1. Preprocess image')
    print('2. Show success rate for dataset')
    print('3. Quit')
    while True:
        try:
            sel = int(input())
            if 0 < sel < 4:
                return sel
            else:
                print('Please choose again')
        except ValueError:
            print('Please choose again')


if __name__ == '__main__':
    while True:
        choice = menu()
        if choice == 1:
            print('Enter full path for image')
            get_input = str(input()) #input of path
            try:
                image, label = get_image(get_input)  # use path to get image
                sel_order = process_manage.choose_process()
                res = process_manage.process(image, sel_order)
                res.show()
                print(label)
            except FileNotFoundError as e:
                print(e)
            except cv2.error:
                print('Error reading the image. Please provide a valid image file.\n')
        elif choice == 2:
            process_manage.show_rate()
        elif choice == 3:
            raise SystemExit
