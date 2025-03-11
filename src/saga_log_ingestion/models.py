import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, UUID, String, DateTime, Float
from sqlalchemy.sql import func

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Define the SagaLog model
class SagaLog(Base):
    __tablename__ = "saga_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    correlation_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    component = Column(String, nullable=False)
    action_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    entity_id = Column(String(), nullable=True)
    event_at = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
