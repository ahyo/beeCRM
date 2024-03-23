from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean, Double
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


from config.db import Base


class LiveAccount(Base):
    __tablename__ = "live_account"
    account = Column(String, primary_key=True, index=True)
    password = Column(String)
    password_investor = Column(String)
    server = Column(String)
    commission = Column(Double)
    client_id = Column(UUID, ForeignKey("client.id"))
    # detail account
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
