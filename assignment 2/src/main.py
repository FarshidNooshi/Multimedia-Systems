import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.5870, 0.1140])


# address = input('please enter address of image: ')
address = '/Volumes/Farshid_SSD/Projects/University/MultiMediaSystems/assignment 2/assets/image.png'
image = Image.open(address)
print(image.mode)

im_arr = np.array(image)

plt.imshow(rgb2gray(im_arr), cmap='gray', vmin=0, vmax=255)
plt.show()
