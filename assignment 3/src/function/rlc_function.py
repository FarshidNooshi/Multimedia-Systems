import numpy as np

from .utils.log_business import MyLogger


class RlcFunction:
    """
    Business logic for RLC (Run Length Code) encoding and decoding
    """

    def __init__(self, log_path):
        self.logger = MyLogger('assignment3.function.rlc_function.RlcFunction', log_path)

    def encode(self, vector):
        """
        Encodes a vector to RLC (Run Length Code)
        """
        rlc_vector = []
        current_run_length = 1
        for i in range(1, len(vector)):
            if vector[i] == vector[i - 1]:
                current_run_length += 1
            else:
                rlc_vector.append(current_run_length)
                rlc_vector.append(vector[i - 1])
                current_run_length = 1
        rlc_vector.append(current_run_length)
        rlc_vector.append(vector[-1])
        return rlc_vector

    def decode(self, rlc_vector):
        """
        Decodes a RLC vector to a vector
        """
        vector = []
        for i in range(0, len(rlc_vector), 2):
            vector.extend([rlc_vector[i + 1]] * rlc_vector[i])
        return vector


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
        matrix = np.array((height * width, window_size * window_size))
        for i in range(height):
            for j in range(width):
                matrix[i * width + j] = self.__call__(board[i:i + window_size, j:j + window_size])
        return matrix

    def get_zigzag_vectors(self, board):
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
        self.logger.debug('Converting 8*8 board to zigzag vector')
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

        return zigzag
