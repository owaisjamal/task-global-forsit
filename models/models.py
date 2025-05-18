from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Add indexes for frequently queried fields
    __table_args__ = (
        Index('idx_product_category', 'category'),
        Index('idx_product_name', 'name'),
    )

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    product = relationship("Product")

    # Add index for low stock queries
    __table_args__ = (
        Index('idx_inventory_low_stock', 'quantity', 'low_stock_threshold'),
    )

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    sale_date = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    product = relationship("Product")

    # Add indexes for date-based queries
    __table_args__ = (
        Index('idx_sale_date', 'sale_date'),
        Index('idx_sale_product_date', 'product_id', 'sale_date'),
    )

class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    previous_quantity = Column(Integer)
    new_quantity = Column(Integer)
    change_date = Column(DateTime, default=datetime.datetime.utcnow)
    change_reason = Column(String(255))
    product = relationship("Product")

    # Add index for history queries
    __table_args__ = (
        Index('idx_inventory_history_date', 'change_date'),
        Index('idx_inventory_history_product', 'product_id'),
    )
