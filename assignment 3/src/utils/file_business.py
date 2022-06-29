import json
import os.path

from PIL import Image

from .log_business import MyLogger


class FileBusiness:
    def __init__(self):
        self.logger = MyLogger('assignment3.utils.file_business')

    @staticmethod
    def read_image(filepath):
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
        file_path = os.path.join(filepath, 'data', 'config.json')
        with open(file_path) as json_file:
            data = json.load(json_file)
            config = data
        self.logger.info('config file read')
        return config
