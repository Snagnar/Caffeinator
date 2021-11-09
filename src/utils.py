import logging
from typing import Union
from pathlib import Path

def set_logging(log_file: Union[None, str], log_level: str, output_stdout: bool) -> None:
    """configures logging module.

    Args:
        log_file (str): path to log file. if omitted, logging will be forced to stdout.
        log_level (str): string name of log level (e.g. 'debug')
        output_stdout (bool): toggles stdout output. will be activated automatically if no log file was given.
            otherwise if activated, logging will be outputed both to stdout and log file.
    """
    logger = logging.getLogger()

    log_level_name = log_level.upper()
    log_level = getattr(logging, log_level_name)
    logger.setLevel(log_level)

    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s [%(filename)s : %(funcName)s() : l. %(lineno)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    if log_file:
        log_file_path = Path(log_file)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging_format)
        logger.addHandler(file_handler)
    else:
        output_stdout = True

    if output_stdout:
        stream = logging.StreamHandler()
        stream.setLevel(log_level)
        stream.setFormatter(logging_format)
        logger.addHandler(stream)
