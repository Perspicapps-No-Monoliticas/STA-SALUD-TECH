# Listen to local event and publish to pulsar
from pydispatch import dispatcher

from modules.data_source.domain.events import DataSourceCreated

from .handlers import DataSourceEventsHandler


def init_producers():
    dispatcher.connect(
        DataSourceEventsHandler.handle_data_source_created,
        signal=f"{DataSourceCreated.__name__}Integration",
    )
