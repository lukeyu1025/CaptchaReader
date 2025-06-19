import numpy as np
from matplotlib import pyplot as plt
import fnmatch
import os
import glob
import logging

logging.basicConfig(level=logging.ERROR)

import Preprocessing
from load import get_image


class Result:
    """Container for processed captcha results."""

    def __init__(self, order, images, text):
        """Create a ``Result`` instance.

        Parameters
        ----------
        order : list of callable
            Functions that were applied to the image.
        images : list of numpy.ndarray
            Intermediate images produced for each step.
        text : str
            Text returned by Tesseract.
        """

        self.order = order
        self.images = images
        self.text = text

    def show(self):
        """Display each processing step and the recognised text."""

        titles = ['Original']
        images = [self.images[0]]
        for i in range(4):
            if self.order[i] == Preprocessing.bw:
                titles.append('Binarise')
                images.append(self.images[i + 1])
            elif self.order[i] == Preprocessing.crop_image:
                titles.append('Crop')
                images.append(self.images[i + 1])
            elif self.order[i] == Preprocessing.morph_image:
                titles.append('Close')
                images.append(self.images[i + 1])
            elif self.order[i] == Preprocessing.blur_image:
                titles.append('Blur')
                images.append(self.images[i + 1])
            elif self.order[i] == Preprocessing.return_image:
                continue
        titles.append('Text')
        empty = np.zeros((images[-1].shape[0], images[-1].shape[1], 3), np.uint8)
        empty[:] = (255, 255, 255)
        images.append(empty)

        for i in range(len(titles)):
            plt.subplot(1, len(titles), i + 1)
            plt.imshow(images[i], 'gray')
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
        ax = plt.gca()

        plt.text(
            0.5,
            0,
            self.text,
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=13,
        )
        plt.show()


def process(original_image, order):
    """Run the selected preprocessing pipeline on an image.

    Parameters
    ----------
    original_image : numpy.ndarray
        The image to be processed.
    order : list of callable
        List of processing functions to apply sequentially.

    Returns
    -------
    Result
        The result containing intermediate images and OCR text.
    """

    images = [original_image]
    images.append(order[0](original_image))
    images.append(order[1](images[1]))
    images.append(order[2](images[2]))
    images.append(order[3](images[3]))
    text = Preprocessing.tesseract(images[4])
    return Result(order, images, text)


def choose_process():
    """Ask the user for a processing order.

    Returns
    -------
    list of callable
        Functions representing the chosen processing steps.
    """

    steps = [
        Preprocessing.bw,
        Preprocessing.crop_image,
        Preprocessing.morph_image,
        Preprocessing.blur_image,
    ]
    order = []
    print('Choose order of processing')
    print('1. Binarisation  2.Cropping  3.Closing   4.Blurring')

    get_order = input()
    for i in range(4):
        try:
            order.append(steps[int(get_order[i]) - 1])
        except IndexError:
            order.append(Preprocessing.return_image)
    return order


def show_rate():
    """Display OCR accuracy statistics for a dataset of captcha images."""

    current_path = os.path.dirname(__file__)
    print('* Current path = ' + current_path)
    print('Enter path of dataset')
    while True:
        try:
            data_path = input()
            total = len(fnmatch.filter(os.listdir(data_path), '*.png'))
            break
        except FileNotFoundError:
            print('Wrong path. Try again.')

    order = choose_process()

    count = letter_correct = correct = 0
    for f in glob.glob(data_path + '/*.png'):
        count += 1
        original_image, label = get_image(f)
        try:
            processed_image = process(original_image, order)
            if processed_image.text.strip() == label:
                correct += 1
            for i in range(min(len(processed_image.text), len(label))):
                if processed_image.text[i] == label[i]:
                    letter_correct += 1
        except Exception as e:
            logging.error('Error occured in processing image %s: %s', label, e)
            print('\r{0: .2f}% complete..'.format((count * 100) / total), end='')
            continue
        print('\r{0: .2f}% complete..'.format((count * 100) / total), end='')

    print('')
    print(
        '\tOut of {0} letters {1} were correctly read.'
        'Success Rate: {2:.2f}%'
        .format(total * 6, letter_correct, (letter_correct * 100) / (total * 6))
    )
    print(
        '\tOut of {0} captcha images, {1} were correctly read.'
        'Success Rate: {2:.2f}%'
        .format(total, correct, (correct * 100) / total)
    )
    print('Press any key to continue.')

    input()
