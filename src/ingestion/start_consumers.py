from modules.data_source.infrastructure.consumers import (
    init_consumers as data_source_init_consumers,
)
from modules.data_intake.infrastructure.consumers import (
    init_consumers as data_intake_init_consumers,
)
from modules.data_source.application.handle_domain_events import (
    init_producers as data_source_producers,
)
from modules.data_intake.application.handle_domain_events import (
    init_producers as data_intake_producers,
)

# Ensure dispatch_events are registered for the events
import modules.data_source.infrastructure.event_dispatcher  # type: ignore
import modules.data_intake.infrastructure.event_dispatcher  # type: ignore

data_source_init_consumers()
data_intake_init_consumers()
data_source_producers()
data_intake_producers()
