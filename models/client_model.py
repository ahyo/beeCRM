from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from pydantic import BaseModel
from config.db import Base
from enum import Enum


class Client(Base):
    __tablename__ = "client"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    email = Column(String, unique=True, index=True)
    password = Column(String)
    fullname = Column(String)
    phone = Column(String)
    register_id = Column(UUID, ForeignKey("register.id"))
    wp_id = Column(UUID, ForeignKey("wp.id"))
    sales_id = Column(UUID, ForeignKey("sales.id"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ClientAuth(BaseModel):
    id: int
    email: str
    fullname: str


class dokumenEnum(str, Enum):
    ktp = "ktp"
    selfie = "selfie"
    npwp_kk = "npwp_kk"
