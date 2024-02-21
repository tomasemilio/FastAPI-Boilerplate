from logging.config import dictConfig

from app.config import config


def setup_logger():
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 16,
                    "default_value": " ",
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "[%(correlation_id)s] %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ %(levelname) [%(correlation_id)s] %(name)s:%(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "formatter": "console",
                    "level": "DEBUG",
                    "filters": ["correlation_id"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "file",
                    "level": "DEBUG",
                    "filename": "app.log",
                    "maxBytes": 1024 * 1024,
                    "backupCount": 3,
                    "encoding": "utf8",
                    "filters": ["correlation_id"],
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
                "sqlalchemy.engine.Engine": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )
