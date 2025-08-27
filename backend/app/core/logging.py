import logging.config
from app.core.config import settings

log_level = logging.DEBUG if settings.ENVIRONMENT == "local" else logging.INFO

# Initial config from https://stackoverflow.com/questions/7507825
LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': log_level,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': { 
        'httpcore': {'level': 'WARNING', 'handlers': ['default'], 'propagate': False},
        'httpx': {'level': 'WARNING', 'handlers': ['default'], 'propagate': False},
        '': {  # root logger
            'handlers': ['default'],
            'level': log_level,
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    } 
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)
logger.debug("Logging is configured.")