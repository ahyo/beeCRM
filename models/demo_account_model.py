from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


from config.db import Base


class DemoAccount(Base):
    __tablename__ = "demo_account"
    account = Column(String, primary_key=True, index=True)
    server = Column(String)
    password = Column(String)
    password_investor = Column(String)
    # account = Column(String)
    client_id = Column(UUID, ForeignKey("client.id"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
