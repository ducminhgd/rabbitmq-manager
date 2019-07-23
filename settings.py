import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True, verbose=True)

AMQP_URL = os.environ.get('AMQP_URL', None)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(process)d | %(thread)d | %(filename)s:%(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'main': {
            'level': 'INFO',
            'handlers': os.environ.get('LOGGER_MAIN_HANDLERS', 'console').split(','),
            'propagate': True,
        },
    },
}