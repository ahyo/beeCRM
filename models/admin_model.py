from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from config.db import Base
import pyotp


class Admin(Base):
    __tablename__ = "admin"
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
    secret_token = Column(String, unique=True)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class AdminBase(BaseModel):
    fullname: str = Field(..., min_length=8)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: str = Field(..., min_length=8)


class AdminDisplay(BaseModel):
    fullname: str
    email: str
    phone: str

    class Config:
        from_attributes = True


class AdminAuth(BaseModel):
    id: int
    email: str
    fullname: str
