from enum import Enum

class PaymentStatus(str,Enum): 
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    
class OrderStatus(str, Enum):
    PLACED = 'PLACED'
    PREPARING= 'PREPARING',
    READY = "READY"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    
class UserRole(str, Enum):
    USER = 'USER',
    ADMIN = 'ADMIN',
    MANAGER = 'MANAGER'