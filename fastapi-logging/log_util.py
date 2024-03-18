import logging
import contextvars

request_id_context = contextvars.ContextVar("request_id", default="")  # default: empty string


logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ],
    format='%(asctime)s.%(msecs)03d-%(levelname)s:%(name)s:%(module)s:%(funcName)s:%(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("SERVER")


def logger_info(message):
    if type(message) is str:
        message = dict(request_id=request_id_context.get(), message=message)
    elif type(message) is dict:
        message = message.update({"request_id": request_id_context.get()})
    logger.info(message)

