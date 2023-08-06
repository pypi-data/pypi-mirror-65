import logging

import colorama
from colorama import Fore, Back, Style



class Logger:
    SEVERITY_COLORS = {
        "debug": Fore.CYAN,
        "info": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "critical": Back.RED
    }

    def __init__(self, logger, quiet=False):
        colorama.init()
        self.logger = logger
        self.is_quiet = quiet

    def __getattr__(self, attr_name):
        if attr_name == 'warn':
            attr_name = 'warning'

        if attr_name not in "debug info warn error critical":
            return getattr(self.logger, attr_name)

        log_level = getattr(logging, attr_name.upper())

        if self.is_quiet or not self.logger.isEnabledFor(log_level):
            return

        def wrapped_attr(msg, *args, **kwargs):
            color = self.SEVERITY_COLORS[attr_name]
            msg = color + msg + Style.RESET_ALL

            return self.logger._log(log_level, msg, args, **kwargs)
        return wrapped_attr
