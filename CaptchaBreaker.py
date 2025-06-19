"""Command line interface for the CAPTCHA toolkit."""

import argparse
import process_manage
import cv2
from load import get_image

def menu():
    """Prompt the user to choose an action."""
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


def run_process(path, order=None):
    """Process a single image and display the result."""
    image, label = get_image(path)
    sel_order = process_manage.choose_process(order)
    res = process_manage.process(image, sel_order)
    res.show()
    print(label)


def main():
    """Entry point for command line execution."""
    parser = argparse.ArgumentParser(description='Captcha recognition toolkit')
    parser.add_argument('--process', metavar='IMAGE', help='Preprocess an image')
    parser.add_argument('--rate', metavar='DIR', help='Show success rate for dataset')
    parser.add_argument('--order', metavar='ORDER', help='Preprocessing order e.g. 1234')
    args = parser.parse_args()

    if args.process:
        run_process(args.process, args.order)
        return
    if args.rate:
        process_manage.show_rate(args.rate, args.order, pause=False)
        return

    while True:
        choice = menu()
        if choice == 1:
            print('Enter full path for image')
            get_input = str(input())
            try:
                run_process(get_input)
            except FileNotFoundError as e:
                print(e)
            except cv2.error:
                print('Error reading the image. Please provide a valid image file.\n')
        elif choice == 2:
            process_manage.show_rate()
        elif choice == 3:
            raise SystemExit


if __name__ == '__main__':
    main()
