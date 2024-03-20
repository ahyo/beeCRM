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


class Regencies(Base):
    __tablename__ = "regencies"
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    name = Column(String, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class RegenciesOut(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    # class Config
    #     from_attributes = True
