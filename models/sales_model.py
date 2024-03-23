from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from config.db import Base


class Sales(Base):
    __tablename__ = "sales"
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
    code = Column(String, unique=True, index=True)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class SalesBase(BaseModel):
    fullname: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str = Field(..., min_length=8)
    code: str = Field(..., min_length=3)


class SalesDisplay(BaseModel):
    fullname: str
    email: str
    phone: str

    class Config:
        from_attributes = True
