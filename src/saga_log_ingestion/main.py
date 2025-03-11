from base_consumer import start_threads_for_all_consumers
from consumers import CONSUMERS


def init_consumption():
    start_threads_for_all_consumers(CONSUMERS)


if __name__ == "__main__":
    init_consumption()
