import logging.handlers


# we use the logger to print to the console
# Debug    - verbose variable manipulation
# Info     - long descriptions
# Warning  - statuses
# Error    - short descriptions
# Critical - ?
def init_logger(console_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.handlers.RotatingFileHandler(
        filename='log.txt',
        maxBytes=8192,
        backupCount=8,
    )
    fh.setLevel(logging.DEBUG)
    fh.doRollover()

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(console_level)

    # # create formatter and add it to the handlers
    # formatter = logging.Formatter('%(asctime)s |%(levelname)8s | %(message)s', datefmt='%Y/%m/%d %a %H:%M:%S')
    # fh.setFormatter(formatter)
    # ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logging.debug('Logging Started')


def main():
    init_logger(logging.DEBUG)
