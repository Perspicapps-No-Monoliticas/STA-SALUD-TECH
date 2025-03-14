import time
import os
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)


def time_millis():
    return int(time.time() * 1000)


def broker_host():
    return os.getenv("BROKER_HOST", default="localhost")

def country_code():
    return os.getenv('COUNTRY_CODE', default="US")

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0
