from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from config.db import Base


class Register(Base):
    __tablename__ = "register"
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
    verified = Column(Boolean, nullable=False, server_default="False")
    verification_code = Column(String, nullable=True, unique=True)
    verification_date = Column(DateTime(timezone=True))
    reff_code = Column(String)
    reff_source = Column(String)
    otp_code = Column(String)
    otp_verified = Column(Boolean, nullable=False, server_default="False")
    otp_date = Column(DateTime(timezone=True))
    # wp_id = Column(UUID, ForeignKey("wp.id")) saat ini semua sales wajib WP
    sales_id = Column(UUID, ForeignKey("sales.id"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)


class RegisterBase(BaseModel):
    fullname: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str = Field(..., min_length=8)
    reff_code: str | None = None
    reff_source: str | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "fullname": "Ahyo Client",
                    "email": "client@testing.com",
                    "password": "rahasia",
                    "phone": "6281807003289",
                    "reff_code": "",
                    "reff_source": "",
                }
            ]
        }
    }


class RegisterDisplay(BaseModel):
    fullname: str
    email: str
    phone: str

    class Config:
        from_attributes = True


class RegisterVerified(BaseModel):
    email: str
    code: str
