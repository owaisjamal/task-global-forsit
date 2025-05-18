from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas import inventory as schemas
from app.crud import inventory as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.InventoryOut])
def get_inventory(db: Session = Depends(get_db)):
    """Get all inventory items"""
    return crud.get_inventory(db)

@router.post("/", response_model=schemas.InventoryOut)
def create_inventory_item(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    return crud.create_inventory_item(db, item)

@router.put("/{item_id}", response_model=schemas.InventoryOut)
def update_inventory(
    item_id: int,
    update: schemas.InventoryUpdate,
    db: Session = Depends(get_db)
):
    """Update inventory quantity and track history"""
    return crud.update_inventory(db, item_id, update)

@router.get("/low-stock", response_model=List[schemas.LowStockAlert])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    """Get all items that are low in stock"""
    return crud.get_low_stock_alerts(db)

@router.get("/history/{product_id}", response_model=List[schemas.InventoryHistoryOut])
def get_inventory_history(product_id: int, db: Session = Depends(get_db)):
    """Get inventory history for a specific product"""
    return crud.get_inventory_history(db, product_id)

@router.get("/summary", response_model=schemas.InventorySummary)
def get_inventory_summary(db: Session = Depends(get_db)):
    """Get inventory summary including low stock alerts"""
    return crud.get_inventory_summary(db)

@router.get("/out-of-stock", response_model=List[schemas.LowStockAlert])
def get_out_of_stock_items(db: Session = Depends(get_db)):
    """Get all items that are out of stock"""
    return crud.get_out_of_stock_items(db)

@router.get("/recently-updated", response_model=List[schemas.InventoryOut])
def get_recently_updated(db: Session = Depends(get_db)):
    """Get recently updated inventory items"""
    return crud.get_recently_updated(db)
