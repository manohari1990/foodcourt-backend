from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Time, ForeignKey, Numeric, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from constants import PaymentStatus, OrderStatus

class Order(Base):
    __tablename__= "orders"
    
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_number = Column(Integer, nullable=False)
    stall_id = Column(UUID(as_uuid=True), ForeignKey("stalls.id"), nullable=False, index=True)
    order_status= Column(Enum(OrderStatus), nullable=False)
    estimated_time = Column(Integer)
    total_payment = Column(Numeric(10,2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at=Column(DateTime, onupdate=func.now())
    
    stall = relationship('Stall', back_populates='order_ref')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    