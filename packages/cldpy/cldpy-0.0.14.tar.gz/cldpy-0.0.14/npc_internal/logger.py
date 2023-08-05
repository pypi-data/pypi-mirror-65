import os

import logging
import logging.config


log_format = '%(asctime)s %(levelname)s %(filename)s:%(lineno)d: %(message)s'

config = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'short': {
            'format': log_format,
            'datefmt': '%Y%m%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'short',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

try:
    from systemd.journal import JournaldLogHandler
    journald_handler = JournaldLogHandler()
    journald_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(journald_handler)
    logger.setLevel(logging.DEBUG)
except ImportError:
    pass
