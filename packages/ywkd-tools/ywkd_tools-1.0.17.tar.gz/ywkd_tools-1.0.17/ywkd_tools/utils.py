from uuid import uuid1
from log_request_id import local, NO_REQUEST_ID


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_request_id():
    try:
        request_id = local.request_id
    except AttributeError:
        request_id = NO_REQUEST_ID if NO_REQUEST_ID else uuid1().hex
    return request_id
