from logging.config import dictConfig

from app.config import config


def setup_logger():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | %(name)-30s:%(lineno)-4d | %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "formatter": "console",
                    "level": "DEBUG",
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "file",
                    "level": "DEBUG",
                    "filename": "app.log",
                    "maxBytes": 1024 * 1024,
                    "backupCount": 3,
                    "encoding": "utf8",
                },
            },
            "loggers": {
                "app": {
                    "handlers": ["default", "rotating_file"],
                    "level": config.LOG_LEVEL,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["default", "rotating_file"],
                    "level": config.LOG_LEVEL,
                    "propagate": False,
                },
                "sqlalchemy": {
                    "handlers": ["default"],
                    "level": "WARNING",
                    "propagate": False,
                },
            },
        }
    )
