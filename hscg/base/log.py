import logging
import functools

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s", "%Y%m%d-%H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)


def log(func=None, msg=None):
    if func is None:
        return functools.partial(log, msg=msg)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(func.__name__ + func.__doc__)
        if msg:
            logger.info(msg.format(result))
        return result

    return wrapper
