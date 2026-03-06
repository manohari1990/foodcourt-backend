from sqlalchemy import Column, Integer, String, Time, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Stall(Base):
    __tablename__ = 'stalls'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stall_name = Column(String, nullable = False)
    stall_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    display_order = Column(Integer, nullable=False)
    stall_image = Column(String)
    contact_name = Column(String)
    stall_area = Column(String)
    open_at = Column(Time)
    close_at = Column(Time)
    stall_number = Column(String, unique=True, nullable=False)
    discount = Column(Integer)
    is_deleted= Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    order_ref = relationship('Order', back_populates='stall')
    menu_items = relationship("Menu", back_populates="stall", cascade="all, delete-orphan")

    