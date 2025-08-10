import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routes import warehouses

app = FastAPI(title="Inventory Management API", version="1.0.0")

def runApp():

    api_router = APIRouter(prefix="/api")

    api_router.include_router(warehouses.router)

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