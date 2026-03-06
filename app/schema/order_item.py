from pydantic import BaseModel 
from uuid import UUID
from decimal import Decimal


class OrderItemBase(BaseModel):
    
    # order_id: UUID
    item_id: UUID
    quantity: int
    price_at_order_time: Decimal
    

class OrderItemCreate(OrderItemBase):
    pass