from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional, Generator
from uuid import UUID
from pydantic import BaseModel
from models import Supplier
from db.session import getSession

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

class SupplierCreate(BaseModel):
    name: str
    contact_email: str

class SupplierUpdate(BaseModel):
    name: str
    contact_email: str

class SupplierPatch(BaseModel):
    name: Optional[str] = None
    contact_email: Optional[str] = None

class SupplierResponse(BaseModel):
    id: str
    name: str
    contact_email: str

class SupplierCreateResponse(BaseModel):
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

@router.post("/", response_model=SupplierCreateResponse)
async def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(
        name=supplier.name,
        contact_email=supplier.contact_email
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    
    return SupplierCreateResponse(
        message="Supplier created successfully",
        id=str(db_supplier.id)
    )

@router.get("/", response_model=List[SupplierResponse])
async def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    return [
        SupplierResponse(
            id=str(supplier.id),
            name=str(supplier.name),
            contact_email=str(supplier.contact_email)
        )
        for supplier in suppliers
    ]

@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: str, db: Session = Depends(get_db)):
    try:
        supplier_uuid = UUID(supplier_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplier ID format")
    
    supplier = db.query(Supplier).filter(Supplier.id == supplier_uuid).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    return SupplierResponse(
        id=str(supplier.id),
        name=str(supplier.name),
        contact_email=str(supplier.contact_email)
    )

@router.patch("/{supplier_id}", response_model=MessageResponse)
async def patch_supplier(supplier_id: str, supplier_update: SupplierPatch, db: Session = Depends(get_db)):
    try:
        supplier_uuid = UUID(supplier_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplier ID format")
    
    supplier = db.query(Supplier).filter(Supplier.id == supplier_uuid).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = supplier_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    
    return MessageResponse(message="Supplier updated successfully")

@router.put("/{supplier_id}", response_model=MessageResponse)
async def update_supplier(supplier_id: str, supplier_update: SupplierUpdate, db: Session = Depends(get_db)):
    try:
        supplier_uuid = UUID(supplier_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplier ID format")
    
    supplier = db.query(Supplier).filter(Supplier.id == supplier_uuid).first()
    
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    update_data = supplier_update.dict()
    for field, value in update_data.items():
        setattr(supplier, field, value)
    
    db.commit()
    
    return MessageResponse(message="Supplier updated successfully")
