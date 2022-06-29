import numpy as np

from .utils.log_business import MyLogger


class RlcFunction:
    """
    Business logic for RLC (Run Length Code) encoding and decoding
    """

    def __init__(self, log_path):
        self.logger = MyLogger('assignment3.function.rlc_function.RlcFunction', log_path)

    @staticmethod
    def trim(array):
        """
        Trims the array to remove the zeros at the end of the array

            Parameters
            ----------
                array : :py:class:`np.ndarray`
                    numpy array of one layer of image

            Returns
            -------
                out : :py:class:`np.ndarray`
                    numpy array of one layer of image without the zeros at the beginning of the array
        """
        trimmed = np.trim_zeros(array, 'b')

        if len(trimmed) == 0:
            trimmed = np.zeros(1)

        return trimmed

    def encode(self, array):
        """
        Encodes an array to RLC (Run Length Code)
        """
        self.logger.info('Encoding array')
        encoded = []
        run_length = 0
        eob = ("EOB",)
        for i in range(len(array)):
            trimmed = self.trim(array[i])
            for j in range(len(array[i])):
                if j == len(trimmed):
                    encoded.append(eob)
                    break
                run_length = self.__relax_next(array, encoded, i, j, run_length, trimmed)
            if not (encoded[-1] == eob):
                encoded.append(eob)
        self.logger.info('Encoded array length: {}'.format(len(encoded)))
        return encoded

    @staticmethod
    def __relax_next(array, encoded, i, j, run_length, trimmed):
        if i == 0 and j == 0:
            encoded.append((int(trimmed[j]).bit_length(), trimmed[j]))
        elif j == 0:
            diff = int(array[i][j] - array[i - 1][j])
            if diff != 0:
                encoded.append((diff.bit_length(), diff))
            else:
                encoded.append((1, diff))
            run_length = 0
        elif trimmed[j] == 0:
            run_length += 1
        else:
            encoded.append((run_length, int(trimmed[j]).bit_length(), trimmed[j]))
            run_length = 0
        return run_length

    def encode_image(self, image):
        """
        Encodes an image to RLC (Run Length Code)
        """
        self.logger.info('Encoding image')
        y, cb, cr = self.convert(image, 'YCbCr')
        y_encoded = self.encode(y)
        cb_encoded = self.encode(cb)
        cr_encoded = self.encode(cr)
        self.logger.info('Encoded image: {}'.format([y_encoded, cb_encoded, cr_encoded]))
        return [y_encoded, cb_encoded, cr_encoded]

    def convert(self, image, mode):
        """
        returns different channels of an image with the specified mode

            Parameters
            ----------
                image : list
                    list of np.ndarray of shape (height, width) of image
                mode : str
                    'YCbCr' or 'RGB'
            Returns
            -------
                out : list
                    list of channels of image with np.ndarray of shape (height, width) of image in the specified mode (YCbCr or RGB)

            Raises
            ------
                ValueError
                    if mode is not 'YCbCr' or 'RGB'
        """
        self.logger.info('Converting image to {} format'.format(mode))
        if mode == 'YCbCr':
            return image[0], image[1], image[2]
        elif mode == 'RGB':
            return image[0], image[1], image[2]
        raise ValueError('Invalid mode')


class ZigZagMovementFunction:
    def __init__(self, log_path):
        self.logger = MyLogger('assignment3.function.rlc_function.ZigZagMovementFunction', log_path)

    def __call__(self, *args, **kwargs):
        """
        Converts a board to a zigzag vector

            Parameters
            ----------
                board : :py:class:`np.ndarray`
                    np.ndarray of shape (height, width) of board to convert
                window_size : int
                    size of the sliding window

            Returns
            -------
                out : :py:class:`np.ndarray`
                    np.ndarray of shape (height * width, window_size * window_size) of zigzagged board
        """
        board = args[0]
        window_size = args[1]
        height, width = board.shape
        matrix = np.zeros(((height * width), window_size * window_size))
        self.logger.info('Converting board to zigzag vector')
        for i in range(0, height, window_size):
            for j in range(0, width, window_size):
                matrix[i * width + j] += self.get_zigzag_vectors(board[i:i + window_size, j:j + window_size])
        return matrix

    @staticmethod
    def get_zigzag_vectors(board):
        """
        Converts a board to a zigzag vector

            Parameters
            ----------
                board : :py:class:`np.ndarray`
                    np.ndarray of shape (height, width) of board to convert
                    note that the board is assumed to be a square matrix with height = width = 8

            Returns
            -------
                out : :py:class:`np.ndarray`
                    np.ndarray of shape (height * width) of zigzag vector
        """
        zigzag = [
            board[0][0], board[0][1], board[1][0], board[2][0], board[1][1], board[0][2],
            board[0][3], board[1][2], board[2][1], board[3][0], board[4][0], board[3][1],
            board[2][2], board[1][3], board[0][4], board[0][5], board[1][4], board[2][3],
            board[3][2], board[4][1], board[5][0], board[6][0], board[5][1], board[4][2],
            board[3][3], board[2][4], board[1][5], board[0][6], board[0][7], board[1][6],
            board[2][5], board[3][4], board[4][3], board[5][2], board[6][1], board[7][0],
            board[7][1], board[6][2], board[5][3], board[4][4], board[3][5], board[2][6],
            board[1][7], board[2][7], board[3][6], board[4][5], board[5][4], board[6][3],
            board[7][2], board[7][3], board[6][4], board[5][5], board[4][6], board[3][7],
            board[4][7], board[5][6], board[6][5], board[7][4], board[7][5], board[6][6],
            board[5][7], board[6][7], board[7][6], board[7][7]
        ]

        return np.array(zigzag).astype(np.int8)
