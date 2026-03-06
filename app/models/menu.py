from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class Menu(Base):
    __tablename__= 'menu'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stall_id = Column(UUID(as_uuid=True), ForeignKey("stalls.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    item_image = Column(String)
    serving_quantity = Column(Numeric(10,2))
    serving_quantity_units = Column(String)
    is_available = Column(Boolean, default=True)
    description = Column(String)
    discount = Column(Integer)
    is_deleted= Column(Boolean, default=False)
    created_at= Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    stall = relationship("Stall", back_populates="menu_items")
                                    # relationship(Model name, Object name which is defined in Stall Model)
    order_items = relationship("OrderItem", back_populates="menu_item")
