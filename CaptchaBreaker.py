import process_manage
import cv2
from load import get_image

def menu():
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
                if image is not None:
                    sel_order = process_manage.choose_process()
                    res = process_manage.process(image, sel_order)
                    res.show()
                    print(label)
                else:
                    print('Invalid path or image file. Please try again.\n')
            except cv2.error:
                print('Error reading the image. Please provide a valid image file.\n')
        elif choice == 2:
            process_manage.show_rate()
        elif choice == 3:
            raise SystemExit