from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base


class Users(Base):
    __tablename__ = 'users'
    
    id=Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4())
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    user_role = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, onupdate=func.now())
    