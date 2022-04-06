import collections

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.5870, 0.1140])


def image_read():
    # address = input('please enter address of image: ')
    address = '/Volumes/Farshid_SSD/Projects/University/MultiMediaSystems/assignment 2/assets/image.png'
    image = Image.open(address)
    print('for test, pixel at position(1, 25) is ' + image.getpixel((1, 25)).__str__())
    return image


def section_one():
    image = image_read()
    print('mode of initial image: ' + image.mode)
    im_arr = np.array(image)
    gray = rgb2gray(im_arr)
    plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    plt.show()
    return gray


def section_two(number_of_bins=40):
    data = section_one()
    data_1d = data.flatten()
    plt.hist(data_1d, density=True, bins=number_of_bins)
    plt.show()


