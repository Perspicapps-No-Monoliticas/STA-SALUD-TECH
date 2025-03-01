from sqlalchemy import Column, UUID, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from config.db import Base


class DataIntake(Base):
    __tablename__ = "data_intakes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    provider_id = Column(UUID(as_uuid=True), index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    status = Column(String)
    total_records = Column(String, index=True)
    repository_out_path = Column(String)
    history = relationship("DataIntakeStep", back_populates="data_intake")


class DataIntakeStep(Base):
    __tablename__ = "data_intake_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    data_source_id = Column(
        UUID(as_uuid=True), ForeignKey("data_sources.id"), index=True
    )
    data_intake_id = Column(
        UUID(as_uuid=True), ForeignKey("data_intakes.id"), index=True
    )
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    total_records = Column(String, index=True)
    data_intake = relationship("DataIntake", back_populates="history")
