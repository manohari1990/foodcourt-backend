from jose import JWTError, jwt
from database import get_db
from fastapi import Depends, HTTPException, APIRouter, Form
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import bcrypt
from models import Users
from schema.users import UserCreate
from fastapi.responses import JSONResponse

SECRETE_KEY = ""
ALGORITHM= "HS256"
router = APIRouter()

def create_access_token(user_details:dict):
    user_details['exp']= datetime.utcnow() + timedelta(minutes=60)
    return jwt.encode(user_details, SECRETE_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=ALGORITHM)
        user_role = payload['user_role']
        user_role = payload['user_role']
        return user_role, user_role
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))

def get_password_hash(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

def log_error(message, error=None):
    if error is None:
        error = []
    error.append(message)
    print(error)
    return error


@router.post('/')
def register(
    user_details: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        new_user = Users(
            email = user_details.email,
            password_hash = get_password_hash(user_details.password_hash),
            user_role= user_details.user_role
        )
                
        db.add(new_user)
        db.commit()
        return {
            'status_code': 201,
            'message': 'User created successfully!'
        }
        
    except Exception as e:
        db.rollback()
        log_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/login')
def login(
    email:str = Form(...),
    password:str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(Users).filter(Users.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User email Id not found")
        print(user)

        if bcrypt.checkpw(password.encode("utf-8"), (user.password_hash).encode("utf-8")):
            access_token = create_access_token({'user_role': user.user_role, 'email': user.email})
            
            response = JSONResponse({
                'status_code': 200,
                'message': 'Logged in successfully',
                'data': {
                        'id': str(user.id),
                        'email':user.email,
                        'user_role': user.user_role,
                        'create_at': str(user.created_at)
                    }
            })
            
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="strict"
            )
            return response
            
        else:
            log_error('Wrong Credentials! Please try again')
            return {
                'status_code': 401,
                'message': 'Wrong Credentials! Please try again.',
            } 
    except Exception as e:
        log_error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
            
