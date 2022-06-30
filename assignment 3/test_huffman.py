import numpy as np

from src.function.huffman import Huffman

if __name__ == "__main__":
    huffman = Huffman(None)
    array = np.array([8, 8, 34, 5, 10, 34, 6, 43, 127, 10, 10, 8, 10, 34, 10])
    total_bits = len(array) * 8

    encode = huffman.encode_array(array)
    total_compressed_bits = sum([len(value) for value in encode.values()])

    print(f'answer:\n{encode}')
    print(f'Input size: {total_bits} bits')
    print(f'Compressed size: {total_compressed_bits} bits')
    print(f'Compression Ratio: {np.round(total_bits / total_compressed_bits)}')
