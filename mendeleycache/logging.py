__author__ = 'kohn'

import logging
import sys

import sqlparse

def create_logger():
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger('mendeleycache')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

log = create_logger()
