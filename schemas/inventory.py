from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class InventoryBase(BaseModel):
    product_id: int
    quantity: int
    low_stock_threshold: int

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: int
    change_reason: str

class InventoryOut(InventoryBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class InventoryHistoryOut(BaseModel):
    id: int
    product_id: int
    previous_quantity: int
    new_quantity: int
    change_date: datetime
    change_reason: str

    class Config:
        from_attributes = True

class LowStockAlert(BaseModel):
    product_id: int
    product_name: str
    current_quantity: int
    low_stock_threshold: int
    days_until_stockout: Optional[int]

class InventorySummary(BaseModel):
    total_products: int
    low_stock_items: List[LowStockAlert]
    out_of_stock_items: List[LowStockAlert]
    recently_updated: List[InventoryOut]

class InventoryHistory(BaseModel):
    id: int
    product_id: int
    previous_quantity: int
    new_quantity: int
    change_reason: str
    change_date: datetime

    class Config:
        from_attributes = True
