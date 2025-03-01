from modules.data_canonization.infraestrucuture.consumers import (
    init_consumers as init_data_canonization_consumers,
)

from modules.data_canonization.application.handle_domain_events import (
    init_producers as data_canonization_producers,
)


import modules.data_canonization.infraestrucuture.event_dispatcher  # type: ignore


init_data_canonization_consumers()
data_canonization_producers()
