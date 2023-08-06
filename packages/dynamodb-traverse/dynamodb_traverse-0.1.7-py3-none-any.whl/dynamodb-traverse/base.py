import logging
import re
import sys
from os.path import expanduser
from datetime import datetime


class Base(object):
    def __init__(self, **kwargs):
        self._setup_logging(**kwargs)

    def _setup_logging(self, log_to_screen=False, silence=True, **kwargs):
        self.silence = silence
        if not silence:
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            # log setup
            # article = re.sub(r'(?is)</html>.+', '</html>', article)
            suffix = str(datetime.utcnow()).strip()
            suffix = re.sub(r"[:.\s]+", "", suffix)
            log_location = kwargs.pop(
                "log_path", "".join(("/tmp/", "dynamodb_traverse_", suffix, ".log"))
            )
            logger_name = kwargs.pop("name", "base_logger")
            formatter = logging.Formatter(
                fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler = logging.FileHandler(log_location, mode="w")
            handler.setFormatter(formatter)

            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.ERROR)
            logger.addHandler(handler)
            if log_to_screen:
                screen_handler = logging.StreamHandler(stream=sys.stderr)
                screen_handler.setFormatter(formatter)
                logger.addHandler(screen_handler)

            # logging.basicConfig(filename=log_location, level=logging.INFO)
            self.logger = logger

    def info(self, msg):
        if not self.silence:
            self.logger.info(msg)

    def error(self, msg):
        if not self.silence:
            self.logger.error(msg)
