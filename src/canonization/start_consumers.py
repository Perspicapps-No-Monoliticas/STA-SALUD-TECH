from modules.data_canonization.infrastructure.consumers import (
    init_consumers as init_data_canonization_consumers,
)

from modules.data_canonization.application.handle_domain_events import (
    init_producers as data_canonization_producers,
)


init_data_canonization_consumers()
data_canonization_producers()
