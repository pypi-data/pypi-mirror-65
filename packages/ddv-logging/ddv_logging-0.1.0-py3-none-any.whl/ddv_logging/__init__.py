__version__ = "0.1.0"

"""
    Convenience methods for logging
"""
import sys
import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the
# foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    "WARNING": YELLOW,
    "INFO": WHITE,
    "DEBUG": BLUE,
    "CRITICAL": YELLOW,
    "ERROR": RED,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = (
                COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            )
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def log_to_stdout(debug_enabled):
    root = logging.getLogger()

    formatter = ColoredFormatter
    if sys.platform == "win32":
        formatter = logging.Formatter

    handler = logging.StreamHandler(sys.stdout)
    if debug_enabled:
        root.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        formatter = formatter("%(name)s\t%(levelname)s\t%(message)s")
    else:
        root.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
        formatter = formatter("%(levelname)s\t%(message)s")

    handler.setFormatter(formatter)
    root.addHandler(handler)
