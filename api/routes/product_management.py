from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Generator
from uuid import UUID
from pydantic import BaseModel, validator
from models import Product, Warehouse, Stock
from db.session import getSession
from ..rate_limiter import limiter, RateLimitConfig

router = APIRouter(prefix="/warehouses/{warehouse_id}/products", tags=["product_management"])

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock_quantity: int

class ProductUpdate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None

class ProductPatch(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_quantity: Optional[int] = None
    
    @validator('stock_quantity')
    def stock_quantity_not_allowed(cls, v):
        if v is not None:
            raise ValueError("Stock quantity cannot be updated via this endpoint. Use Stock Management endpoints instead.")
        return v

class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    price: float
    stock_quantity: int
    
    class Config:
        from_attributes = True

class ProductDetailResponse(BaseModel):
    id: str
    name: str
    sku: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock_quantity: int
    
    class Config:
        from_attributes = True

class ProductCreateResponse(BaseModel):
    id: str
    message: str

class MessageResponse(BaseModel):
    message: str

def get_db() -> Generator[Session, None, None]:
    session = getSession()
    try:
        yield session
    finally:
        session.close()

@router.post("/", response_model=ProductCreateResponse)
@limiter.limit(RateLimitConfig.WRITE)
async def create_product(request: Request, warehouse_id: str, product: ProductCreate, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid warehouse ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    
    db_product = Product(
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=product.price,
        category=product.category,
        stock_quantity=product.stock_quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Create initial stock record for this warehouse
    stock_record = Stock(
        product_id=db_product.id,
        sku=product.sku,
        stock_quantity=product.stock_quantity
    )
    stock_record.warehouses.append(warehouse)
    db.add(stock_record)
    db.commit()
    
    return ProductCreateResponse(
        id=str(db_product.id),
        message="Product created successfully"
    )

@router.get("/", response_model=List[ProductResponse])
@limiter.limit(RateLimitConfig.READ)
async def get_products(request: Request, warehouse_id: str, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid warehouse ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    products = db.query(Product).all()
    return [
        ProductResponse(
            id=str(product.id),
            name=product.name, # type: ignore
            sku=product.sku, # type: ignore
            price=float(product.price), # type: ignore
            stock_quantity=product.stock_quantity, # type: ignore
        )
        for product in products
    ]

@router.get("/{product_id}", response_model=ProductDetailResponse)
@limiter.limit(RateLimitConfig.READ)
async def get_product(request: Request, warehouse_id: str, product_id: str, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    product = db.query(Product).filter(Product.id == product_uuid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductDetailResponse(
        id=str(product.id),
        name=product.name, # type: ignore
        sku=product.sku, # type: ignore
        description=product.description, # type: ignore
        price=product.price, # type: ignore
        category=product.category, # type: ignore
        stock_quantity=product.stock_quantity # type: ignore
    )

@router.patch("/{product_id}", response_model=MessageResponse)
@limiter.limit(RateLimitConfig.WRITE)
async def patch_product(request: Request, warehouse_id: str, product_id: str, product_update: ProductPatch, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    product = db.query(Product).filter(Product.id == product_uuid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    
    return MessageResponse(message="Product updated successfully")

@router.put("/{product_id}", response_model=MessageResponse)
@limiter.limit(RateLimitConfig.WRITE)
async def update_product(request: Request, warehouse_id: str, product_id: str, product_update: ProductUpdate, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    product = db.query(Product).filter(Product.id == product_uuid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict()
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    
    return MessageResponse(message="Product updated successfully")

@router.delete("/{product_id}", response_model=MessageResponse)
@limiter.limit(RateLimitConfig.WRITE)
async def delete_product(request: Request, warehouse_id: str, product_id: str, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    product = db.query(Product).filter(Product.id == product_uuid).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    
    return MessageResponse(message="Product deleted successfully")
