from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean, Double
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


from config.db import Base


class LiveSummary(Base):
    __tablename__ = "live_summary"
    id = Column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
    name = Column(String)
    value = Column(String)
    account = Column(String, ForeignKey("live_account.account"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
