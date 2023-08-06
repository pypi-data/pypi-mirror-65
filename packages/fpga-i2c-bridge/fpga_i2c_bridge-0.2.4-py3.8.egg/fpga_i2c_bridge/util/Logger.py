import logging


def get_logger(module):
    """

    :param module:
    :return:
    """
    logging.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                        datefmt='%H:%M:%S', level=logging.DEBUG)

    return logging.getLogger(module if isinstance(module, str) else module.__class__.__name__)
