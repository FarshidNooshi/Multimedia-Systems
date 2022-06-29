import json
import os.path

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from .log_business import MyLogger


class FileBusiness:
    def __init__(self, log_path):
        self.logger = MyLogger('assignment3.utils.file_business', log_path)

    def read_image(self, filepath):
        """
        Reads an image from a filepath and returns a numpy array of shape (height, width, 3) for RGB images

            Parameters
            ----------
                filepath : str
                    filepath of the image
            Returns
            -------
                out : :py:class:`PIL.Image.Image`
                    image with shape (height, width, 3) in RGB format
        """
        filepath = os.path.abspath(filepath)
        image = Image.open(filepath, 'r').convert('RGB')
        self.logger.info('image read')
        return image

    def read_config(self, filepath):
        """
        Reads a config file from the json file at config.json from filepath and returns a dictionary of the config file

            Parameters
            ----------
                filepath : str
                    filepath of the code source folder

            Returns
            -------
                out : dict
                    dictionary of the config file
        """
        file_path = os.path.join(filepath, 'function', 'json', 'config.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
            config = data
        self.logger.info('config file read')
        return config

    def show_image(self, image, title):
        """
        Shows an image

            Parameters
            ----------
                image : :py:class:`np.ndarray`
                    image with shape (height, width, 3) in RGB format
        """
        self.logger.info('Showing image')
        pil_image = Image.fromarray((np.asarray(image) * 255).astype(np.uint8))
        plt.figure(figsize=(10, 5))
        plt.imshow(pil_image)
        plt.title(title)
        plt.show()

