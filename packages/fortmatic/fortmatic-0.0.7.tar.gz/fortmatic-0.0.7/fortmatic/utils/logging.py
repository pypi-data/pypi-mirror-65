import logging
import sys

import fortmatic
from fortmatic.config import LOGGER_NAME


logger = logging.getLogger(LOGGER_NAME)


def _fortmatic_log_level():
    if fortmatic.log == 'debug':
        return fortmatic.log


def format_log(message, **kwargs):
    return dict(
        {'message': message},
        log_level=fortmatic.log,
        serverice=LOGGER_NAME,
        **kwargs,
    )


def log_debug(message, **kwargs):
    log_line = format_log(message, **kwargs)

    if _fortmatic_log_level() == 'debug':
        print(log_line, file=sys.stderr)

    logger.debug(log_line)


def log_info(message, **kwargs):
    log_line = format_log(message, **kwargs)

    if _fortmatic_log_level() == 'debug':
        print(log_line, file=sys.stderr)

    logger.info(log_line)
