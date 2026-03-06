from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

class OrderItem(Base):
    
    __tablename__ = 'order_items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), index=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("menu.id"), index=True)
    quantity = Column(Integer, nullable=False)
    price_at_order_time = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    order = relationship("Order", back_populates="items")
    menu_item = relationship("Menu", back_populates="order_items")
