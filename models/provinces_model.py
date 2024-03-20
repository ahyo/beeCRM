from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime,
    String,
    BigInteger,
    ForeignKey,
    Boolean,
    Integer,
)
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from config.db import Base
from typing import Optional


class Provices(Base):
    __tablename__ = "provinces"
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    name = Column(String, unique=True, index=True)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ProvicesOut(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    # class Config
    #     from_attributes = True
