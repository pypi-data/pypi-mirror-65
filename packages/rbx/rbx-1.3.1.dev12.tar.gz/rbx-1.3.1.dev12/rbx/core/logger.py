import logging
import logging.config
import os

import click


def init(format='[%(asctime)s] [%(levelname)s] %(message)s'):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': format
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            '': {
                'level': os.getenv('LOG_LEVEL', 'ERROR'),
                'handlers': ['console'],
            },
            'rbx': {
                'level': os.getenv('LOG_LEVEL', 'ERROR'),
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    logging.config.dictConfig(LOGGING)
    logging.getLogger('urllib3').propagate = False
    logging.getLogger('google').propagate = False


class Logger:
    """Implements the default logging methods."""
    def __init__(self, format='[%(asctime)s] [%(levelname)s] %(message)s', logger=None):
        if not logger:
            logger = logging

        self.format = format
        self.logger = logger
        self.setup_logging()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.__class__.__name__)

    def __getattr__(self, name):
        """Delegate the basic logging methods to the logger."""
        if name in ('debug', 'info', 'warning', 'error', 'critical', 'exception'):
            return getattr(self.logger, name)

        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {name!r}')

    def setup_logging(self):
        init(format=self.format)

    def done(self):
        pass

    def log(self, message):
        self.logger.debug(message)

    def progress(self):
        pass


class ConsoleLogger(Logger):
    """Logs to the console with colours."""

    def info(self, message, *args, **kwargs):
        self.logger.info(click.style(str(message), bold=True), *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(click.style(str(message), fg='yellow'), *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(click.style(str(message), fg='bright_red'), *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.logger.exception(click.style(str(message), fg='bright_red'), *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(
            click.style(str(message), fg='bright_white', bg='red'), *args, **kwargs)

    def log(self, message):
        """Print to screen without a new line."""
        click.echo(message, nl=False)

    def progress(self):
        """Print a '.' to screens without a new line."""
        click.echo('.', nl=False)

    def done(self):
        """Print 'done' followed by a new line."""
        click.secho(' done', fg='green')
