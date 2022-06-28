import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

info_handler = logging.FileHandler('../logs/info.log')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

file_handler = logging.FileHandler('../logs/errors.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)


logger.addHandler(info_handler)
logger.addHandler(file_handler)
