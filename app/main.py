from fastapi import FastAPI
from database import engine
from routers.stalls import router as stalls_router
from routers.menus import router as menus_router
from routers.orders import router as order_router
from routers.UserLogin import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)
###############################
### Remember This Forever ###
# Schemas validate data
# Models talk to database 
###############################


app.include_router(
    user_router,
    prefix="/users",
    tags=["Users"]
)


app.include_router(
    stalls_router,
    prefix="/stalls",
    tags=["Stalls"]
)

app.include_router(
    menus_router,
    prefix="/menu",
    tags=["Menu"]
)

app.include_router(
    order_router,
    prefix="/orders",
    tags=["Orders"]
)


@app.get('/health')
def health_check():
    try:
        with engine.connect() as connection:
            return {
                'status': 'DB Connected'
            }
    except Exception as e:
        return {
            'status': 'Db connection error', 'error':str(e)
        }
