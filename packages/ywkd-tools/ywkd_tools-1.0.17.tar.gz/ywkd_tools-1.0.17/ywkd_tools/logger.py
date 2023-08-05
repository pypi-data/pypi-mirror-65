import logging
import log_request_id

logger = logging.getLogger('ywkd_tools')
logger.setLevel(logging.INFO)

hd = logging.StreamHandler()
fm = logging.Formatter('{"asctime": "%(asctime)s", "levelname": "%(levelname)s", "location": "%(module)s.%(funcName)s", "path":"%(pathname)s:%(lineno)s", "request_id": "%(request_id)s", "message": "%(message)s"}')
hd.setFormatter(fm)
hd.addFilter(log_request_id.filters.RequestIDFilter())
logger.addHandler(hd)
