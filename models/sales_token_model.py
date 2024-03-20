from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime




from config.db import Base


class SalesToken(Base):
    __tablename__ = "sales_token"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    token = Column(String,index=True)
    sales_id = Column(UUID, ForeignKey("sales.id"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
