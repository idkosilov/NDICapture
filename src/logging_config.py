import logging.config

logging_config = dict(
    version=1,
    formatters={
        'formatter': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers={
        'stream_handler': {'class': 'logging.StreamHandler',
                           'formatter': 'formatter',
                           'level': logging.DEBUG},
        'file_handler': {'class': 'logging.FileHandler',
                         'formatter': 'formatter',
                         'filename': 'app.log',
                         'mode': 'w',
                         'level': logging.DEBUG},
    },
    root={
        'handlers': ['stream_handler', 'file_handler'],
        'level': logging.DEBUG,
    },
)

logging.config.dictConfig(logging_config)
