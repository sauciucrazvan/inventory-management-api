from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Generator
from uuid import UUID
from pydantic import BaseModel
from models import Product, Warehouse, Stock
from db.session import getSession
from ..rate_limiter import limiter, RateLimitConfig

router = APIRouter(prefix="/warehouses/{warehouse_id}/inventory", tags=["stock_management"])

class StockResponse(BaseModel):
    product_id: str
    sku: str
    stock_quantity: int

class StockIncreaseRequest(BaseModel):
    quantity: int
    supplier_id: str

class StockDecreaseRequest(BaseModel):
    quantity: int
    reason: str

class StockTransferRequest(BaseModel):
    quantity: int
    target_warehouse_id: str
    reason: str

class StockOperationResponse(BaseModel):
    message: str
    new_stock_quantity: int

def get_db() -> Generator[Session, None, None]:
    session = getSession()
    try:
        yield session
    finally:
        session.close()

@router.get("/", response_model=List[StockResponse])
@limiter.limit(RateLimitConfig.READ)
async def get_inventory(request: Request, warehouse_id: str, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid warehouse ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    stocks = db.query(Stock).filter(
        Stock.warehouses.any(Warehouse.id == warehouse_uuid)
    ).all()
    
    return [
        StockResponse(
            product_id=str(stock.product_id),
            sku=stock.sku, # type: ignore
            stock_quantity=stock.stock_quantity # type: ignore
        )
        for stock in stocks
    ]

@router.get("/{product_id}", response_model=StockResponse)
@limiter.limit(RateLimitConfig.READ)
async def get_product_inventory(request: Request, warehouse_id: str, product_id: str, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    stock = db.query(Stock).filter(
        Stock.product_id == product_uuid,
        Stock.warehouses.any(Warehouse.id == warehouse_uuid)
    ).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Product not found in this warehouse")
    
    return StockResponse(
        product_id=str(stock.product_id),
        sku=stock.sku, # type: ignore
        stock_quantity=stock.stock_quantity # type: ignore
    )

@router.post("/{product_id}/increase", response_model=StockOperationResponse)
@limiter.limit(RateLimitConfig.STOCK)
async def increase_product_inventory(request: Request, warehouse_id: str, product_id: str, stock_request: StockIncreaseRequest, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    stock = db.query(Stock).filter(
        Stock.product_id == product_uuid,
        Stock.warehouses.any(Warehouse.id == warehouse_uuid)
    ).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Product not found in this warehouse")
    
    if stock_request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    stock.stock_quantity += stock_request.quantity # type: ignore
    db.commit()
    
    return StockOperationResponse(
        message="Stock increased successfully",
        new_stock_quantity=stock.stock_quantity # type: ignore
    )

@router.post("/{product_id}/decrease", response_model=StockOperationResponse)
@limiter.limit(RateLimitConfig.STOCK)
async def decrease_product_inventory(request: Request, warehouse_id: str, product_id: str, stock_request: StockDecreaseRequest, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    stock = db.query(Stock).filter(
        Stock.product_id == product_uuid,
        Stock.warehouses.any(Warehouse.id == warehouse_uuid)
    ).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="Product not found in this warehouse")
    
    if stock_request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    if stock.stock_quantity < stock_request.quantity: # type: ignore
        raise HTTPException(status_code=400, detail="Insufficient stock quantity")
    
    stock.stock_quantity -= stock_request.quantity # type: ignore
    db.commit()
    
    return StockOperationResponse(
        message="Stock decreased successfully",
        new_stock_quantity=stock.stock_quantity # type: ignore
    )

@router.post("/{product_id}/transfer", response_model=StockOperationResponse)
@limiter.limit(RateLimitConfig.STOCK)
async def transfer_product_inventory(request: Request, warehouse_id: str, product_id: str, stock_request: StockTransferRequest, db: Session = Depends(get_db)):
    try:
        warehouse_uuid = UUID(warehouse_id)
        product_uuid = UUID(product_id)
        target_warehouse_uuid = UUID(stock_request.target_warehouse_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_uuid).first()
    if not warehouse:
        raise HTTPException(status_code=404, detail="Source warehouse not found")
    
    target_warehouse = db.query(Warehouse).filter(Warehouse.id == target_warehouse_uuid).first()
    if not target_warehouse:
        raise HTTPException(status_code=404, detail="Target warehouse not found")
    
    if warehouse_uuid == target_warehouse_uuid:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same warehouse")
    
    source_stock = db.query(Stock).filter(
        Stock.product_id == product_uuid,
        Stock.warehouses.any(Warehouse.id == warehouse_uuid)
    ).first()
    
    if not source_stock:
        raise HTTPException(status_code=404, detail="Product not found in source warehouse")
    
    if stock_request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    
    if source_stock.stock_quantity < stock_request.quantity: # type: ignore
        raise HTTPException(status_code=400, detail="Insufficient stock quantity")
    
    source_stock.stock_quantity -= stock_request.quantity # type: ignore
    
    target_stock = db.query(Stock).filter(
        Stock.product_id == product_uuid,
        Stock.warehouses.any(Warehouse.id == target_warehouse_uuid)
    ).first()
    
    if target_stock:
        target_stock.stock_quantity += stock_request.quantity # type: ignore
    else:
        target_stock = Stock(
            product_id=product_uuid,
            sku=source_stock.sku, # type: ignore
            stock_quantity=stock_request.quantity
        )
        target_stock.warehouses.append(target_warehouse)
        db.add(target_stock)
    
    db.commit()
    
    return StockOperationResponse(
        message="Stock transferred successfully",
        new_stock_quantity=source_stock.stock_quantity # type: ignore
    )
