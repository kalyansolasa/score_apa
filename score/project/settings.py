import logging
from logging.config import dictConfig
from logging.handlers import SysLogHandler
from config.config import Load_Config 
import os

env = os.environ.get("ENV", 'staging')
#conf = Load_Config(env, os.getcwd()).config
app_name = 'score_app'
app_path = '/var/www/score/project'
from logging.config import dictConfig
log_conf = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
            },
        'file': {
            'filename': '/tmp/test.log',
            'class': 'logging.handlers.WatchedFileHandler',
            'formatter': 'default',
            }
        },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'ERROR'
            },
        'score':{
            'handlers': ['console', 'file'],
            'level': 'INFO',
             'propagate': False,
                }
            }
        }


dictConfig(log_conf)

logger = logging.getLogger('score.%s' % __name__)
logger.info('hurry')


