from dataclasses import dataclass, field
import uuid

from seedwork.domain.entities import RootAgregation
from . import value_objects as vo
from .events import DataSourceCreated


@dataclass
class DataSource(RootAgregation):
    infromation: vo.Information = field(default=None)
    type: vo.DataSourceType = field(default=None)
    credentials: vo.Credentials = field(default=None)
    provider_id: uuid.UUID = field(default=None)

    def create_data_source(self, data_source: "DataSource"):
        self.infromation = data_source.infromation
        self.type = data_source.type
        self.credentials = data_source.credentials
        self.provider_id = data_source.provider_id
        self.add_event(
            DataSourceCreated(
                provider_id=self.provider_id,
                data_source_id=self.id,
                created_at=self.created_at,
            )
        )
