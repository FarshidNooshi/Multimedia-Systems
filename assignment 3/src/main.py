import os.path

import numpy as np

from function.huffman import Huffman
from function.quantify_function import QuantifyingFunction, QTC
from function.rlc_function import ZigZagMovementFunction, RlcFunction
from function.sample_function import SamplingFunction
from function.utils.converter_business import ConverterBusiness
from function.utils.file_business import FileBusiness
from function.utils.log_business import MyLogger


def calculateTotalNumberOfBitsWithoutCompression(ch_y, ch_cb, ch_cr):
    return len(ch_y) * len(ch_y[0]) * 8 + len(ch_cb) * len(ch_cb[0]) * 8 + len(ch_cr) * len(ch_cr[0]) * 8


if __name__ == '__main__':
    config = FileBusiness(None).read_config(os.getcwd())
    log_path = config.get('log_path')
    output_path = config.get('output_path')
    os.chdir('../')
    logger = MyLogger('assignment3.main', log_path)
    converter = ConverterBusiness(log_path)
    file_manager = FileBusiness(log_path)
    sampler = SamplingFunction(log_path)
    quantifier = QuantifyingFunction(log_path)
    zigzag = ZigZagMovementFunction(log_path)
    rlcEncoder = RlcFunction(log_path)
    huffman = Huffman(log_path)
    window_size = len(QTC)
    ####################################################################################################################

    # start of the program
    logger.info('Starting program')
    logger.info('Changing directory to ' + os.getcwd())
    image = file_manager.read_image(config.get('image_path'))
    logger.info('Reading image from ' + config.get('image_path'))
    logger.info('Image shape: ' + str(image.info))
    ####################################################################################################################

    # convert image to YCbCr
    ycbcr = converter.convert(image, mode='YCbCr')
    logger.info('Converting image to YCbCr')
    logger.info(f'Image shape: {ycbcr.shape}')
    file_manager.show_image(ycbcr, 'YCbCr image converted from RGB')
    ####################################################################################################################

    # sample the image
    y, cb, cr = ycbcr[:, :, 0], ycbcr[:, :, 1], ycbcr[:, :, 2]
    totalNumberOfBitsWithoutCompression = calculateTotalNumberOfBitsWithoutCompression(y, cb, cr)
    logger.debug('subsampling image')
    y, cb, cr = sampler.sample(ycbcr, config.get('chroma_subsampling'))
    logger.debug('y shape: {}'.format(y.shape))
    ####################################################################################################################

    # quantize the image
    logger.debug('quantifying image')
    y, cb, cr = quantifier.quantize([y, cb, cr])
    logger.debug('y shape: {}'.format(y.shape))
    logger.debug('cb shape: {}'.format(cb.shape))
    logger.debug('cr shape: {}'.format(cr.shape))
    ####################################################################################################################

    # zig-zag movement
    logger.debug('zig-zag movement')
    y = zigzag(y, window_size).astype(np.uint16)
    cb = zigzag(cb, window_size).astype(np.uint16)
    cr = zigzag(cr, window_size).astype(np.uint16)
    # y, cb, cr = zigzag(y, cb, cr, 8)
    logger.debug('y shape: {}'.format(y.shape))
    logger.debug('cb shape: {}'.format(cb.shape))
    logger.debug('cr shape: {}'.format(cr.shape))
    ####################################################################################################################

    # rlc encoding
    logger.debug('rlc encoding')
    y_encoded, cb_encoded, cr_encoded = rlcEncoder.encode_image([y, cb, cr])
    logger.debug('y_encoded len: {}'.format(len(y_encoded)))
    logger.debug('cb_encoded len: {}'.format(len(cb_encoded)))
    logger.debug('cr_encoded len: {}'.format(len(cr_encoded)))
    ####################################################################################################################

    # huffman encoding
    logger.debug('huffman encoding')
    y_huffman = huffman.encode_array(y_encoded)
    cb_huffman = huffman.encode_array(cb_encoded)
    cr_huffman = huffman.encode_array(cr_encoded)
    ####################################################################################################################

    # save the results
    logger.debug('Saving results')
    file_manager.save_image([y_encoded, cb_encoded, cr_encoded], os.path.join(output_path, 'encoded.pickle'))
    file_manager.save_codes([y_huffman, cb_huffman, cr_huffman], os.path.join(output_path, 'huffman.pickle'))
    file_manager.save_image(ycbcr, os.path.join(output_path, 'original.pickle'))
    ####################################################################################################################

    # calculate the compression ratio
    logger.debug('Calculating compression ratio')
    y_bits = ''.join([y_huffman[value] for value in y_encoded])
    cb_bits = ''.join([cb_huffman[value] for value in cb_encoded])
    cr_bits = ''.join([cr_huffman[value] for value in cr_encoded])
    compression_ratio = np.round(totalNumberOfBitsWithoutCompression / (len(y_bits) + len(cb_bits) + len(cr_bits)), 2)
    logger.critical(f'Compressed image size: {np.round((len(y_bits) + len(cb_bits) + len(cr_bits)) / 1024)} kb')
    logger.critical(f'size before compression: {np.round(totalNumberOfBitsWithoutCompression / 1024)} kb')
    logger.critical(f'Compression ratio: {compression_ratio}')
    ####################################################################################################################
