from base_consumer import start_threads_for_all_consumers
from consumers import CONSUMERS
from models import Base, engine

Base.metadata.create_all(bind=engine)


def init_consumption():
    start_threads_for_all_consumers(CONSUMERS)


if __name__ == "__main__":
    init_consumption()
