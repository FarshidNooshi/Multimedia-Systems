import collections

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def get_address(get_input=True):
    if get_input:
        return input('please enter address of image: ')
    return input('please enter address for saving result: ')


def image_read():
    address = get_address()
    image = Image.open(address)
    print('for test, pixel at position(1, 25) is ' + image.getpixel((1, 25)).__str__())
    return image


def section_one():
    image = image_read()
    print('mode of initial image: ' + image.mode)
    im_arr = np.array(image)
    gray = rgb2gray(im_arr).astype(int)
    plt.imshow(gray, cmap='gray', vmin=0, vmax=255)
    plt.show()
    return gray


def section_two(data):
    data_1d = data.flatten().astype(int)
    count = np.zeros(256)
    for i in range(len(data_1d)):
        count[data_1d[i]] += 1
    pixels = np.arange(0, 256, 1)
    plt.bar(pixels, count)
    plt.xlabel('color')
    plt.ylabel('count')
    plt.show()
    return count


def section_three(data):
    count = section_two(data=data)
    counter_keys = np.arange(0, 256, 1)
    counter_values = count
    for i in range(1, len(counter_values)):
        counter_values[i] = counter_values[i] + counter_values[i - 1]
    plt.bar(counter_keys, counter_values)
    plt.xlabel('color')
    plt.ylabel('count')
    plt.show()
    return dict(zip(counter_keys, counter_values))


def section_four(*args, **kwargs):
    return round((kwargs['color_levels'] - 1) * kwargs['cumulative_sum'][args[0]] / (
            kwargs['image_height'] * kwargs['image_weight']))


def section_five(**kwargs):
    data = kwargs.get('data', section_one())
    cumulative_sum = section_three(data)
    new_image_array = np.zeros(data.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            new_image_array[i][j] = section_four(data[i][j], color_levels=kwargs.get('number_of_levels',
                                                                                     len(cumulative_sum.keys())),
                                                 cumulative_sum=cumulative_sum, image_height=data.shape[0],
                                                 image_weight=data.shape[1])
    plt.imshow(new_image_array, cmap='gray', vmin=0, vmax=255)
    plt.show()
    return new_image_array, cumulative_sum


def save_image(image_pixels, identifier):
    address = get_address(get_input=False)
    image = Image.fromarray(image_pixels).convert('LA')
    image.save(f'{address}/result_{identifier}.png')


new_image_arr, cumulative_sum_dict = section_five()
save_image(new_image_arr, identifier='sample')

cumulative_sum_dict_final = section_three(data=new_image_arr)
