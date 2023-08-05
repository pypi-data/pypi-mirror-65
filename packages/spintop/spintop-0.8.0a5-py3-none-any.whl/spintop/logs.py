import logging

LEVEL = logging.DEBUG
VERBOSE = (LEVEL == logging.DEBUG)
CORE_LOGGER = logging.getLogger('sptp')
FORMAT = '%(relativeCreated)-10d[ms] %(name)-30s:%(levelname)-5s: %(message)s'

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(logging.Formatter(FORMAT))



def _logger(name):
    return CORE_LOGGER.getChild(name)

def setup_logging():
    logging.basicConfig(format=FORMAT)

    CORE_LOGGER.setLevel(LEVEL)
    # if STREAM_HANDLER not in CORE_LOGGER.handlers:
    #     CORE_LOGGER.addHandler(STREAM_HANDLER)