import logging.handlers

LOG_FILE_SETTINGS = {
    'filename': 'log.txt',
    'maxBytes': 8192,
    'backupCount': 8,
}


def init_logger():
    # we use the logger to print to the console
    # Debug    - verbose variable manipulation
    # Info     - long descriptions
    # Warning  - ?
    # Error    - short descriptions
    # Critical - ?

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.handlers.RotatingFileHandler(**LOG_FILE_SETTINGS)
    fh.setLevel(logging.DEBUG)
    fh.doRollover()

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # TODO: config console log level (maybe WARN for release?)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s |%(levelname)8s | %(message)s', datefmt='%Y/%m/%d %a %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # logging.debug('fdsa')
    logging.info('Logging Started')
    # logging.warning('asdf')
    # logging.error('qwer')
    # logging.critical('rewq')
