import os.path

import numpy as np

from function.sample_function import SamplingFunction
from function.utils.converter_business import ConverterBusiness
from function.utils.file_business import FileBusiness
from function.utils.log_business import MyLogger
from function.quantify_function import QuantifyingFunction


def calculateTotalNumberOfBitsWithoutCompression(ch_y, ch_cb, ch_cr):
    return len(ch_y) * len(ch_y[0]) * 8 + len(ch_cb) * len(ch_cb[0]) * 8 + len(ch_cr) * len(ch_cr[0]) * 8


if __name__ == '__main__':
    config = FileBusiness(None).read_config(os.getcwd())
    log_path = config.get('log_path')
    os.chdir('../')
    logger = MyLogger('assignment3.main', log_path)
    converter = ConverterBusiness(log_path)
    file_manager = FileBusiness(log_path)
    sampler = SamplingFunction(log_path)
    quantifier = QuantifyingFunction(log_path)

    # start of the program
    logger.info('Starting program')
    logger.info('Changing directory to ' + os.getcwd())
    image = file_manager.read_image(config.get('image_path'))
    logger.info('Reading image from ' + config.get('image_path'))
    logger.info('Image shape: ' + str(image.info))

    # convert image to YCbCr
    ycbcr = converter.convert(image, mode='YCbCr')
    logger.info('Converting image to YCbCr')
    logger.info(f'Image shape: {ycbcr.shape}')
    file_manager.show_image(ycbcr, 'YCbCr image converted from RGB')

    # sample the image
    y, cb, cr = ycbcr[:, :, 0], ycbcr[:, :, 1], ycbcr[:, :, 2]
    totalNumberOfBitsWithoutCompression = calculateTotalNumberOfBitsWithoutCompression(y, cb, cr)
    logger.debug('subsampling image')
    y, cb, cr = sampler.sample(ycbcr, config.get('chroma_subsampling'))
    logger.debug('y shape: {}'.format(y.shape))

    # quantize the image
    logger.debug('quantifying image')
    y, cb, cr = quantifier.quantize([y, cb, cr])
    logger.debug('y shape: {}'.format(y.shape))
    logger.debug('cb shape: {}'.format(cb.shape))
    logger.debug('cr shape: {}'.format(cr.shape))




