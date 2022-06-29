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

    def quantize(self, layers):
        window_size = len(QTC)
        if self.check_for_padding(layers, window_size):
            y_padded, cb_padded, cr_padded = self.pad_image(layers, window_size)
            y, cb, cr = self.perform_dct([y_padded, cb_padded, cr_padded], window_size)
        else:
            y, cb, cr = self.perform_dct(layers, window_size)
        return self.quantify_image([y, cb, cr], window_size)

    @staticmethod
    def check_for_padding(layers, window_size):
        y, cb, cr = layers[0], layers[1], layers[2]
        if len(y) % window_size != 0 or len(cb) % window_size != 0 or len(cr) % window_size != 0:
            return True
        if len(y[0]) % window_size != 0 or len(cb[0]) % window_size != 0 or len(cr[0]) % window_size != 0:
            return True
        return False

    @staticmethod
    def pad_image(layers, window_size):
        """
        Pads the image with zeros to make it divisible by window_size in both dimensions

            Parameters
            ----------
                layers : list[numpy.ndarray]
                    List of layers to pad
                window_size : int
                    size of the window

            Returns
            -------
                out : list[:py:class:`np.ndarray`, :py:class:`np.ndarray`, :py:class:`np.ndarray`]
                    list of three numpy arrays of for Y, Cr, Cb after padding
        """
        for layer in layers:
            image_layer = layer.copy()
            if len(image_layer) % window_size != 0:
                new_block = np.zeros((window_size - (len(image_layer) % window_size), len(image_layer[0])))
                image_layer = np.concatenate((image_layer, new_block), axis=0)
            if len(image_layer[0]) % window_size != 0:
                new_block = np.zeros((len(image_layer), window_size - (len(image_layer[0]) % window_size)))
                image_layer = np.concatenate((image_layer, new_block), axis=1)
            yield image_layer

    @staticmethod
    def perform_dct(layers, windows_size):
        layers_dct_list = []
        height = len(layers[0])
        width = len(layers[0][0])
        for layer in layers:
            old_layer = layer.copy()
            for i in range(0, height, windows_size):
                for j in range(0, width, windows_size):
                    from scipy.fftpack import dct
                    layer[i:i + windows_size, j:j + windows_size] = \
                        dct(old_layer[i:i + windows_size, j:j + windows_size], norm='ortho')
            layers_dct_list.append(layer)
        return layers_dct_list

    @staticmethod
    def quantify_image(layers, windows_size):
        layers_quantified_list = []
        height = len(layers[0])
        width = len(layers[0][0])
        for num, layer in enumerate(layers):
            old_dct_values = layer.copy()
            for i in range(0, height, windows_size):
                for j in range(0, width, windows_size):
                    if num == 0:
                        layer[i:i + windows_size, j:j + windows_size] = \
                            np.ceil(old_dct_values[i:i + windows_size, j:j + windows_size] / QTY)
                    else:
                        layer[i:i + windows_size, j:j + windows_size] = \
                            np.ceil(old_dct_values[i:i + windows_size, j:j + windows_size] / QTC)
            layers_quantified_list.append(layer)
        return layers_quantified_list
