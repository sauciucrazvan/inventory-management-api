from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from db.session import base as Base

# Association tables for many-to-many relationships
stock_suppliers = Table(
    'stock_suppliers',
    Base.metadata,
    Column('stock_id', UUID(as_uuid=True), ForeignKey('stocks.id'), primary_key=True),
    Column('supplier_id', UUID(as_uuid=True), ForeignKey('suppliers.id'), primary_key=True)
)

stock_warehouses = Table(
    'stock_warehouses', 
    Base.metadata,
    Column('stock_id', UUID(as_uuid=True), ForeignKey('stocks.id'), primary_key=True),
    Column('warehouse_id', UUID(as_uuid=True), ForeignKey('warehouses.id'), primary_key=True)
)

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    sku = Column(String(50), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="stocks")
    suppliers = relationship("Supplier", secondary=stock_suppliers, back_populates="stocks")
    warehouses = relationship("Warehouse", secondary=stock_warehouses, back_populates="stocks")
