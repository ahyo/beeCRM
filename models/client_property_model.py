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
from pydantic import BaseModel
from config.db import Base
from enum import Enum


class ClientProperty(Base):
    __tablename__ = "client_property"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    location = Column(String)
    njop = Column(Integer)
    deposit = Column(Integer)
    amount = Column(Integer)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ClientPropertyUpdate(BaseModel):
    location: str
    njop: int
    deposit: int
    amount: int
