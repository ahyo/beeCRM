from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime,
    String,
    BigInteger,
    ForeignKey,
    Boolean,
    Date,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from config.db import Base
from enum import Enum


class ClientJob(Base):
    __tablename__ = "client_job"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    annual_revenue = Column(String)
    company_name = Column(String)
    field = Column(String)
    position = Column(String)
    working_year = Column(Integer)
    prev_working_year = Column(Integer)
    address = Column(String)
    post_code = Column(String)
    phone = Column(String)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ClientJobUpdate(BaseModel):
    annual_revenue: str
    company_name: str
    field: str
    position: str
    working_year: int
    prev_working_year: int
    address: str
    post_code: str = Field(..., min_length=5)
    phone: str
