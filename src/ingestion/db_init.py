#  Try to init the database by importing all dtos
import time
from config.db import engine, Base

MAX_TRIES = 3
SLEEP = 1


def init_db():
    # Import all Dtos from the modules infraestrcutures
    import modules.data_source.infrastructure.dto  # type: ignore
    import modules.data_intake.infrastructure.dto  # type: ignore

    Base.metadata.create_all(bind=engine)


for i in range(MAX_TRIES):
    try:
        init_db()
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(SLEEP)
