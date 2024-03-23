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


class ClientAddress(Base):
    __tablename__ = "client_address"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    ktp_address = Column(String)
    ktp_country_id = Column(Integer, ForeignKey("countries.id"))
    ktp_province_id = Column(Integer, ForeignKey("provinces.id"))
    ktp_district_id = Column(Integer, ForeignKey("districts.id"))
    ktp_regency_id = Column(Integer, ForeignKey("regencies.id"))
    ktp_village_id = Column(BigInteger, ForeignKey("countries.id"))
    ktp_post_code = Column(String)
    address = Column(String)
    country_id = Column(Integer, ForeignKey("countries.id"))
    province_id = Column(Integer, ForeignKey("provinces.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    regency_id = Column(Integer, ForeignKey("regencies.id"))
    village_id = Column(BigInteger, ForeignKey("countries.id"))
    post_code = Column(String)
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class ClientAddressUpdate(BaseModel):
    ktp_address: str
    ktp_country_id: int
    ktp_province_id: int
    ktp_district_id: int
    ktp_regency_id: int
    ktp_village_id: int
    ktp_post_code: str
    address: str
    country_id: int
    province_id: int
    district_id: int
    regency_id: int
    village_id: int
    post_code: str
