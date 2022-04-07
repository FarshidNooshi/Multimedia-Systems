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
    gray = gray.astype(int)
    plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    plt.show()
    return gray


def section_two(number_of_bins=40):
    data = section_one()
    data_1d = data.flatten()
    plt.hist(data_1d, density=True, bins=number_of_bins)
    plt.show()
    return data


def section_three():
    data = section_two(number_of_bins=40)
    data_flattened = data.flatten()
    counter = dict(sorted(collections.Counter(data_flattened).items()))
    counter_keys = counter.keys()
    counter_values = counter.values()
    counter_values = [i for i in counter_values]
    for i in range(1, len(counter_values)):
        counter_values[i] = counter_values[i] + counter_values[i - 1]
    counter_values = np.array(counter_values)
    counter_keys = np.array([i for i in counter_keys])
    return dict(zip(counter_keys, counter_values)), data


def section_four(*args, **kwargs):
    return round((kwargs['color_levels'] - 1) * kwargs['cumulative_sum'][args[0]] / (
            kwargs['image_height'] * kwargs['image_weight']))


def section_five():
    cumulative_sum, data = section_three()
    new_image_array = np.zeros(data.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            new_image_array[i][j] = section_four(data[i][j], color_levels=len(cumulative_sum.keys()),
                                                 cumulative_sum=cumulative_sum, image_height=data.shape[0],
                                                 image_weight=data.shape[1])
    plt.imshow(new_image_array, cmap='gray', vmin=0, vmax=255)
    plt.show()


section_five()
