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


class ClientPersonal(Base):
    __tablename__ = "client_personal"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    home_phone = Column(String)
    home_status = Column(String)
    mother_name = Column(String)
    marital_status = Column(String)
    spouse_name = Column(String)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ClientPersonalUpdate(BaseModel):
    home_phone: str
    home_status: str
    mother_name: str
    marital_status: str
    spouse_name: str
