from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional, Generator
from uuid import UUID
from pydantic import BaseModel
from models import Warehouse
from db.session import getSession

router = APIRouter(prefix="/warehouses", tags=["warehouses"])

class WarehouseCreate(BaseModel):
    name: str
    location: str

class WarehouseUpdate(BaseModel):
    name: str
    location: str

class WarehousePatch(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class WarehouseResponse(BaseModel):
    id: str
    name: str
    location: str

class WarehouseCreateResponse(BaseModel):
    message: str
    id: str

class MessageResponse(BaseModel):
    message: str

def get_db() -> Generator[Session, None, None]:
    session = getSession()
    try:
        yield session
    finally:
        session.close()

@router.post("/", response_model=WarehouseCreateResponse)
async def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_db)):
    db_warehouse = Warehouse(
        name=warehouse.name,
        location=warehouse.location
    )
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    
    return WarehouseCreateResponse(
        message="Warehouse created successfully",
        id=str(db_warehouse.id)
    )

@router.get("/", response_model=List[WarehouseResponse])
async def get_warehouses(db: Session = Depends(get_db)):
    warehouses = db.query(Warehouse).all()
    return [
        WarehouseResponse(
            id=str(warehouse.id),
            name=str(warehouse.name),
            location=str(warehouse.location)
        )
        for warehouse in warehouses
    ]

@router.get("/{warehouse_id}", response_model=WarehouseResponse)
async def get_warehouse(warehouse_id: str, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid warehouse ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    return WarehouseResponse(
        id=str(warehouse.id),
        name=str(warehouse.name),
        location=str(warehouse.location)
    )

@router.patch("/{warehouse_id}", response_model=MessageResponse)
async def patch_warehouse(warehouse_id: str, warehouse_update: WarehousePatch, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid warehouse ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    update_data = warehouse_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(warehouse, field, value)
    
    db.commit()
    
    return MessageResponse(message="Warehouse updated successfully")

@router.put("/{warehouse_id}", response_model=MessageResponse)
async def update_warehouse(warehouse_id: str, warehouse_update: WarehouseUpdate, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid warehouse ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    update_data = warehouse_update.dict()
    for field, value in update_data.items():
        setattr(warehouse, field, value)
    
    db.commit()
    
    return MessageResponse(message="Warehouse updated successfully")
