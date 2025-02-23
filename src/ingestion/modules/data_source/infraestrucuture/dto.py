from sqlalchemy import Column, UUID, String, DateTime, JSON

from config.db import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(UUID(as_uuid=True), primary_key=True)
    provider_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String(100), nullable=False)
    credentials = Column(JSON, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<DataSource(name={self.name}, description={self.description})>"
