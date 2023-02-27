import functools
import logging
import sys
import imgtrf
import rich
from rich.logging import RichHandler

root_logger = logging.getLogger(imgtrf.__name__)
console = rich.console.Console()
rich_handler = RichHandler(console=console)


def configure_logger(log=root_logger):
    """Configure logger for cli purpose"""
    log.addHandler(rich_handler)

    # Default verbosity
    log.setLevel(logging.CRITICAL)


def set_verbosity(verbose: bool = False, debug: bool = False, log=root_logger) -> None:
    """Set verbosity of logger"""
    if verbose:
        log.setLevel(logging.INFO)

    if debug:
        log.setLevel(logging.DEBUG)


def log_func(log=root_logger):
    def wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            log.debug(f"{func.__name__} called with: args {args}, kwargs {kwargs}")
            # print(f"{func.__name__} called with args {args} and kwargs {kwargs}")
            try:
                value = func(*args, **kwargs)
                log.debug(f"{func.__name__} returned: {value!r}")
            except:
                log.debug(
                    f"{func.__name__} rasied exception: \n{str(sys.exc_info()[1])}"
                )
                raise

            return value

        return decorator

    return wrapper
