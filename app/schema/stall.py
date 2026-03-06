from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import time, datetime
from schema.common import PaginationMeta

class StallCreate(BaseModel):
    stall_name: str
    stall_type: str
    status: str
    display_order: int
    stall_number: str
    open_at: time
    close_at: time
    is_deleted: Optional[bool] = False
    stall_image: Optional[str] = None
    contact_name: Optional[str] = None
    stall_area: Optional[str] = None
    discount: Optional[int] = None


class StallResponse(StallCreate):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)
        
class ListStallResponse(BaseModel):
    status_code: int
    message: str
    data: List[StallResponse]
    pagination: PaginationMeta
    
class UpsertStallResponse(BaseModel):
    status_code: int
    message: str
    data: StallResponse
    
class UpdateStall(BaseModel):
    stall_name: Optional[str] = None
    stall_type: Optional[str] = None
    status: Optional[str] = None
    display_order: Optional[int] = None
    stall_number: Optional[str] = None
    open_at: Optional[time] = None
    close_at: Optional[time] = None
    stall_image: Optional[str] = None
    contact_name: Optional[str] = None
    stall_area: Optional[str] = None
    discount: Optional[int] = None
    is_deleted: Optional[bool] = None