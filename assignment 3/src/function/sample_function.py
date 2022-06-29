import os.path

import numpy as np
from scipy.signal import convolve2d

from .utils.file_business import FileBusiness
from .utils.log_business import MyLogger


class SamplingFunction:
    def __init__(self, log_path):
        self.logger = MyLogger('assignment3.utils.sampling_function', log_path)

    def sample(self, image, mode):
        """
        Samples the image with the given sampling factors
            Parameters
            ----------
                image : :py:class:`np.ndarray`
                    np.ndarray or PIL.Image.Image of shape (height, width, 3) of image
                mode : str
                    mode of chroma subsampling ('4:4:4', '4:2:2', '4:2:0', '4:4:0', '4:1:1')

            Returns
            -------
                out : tuple[:py:class:`np.ndarray`, :py:class:`np.ndarray`, :py:class:`np.ndarray`]
                    tuple of three numpy arrays of for Y, Cr, Cb

            Raises
            ------
                NotImplementedError
                    if mode is '4:4:4', '4:2:2', '4:4:0', '4:1:1'
                TypeError
                    if mode is '4:2:0' and image is not of type np.ndarray
        """

        if mode != '4:2:0':
            raise NotImplementedError('Mode {} is not implemented'.format(mode))
        if type(image) is not np.ndarray:
            raise TypeError('Image must be in numpy array format')
        self.logger.debug('Sampling image with mode {}'.format(mode))
        if mode == '4:2:0':
            y, cr, cb = self.__sample_422(image[:, :, 0], image[:, :, 1], image[:, :, 2])
        return y, cr, cb

    def __sample_422(self, y, cr, cb):
        y = y - 128
        cr = cr - 128
        cb = cb - 128

        SSH, SSV = 2, 2

        kernel = np.array([[0.25, 0.25], [0.25, 0.25]])

        # subsampling
        cr = np.repeat(np.repeat(convolve2d(cr, kernel, mode='valid')[::SSV, ::SSH], 2, axis=0), 2, axis=1)
        cb = np.repeat(np.repeat(convolve2d(cb, kernel, mode='valid')[::SSV, ::SSH], 2, axis=0), 2, axis=1)

        self.logger.debug('shape of image after sampling: {}, 3'.format(cr.shape))
        return y, cr, cb
