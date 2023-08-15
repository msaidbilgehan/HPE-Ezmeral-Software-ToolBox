
import logging
import sys



logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)