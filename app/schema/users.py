from pydantic import BaseModel, ConfigDict
from constants import UserRole
from uuid import UUID
from datetime import datetime

class UsersBase(BaseModel):
    email: str
    password_hash: str
    user_role: UserRole
    
class UserCreate(UsersBase):
    pass

class UserResponse(UsersBase):
    id:UUID
    created_at: datetime
    updated_t: datetime
    
    model_config=ConfigDict(from_attributes=True)