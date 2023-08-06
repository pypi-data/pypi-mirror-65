import os
import sys
from logging import getLogger, StreamHandler, DEBUG, INFO, WARNING
from pythonjsonlogger import jsonlogger


logger_name = os.getenv('LOGGER_NAME', 'root')
log_levels = os.getenv('LOG_LEVELS', 'root=INFO').split(',')
format_str = os.getenv('LOG_FORMAT', '%(levelname)%(name)%(asctime)%(module)%(funcName)%(lineno)%(message)')
app_logger = getLogger() if logger_name == 'root' else getLogger(logger_name)


def init_logging():
    # create formatter
    formatter = jsonlogger.JsonFormatter(format_str)
    # create stdout handler
    stdout_handler = StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(DEBUG)
    stdout_handler.addFilter(lambda record: record.levelno in {DEBUG, INFO})
    # create stderr handler
    stderr_handler = StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(WARNING)
    # configure logger
    app_logger.addHandler(stdout_handler)
    app_logger.addHandler(stderr_handler)

    for level in log_levels:
        if '=' in level:
            config = level.strip().split('=')
            if config[0] == logger_name:
                app_logger.setLevel(config[1].upper())
            getLogger(config[0]).setLevel(config[1].upper())


init_logging()
