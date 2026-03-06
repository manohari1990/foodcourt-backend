from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from schema.common import PaginationMeta

class MenuCreate(BaseModel):
    stall_id: UUID
    name: str
    price: Decimal
    item_image: Optional[str] = None
    serving_quantity: Optional[Decimal] = None
    serving_quantity_units: Optional[str] = None
    is_available: Optional[bool] = True
    description: Optional[str] = None
    discount: Optional[int] = None
    is_deleted: Optional[bool] = False


class MenuUpdate(BaseModel):    
    name: Optional[str] = None
    price: Optional[Decimal] = None
    item_image: Optional[str] = None
    serving_quantity: Optional[Decimal] = None
    serving_quantity_units: Optional[str] = None
    is_available: Optional[bool] = None
    description: Optional[str] = None
    discount: Optional[int] = None
    is_deleted: Optional[bool] = None
    
    
class MenuResponse(MenuCreate):
    id: UUID
    created_at: datetime
    updated_at:Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)
    
    
class MenuListResponse(BaseModel):
    status_code: int
    message: str
    data: List[MenuResponse]
    pagination: PaginationMeta

class MenuUpsertResponse(BaseModel):
    status_code: int
    message: str
    data: MenuResponse