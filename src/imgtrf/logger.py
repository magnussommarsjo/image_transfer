import functools
import logging
import sys
import imgtrf

root_logger = logging.getLogger(imgtrf.__name__)

def log_func(log=root_logger):
    def wrapper(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            log.debug(f"{func.__name__} called with: args {args}, kwargs {kwargs}")
            #print(f"{func.__name__} called with args {args} and kwargs {kwargs}")
            try:
                value = func(*args, **kwargs)
                log.debug(f"{func.__name__} returned: {value!r}")
            except:
                log.debug(f"{func.__name__} rasied exception: \n{str(sys.exc_info()[1])}")
                raise

            return value

        
        return decorator
    return wrapper
