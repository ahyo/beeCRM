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


class ClientBank(Base):
    __tablename__ = "client_bank"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    name = Column(String)
    type = Column(String)
    rate = Column(String)
    account = Column(String)
    account_name = Column(String)
    branch = Column(String)
    phone = Column(String)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ClientBankUpdate(BaseModel):
    name: str
    type: str
    rate: str
    account: str
    account_name: str
    branch: str
    phone: str
