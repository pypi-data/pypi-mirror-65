import logging

_LOGGER = None


def get_logger() -> logging.Logger:
    global _LOGGER
    if not _LOGGER:
        logging.info('cache_gs logging init')
        _LOGGER = logging.getLogger('cache_gs')

    return _LOGGER
