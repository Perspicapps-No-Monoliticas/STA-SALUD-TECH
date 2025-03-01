# Listen to local event and publish to pulsar
from pydispatch import dispatcher

from modules.data_intake.domain.events import (
    DataintakeCreated,
    DataIntakeStarted,
    DataIntakeFinished,
)
from seedwork.infraestructure.dispatcher import dispatch_event
from seedwork.domain.events import DomainEvent


def _dispatch_event(event: DomainEvent):
    dispatch_event(event)


def init_producers():
    for event in [DataintakeCreated, DataIntakeStarted, DataIntakeFinished]:
        dispatcher.connect(
            _dispatch_event,
            signal=f"{event.__name__}Integration",
        )
