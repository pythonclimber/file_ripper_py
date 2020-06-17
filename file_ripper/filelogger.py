import logging
from os import path, mkdir
from logging.handlers import TimedRotatingFileHandler


log_directory = '/Users/asmitty/workspace/python/file_ripper_py/file_ripper/logs'
log_file_name = 'file_ripper_logs.txt'


def create_file_ripper_logger():
    formatter = logging.Formatter(
        '%(asctime)s %(name)-8s %(levelname)-8s %(message)s')

    logger = logging.getLogger()
    logger.addHandler(create_stream_handler(formatter))
    logger.addHandler(create_file_handler(formatter))
    logger.setLevel(logging.INFO)
    return logger


def create_file_handler(formatter):
    if not path.exists(log_directory):
        mkdir(log_directory)
    handler = TimedRotatingFileHandler(path.join(log_directory, log_file_name), encoding='UTF-8')
    handler.setFormatter(formatter)
    return handler


def create_stream_handler(formatter):
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    return handler
