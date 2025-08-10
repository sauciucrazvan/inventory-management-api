import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes import warehouses, suppliers, stock_management, product_management

app = FastAPI(title="Inventory Management API", version="1.0.0")

def runApp():

    api_router = APIRouter(prefix="/api")

    api_router.include_router(warehouses.router)
    api_router.include_router(suppliers.router)
    api_router.include_router(stock_management.router)
    api_router.include_router(product_management.router)


    app.include_router(api_router)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="127.0.0.1", port=8000)

def getApp():
    global app
    return app