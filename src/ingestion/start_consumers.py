from modules.data_source.infraestrucuture.consumers import (
    init_consumers as data_source_init_consumers,
)
from modules.data_source.application.handle_domain_events import (
    init_producers as data_source_producers,
)

# Ensure dispatch_events are registered for the events
import modules.data_source.infraestrucuture.event_dispatcher  # type: ignore

data_source_init_consumers()
data_source_producers()
