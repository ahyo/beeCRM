from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime




from config.db import Base


class Wp(Base):
    __tablename__ = "wp"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    wp_code = Column(String)
    sales_id = Column(UUID, ForeignKey("sales.id"))
    time_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
