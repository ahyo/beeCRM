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


class Villages(Base):
    __tablename__ = "villages"
    id = Column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
    name = Column(String, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class VillagesOut(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    # class Config
    #     from_attributes = True
