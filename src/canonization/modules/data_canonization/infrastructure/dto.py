from typing import List

from sqlalchemy import Column, UUID, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from config.db import Base


class DataCanonization(Base):
    __tablename__ = "data_canonizations"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    provider_id = Column(UUID(as_uuid=True), index=True)
    ingestion_id = Column(UUID(as_uuid=True), index=True)
    anonimization_id = Column(UUID(as_uuid=True), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(String)
    total_records = Column(String, index=True)
    repository_in_path = Column(String)
    steps = relationship("DataCanonizationStep", back_populates="data_canonization")


class DataCanonizationStep(Base):
    __tablename__ = "data_canonization_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    ai_model_id = Column(UUID(as_uuid=True), index=True)
    data_canonization_id = Column(
        UUID(as_uuid=True), ForeignKey("data_canonizations.id"), index=True
    )
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    total_records = Column(String, index=True)
    data_canonization = relationship("DataCanonization", back_populates="steps")
