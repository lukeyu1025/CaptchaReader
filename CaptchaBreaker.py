import argparse
import process_manage
import cv2
from load import get_image


def parse_args():
    parser = argparse.ArgumentParser(
        description='Run captcha preprocessing or evaluate a dataset.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--image', help='Path to a single image to process')
    group.add_argument('-d', '--dataset', help='Path to a folder of captcha images')
    return parser.parse_args()

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
    args = parse_args()
    if args.image:
        try:
            image, label = get_image(args.image)
            sel_order = process_manage.choose_process()
            res = process_manage.process(image, sel_order)
            res.show()
            print(label)
        except FileNotFoundError as e:
            print(e)
        except cv2.error:
            print('Error reading the image. Please provide a valid image file.\n')
    elif args.dataset:
        try:
            process_manage.show_rate(args.dataset)
        except FileNotFoundError as e:
            print(e)
    else:
        while True:
            choice = menu()
            if choice == 1:
                print('Enter full path for image')
                get_input = str(input())  # input of path
                try:
                    image, label = get_image(get_input)
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
