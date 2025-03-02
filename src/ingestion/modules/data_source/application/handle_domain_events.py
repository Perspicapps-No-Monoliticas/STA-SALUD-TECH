import sys

# Listen to local event and publish to pulsar
from pydispatch import dispatcher

from modules.data_source.domain.events import DataSourceCreated
from seedwork.infrastructure.dispatcher import dispatch_event
from seedwork.domain.events import DomainEvent


def _dispatch_event(event: DomainEvent):
    dispatch_event(event)


def init_producers():
    dispatcher.connect(
        _dispatch_event,
        signal=f"{DataSourceCreated.__name__}Integration",
    )
