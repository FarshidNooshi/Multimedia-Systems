import numpy as np

from .log_business import MyLogger


class ConverterBusiness:
    """
    Business logic for converting to YCbCr format from RGB format from numpy array of shape
    (height, width, 3) of image  and returns a numpy array of shape (height, width, 3) for image in YCbCr format
    or vice versa (RGB: red, green, blue) (YCbCr: Y, Cb: blue-difference, Cr: red-difference)

        Methods
        -------
            convert_to_np_array(image)
                Converts an image to a numpy array
            convert(image, mode)
                Converts an image to YCbCr format from RGB format from numpy array of shape (height, width, 3) of image
                and returns a numpy array of shape (height, width, 3) for image in YCbCr format or vice versa
                (RGB: red, green, blue) (YCbCr: Y, Cb: blue-difference, Cr: red-difference)
            __convert_to_YCbCr(image)
                private method which converts an image to YCbCr
                (Y: luminance, Cb: blue-difference, Cr: red-difference) from RGB and returns a numpy array
                of shape (height, width, 3) for image in YCbCr format
            __convert_to_rgb(image)
                private method which converts an image to RGB format from YCbCr
                (Y: luminance, Cb: blue-difference, Cr: red-difference) and returns a numpy array
                of shape (height, width, 3) for image in RGB format
    """

    def __init__(self):
        self.logger = MyLogger('assignment3.utils.converter_business')

    @staticmethod
    def convert_to_np_array(image):
        """
        Converts an image to a numpy array

            Parameters
            ----------
                image : :py:class:`PIL.Image.Image`
                    image of shape (height, width, 3) of image

            Returns
            -------
                out : :py:class:`np.ndarray`
                    numpy of shape (height, width, 3) of image

        """
        return np.array(image)

    def convert(self, image, mode):
        """
        Converts an image to YCbCr (Y: luminance, Cb: blue-difference, Cr: red-difference) from RGB or vice versa

            Parameters
            ----------
                image : :py:class:`np.ndarray` or :py:class:`PIL.Image.Image`
                    np.ndarray or PIL.Image.Image of shape (height, width, 3) of image
                mode : str
                    'YCbCr' or 'RGB'

            Returns
            -------
                out : :py:class:`np.ndarray`
                    np.ndarray of shape (height, width, 3) of image in the specified mode (YCbCr or RGB)

            Raises
            ------
                ValueError
                    if mode is not 'YCbCr' or 'RGB'
        """
        if type(image) is not np.ndarray:
            image = self.convert_to_np_array(image)
        self.logger.info('Converting image to {} format'.format(mode))
        if mode == 'YCbCr':
            return self.__convert_to_YCbCr(image)
        elif mode == 'RGB':
            return self.__convert_to_rgb(image)
        else:
            self.logger.error('Invalid mode')
            raise ValueError('Invalid mode')

    @staticmethod
    def __convert_to_YCbCr(image):
        """
        Converts an image to YCbCr (Y, Cb, Cr) format (Y: luminance, Cb: blue-difference, Cr: red-difference) from RGB

            Parameters
            ----------
                image : :py:class:`np.ndarray`
                    np.ndarray of shape (height, width, 3) of image

            Returns
            -------
                out : :py:class:`np.ndarray`
                    np.ndarray of shape (height, width, 3) of image in YCbCr format
        """
        transform_matrix = np.array([[0.299, 0.587, 0.114],
                                     [-0.168736, -0.331264, 0.5],
                                     [0.5, -0.418688, -0.081312]])
        mult = np.dot(image, transform_matrix.T)
        mult[:, :, 1:2] += 128
        return mult

    @staticmethod
    def __convert_to_rgb(image):
        """
        Converts an image to RGB format from YCbCr (Y: luminance, Cb: blue-difference, Cr: red-difference)

            Parameters
            ----------
                image : :py:class:`np.ndarray`
                    np.ndarray of shape (height, width, 3) of image

            Returns
            -------
                out : :py:class:`np.ndarray`
                    np.ndarray of shape (height, width, 3) of image in RGB format
        """
        transform_matrix = np.array([[1, 0, 1.402],
                                     [1, -0.34414, -0.71414],
                                     [1, 1.772, 0]])
        rgb_arr = image.astype(np.float32)
        rgb_arr[:, :, 1:2] -= 128
        mult = np.dot(image, transform_matrix.T)
        mult.putmask(mult > 255, 255)
        mult.putmask(mult < 0, 0)
        return mult.astype(np.uint8)
