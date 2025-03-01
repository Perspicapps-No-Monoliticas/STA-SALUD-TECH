# Listen to local event and publish to pulsar
from pydispatch import dispatcher

from modules.data_canonization.domain.events import DataCanonizationStarted
from seedwork.infraestructure.dispatcher import dispatch_event
from seedwork.domain.events import DomainEvent


# Ensure dispatch_events are registered for the events
import modules.data_canonization.infraestrucuture.event_dispatcher  # type: ignore


def _dispatch_event(event: DomainEvent):
    dispatch_event(event)


def init_producers():
    dispatcher.connect(
        _dispatch_event,
        signal=f"{DataCanonizationStarted.__name__}Integration",
    )
