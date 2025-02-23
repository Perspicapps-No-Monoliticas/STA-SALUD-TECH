import time

from .varaibles import BROKER_HOST


def time_millis():
    return int(time.time() * 1000)


def broker_host() -> str:
    return BROKER_HOST
