"""
@author axiner
@version v1.0.0
@created 2022/10/20 16:33
@abstract 日志模拟
@description
@history
"""
import logging.config
from pathlib import Path

from config import DEBUG, LOG_DIR

log_dir = Path(LOG_DIR)
log_dir.mkdir(parents=True, exist_ok=True)

if DEBUG:
    log_level = 'DEBUG'
else:
    log_level = 'INFO'


LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s]%(message)s'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_dir.joinpath('info.log').as_posix(),
            'maxBytes': 1024*1024*50,
            'backupCount': 3,
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_dir.joinpath('error.log').as_posix(),
            'maxBytes': 1024*1024*50,
            'backupCount': 5,
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'info', 'error'],  # 生产中把 console 移除
            'level': log_level,
            'propagate': True,
        },
    }
}


def getLogger(name: str = 'MapTileDownloader'):
    """获取日志器"""
    logging.config.dictConfig(LOG_CONFIG)
    return logging.getLogger(name)
