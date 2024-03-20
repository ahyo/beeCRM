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


class Countries(Base):
    __tablename__ = "countries"
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    iso = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    nicename = Column(String)
    iso3 = Column(String)
    numcode = Column(String)
    phonecode = Column(String)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class CountriesOut(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    # class Config
    #     from_attributes = True
