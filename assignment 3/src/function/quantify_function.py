import numpy as np

from .utils.log_business import MyLogger

QTY = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 48, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])

# chrominance quantization table
QTC = np.array([
    [17, 18, 24, 47, 99, 99, 99, 99],
    [18, 21, 26, 66, 99, 99, 99, 99],
    [24, 26, 56, 99, 99, 99, 99, 99],
    [47, 66, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99]
])


class QuantifyingFunction:
    def __init__(self, log_path):
        self.logger = MyLogger('assignment3.utils.quantifying_function', log_path)

    def quantize(self, image):
        window_size = len(QTC[0])
        if self.check_for_padding(image, window_size):
            y, cb, cr = self.pad_image(image, window_size)
        y, cb, cr = self.perform_dct([y, cb, cr])

    @staticmethod
    def check_for_padding(image, window_size):
        y, cb, cr = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        if len(y[0]) % window_size != 0 or len(cb[0]) % window_size != 0 or len(cr[0]) % window_size != 0:
            return True
        if len(y[1]) % window_size != 0 or len(cb[1]) % window_size != 0 or len(cr[1]) % window_size != 0:
            return True
        return False

    @staticmethod
    def pad_image(image, window_size):
        """
        Pads the image with zeros to make it divisible by window_size in both dimensions

            Parameters
            ----------
                image : :py:class:`np.ndarray`
                    np.ndarray or of shape (height, width, 3) of image
                window_size : int
                    size of the window

            Returns
            -------
                out : tuple[:py:class:`np.ndarray`, :py:class:`np.ndarray`, :py:class:`np.ndarray`]
                    tuple of three numpy arrays of for Y, Cr, Cb after padding
        """
        for layer in range(3):
            image_layer = image[:, :, layer]
            if len(image_layer) % window_size != 0:
                new_block = np.zeros((window_size - (len(image_layer) % window_size), len(image_layer[0])))
                image_layer = np.concatenate((image_layer, new_block), axis=0)
            if len(image_layer[0]) % window_size != 0:
                new_block = np.zeros((len(image_layer), window_size - (len(image_layer[0]) % window_size)))
                image_layer = np.concatenate((image_layer, new_block), axis=1)
            yield image_layer

    @staticmethod
    def perform_dct(layers):
        dct_3d = []
        height = len(layers[0])
        width = len(layers[0][0])
        for layer in layers:
            old_layer = layer.copy()
            for i in range(0, height, 8):
                for j in range(0, width, 8):
                    from scipy.fftpack import dct
                    layer[i:i + 8, j:j + 8] = dct(old_layer[i:i + 8, j:j + 8], norm='ortho')
            dct_3d.append(layer)
        return dct_3d
