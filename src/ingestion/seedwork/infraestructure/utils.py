import time
import os


def time_millis():
    return int(time.time() * 1000)


def broker_host() -> str:
    return os.getenv("PULSAR_BROKER_URL", default="pulsar://localhost:6650")
