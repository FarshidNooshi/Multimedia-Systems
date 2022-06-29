import os.path

from utils.file_business import FileBusiness
from utils.converter_business import ConverterBusiness
from utils.log_business import MyLogger

config = FileBusiness.read_config(os.getcwd())
logger = MyLogger('assignment3.main')
logger.info('Starting program')
os.chdir('../')
logger.info('Changing directory to ' + os.getcwd())
image = FileBusiness.read_image(config.get('image_path'))
logger.info('Reading image from ' + config.get('image_path'))
logger.info('Image shape: ' + str(image.info))
ycbcr = ConverterBusiness().convert(image, mode='YCbCr')
logger.info('Converting image to YCbCr')
logger.info(f'Image shape: {ycbcr.shape}')
