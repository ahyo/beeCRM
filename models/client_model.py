from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean, Date
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
    sales_id = Column(UUID, ForeignKey("sales.id"))
    no_ktp = Column(String)
    birth_place = Column(String)
    birth_date = Column(Date)
    gender = Column(String)
    job = Column(String)
    no_npwp = Column(String)
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


class ClientUpdate(BaseModel):
    fullname: str
    phone: str
    no_ktp: str
    birth_place: str
    birth_date: datetime
    gender: str
    job: str
    no_npwp: str
