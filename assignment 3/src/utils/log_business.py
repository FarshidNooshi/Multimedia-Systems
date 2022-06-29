import logging

import colorama as colorama
from colorama import Fore


def logging_decorator(name):
    logger_object = logging.getLogger(name)

    def _decor(fn):
        function_name = fn.__name__

        def _fn(*args, **kwargs):
            ret = fn(*args, **kwargs)
            argstr = [str(x) for x in args]
            argstr += [key + "=" + str(val) for key, val in kwargs.items()]
            logger_object.debug("%s(%s) -> %s", function_name, ", ".join(argstr), ret)
            return ret

        return _fn

    return _decor


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        colors = {"DEBUG": Fore.BLUE, "INFO": Fore.GREEN,
                  "WARNING": Fore.YELLOW, "ERROR": Fore.RED, "CRITICAL": Fore.MAGENTA}
        msg = logging.Formatter.format(self, record)
        if record.levelname in colors:
            msg = colors[record.levelname] + msg + Fore.RESET
        return msg


class MyLogger:
    def __init__(self, name):
        colorama.init(autoreset=True)
        self.logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        handler.setFormatter(ColoredFormatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def critical(self, msg):
        self.logger.critical(msg)