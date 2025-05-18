from sqlalchemy.orm import Session
from sqlalchemy import func, desc, cast, Date
from datetime import datetime, timedelta
from typing import List, Optional
from app.models.models import Inventory, Product, InventoryHistory, Sale
from app.schemas.inventory import InventoryCreate, InventoryUpdate, LowStockAlert, InventorySummary, InventoryOut

def get_inventory(db: Session) -> List[InventoryOut]:
    """Get all inventory items"""
    items = db.query(Inventory).all()
    return [InventoryOut.from_orm(item) for item in items]

def create_inventory_item(db: Session, item: InventoryCreate) -> InventoryOut:
    """Create a new inventory item"""
    db_item = Inventory(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return InventoryOut.from_orm(db_item)

def update_inventory(
    db: Session,
    item_id: int,
    update: InventoryUpdate
) -> InventoryOut:
    """Update inventory quantity and track history"""
    db_item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not db_item:
        raise ValueError(f"Inventory item {item_id} not found")
    
    # Create history record
    history = InventoryHistory(
        product_id=db_item.product_id,
        previous_quantity=db_item.quantity,
        new_quantity=update.quantity,
        change_reason=update.change_reason
    )
    db.add(history)
    
    # Update inventory
    db_item.quantity = update.quantity
    db_item.last_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(db_item)
    return InventoryOut.from_orm(db_item)

def get_low_stock_alerts(db: Session) -> List[LowStockAlert]:
    """Get all items that are below their low stock threshold"""
    alerts = db.query(
        Inventory,
        Product.name
    ).join(Product).filter(
        Inventory.quantity <= Inventory.low_stock_threshold
    ).all()
    
    return [
        LowStockAlert(
            product_id=alert.Inventory.product_id,
            product_name=alert.name,
            current_quantity=alert.Inventory.quantity,
            low_stock_threshold=alert.Inventory.low_stock_threshold,
            days_until_stockout=0  # Simplified for interview task
        ) for alert in alerts
    ]

def get_out_of_stock_items(db: Session) -> List[LowStockAlert]:
    """Get all items that are out of stock"""
    alerts = db.query(
        Inventory,
        Product.name
    ).join(Product).filter(
        Inventory.quantity == 0
    ).all()
    
    return [
        LowStockAlert(
            product_id=alert.Inventory.product_id,
            product_name=alert.name,
            current_quantity=0,
            low_stock_threshold=alert.Inventory.low_stock_threshold,
            days_until_stockout=0
        ) for alert in alerts
    ]

def get_inventory_history(
    db: Session,
    product_id: int
) -> List[InventoryHistory]:
    """Get inventory history for a specific product"""
    return db.query(InventoryHistory).filter(
        InventoryHistory.product_id == product_id
    ).order_by(desc(InventoryHistory.change_date)).all()

def get_inventory_summary(db: Session) -> InventorySummary:
    """Get inventory summary including low stock alerts"""
    total_products = db.query(Product).count()
    low_stock_items = get_low_stock_alerts(db)
    out_of_stock_items = get_out_of_stock_items(db)
    
    recently_updated = [
        InventoryOut.from_orm(item) for item in db.query(Inventory)
        .order_by(desc(Inventory.last_updated))
        .limit(5)
        .all()
    ]
    
    return InventorySummary(
        total_products=total_products,
        low_stock_items=low_stock_items,
        out_of_stock_items=out_of_stock_items,
        recently_updated=recently_updated
    )

def get_recently_updated(db: Session) -> List[InventoryOut]:
    """Get recently updated inventory items"""
    items = db.query(Inventory).order_by(
        desc(Inventory.last_updated)
    ).limit(10).all()
    
    return [InventoryOut.from_orm(item) for item in items]

def calculate_days_until_stockout(db: Session, product_id: int) -> Optional[int]:
    # Get average daily sales for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # First, get daily sales counts
    daily_sales = db.query(
        cast(Sale.sale_date, Date).label('sale_date'),
        func.sum(Sale.quantity).label('daily_quantity')
    ).filter(
        Sale.product_id == product_id,
        Sale.sale_date >= thirty_days_ago
    ).group_by(
        cast(Sale.sale_date, Date)
    ).subquery()
    
    # Then calculate the average
    avg_daily_sales = db.query(
        func.avg(daily_sales.c.daily_quantity)
    ).scalar()
    
    if not avg_daily_sales:
        return None
    
    # Get current inventory
    current_inventory = db.query(Inventory).filter(
        Inventory.product_id == product_id
    ).first()
    
    if not current_inventory:
        return None
    
    # Calculate days until stockout
    days_until_stockout = int(current_inventory.quantity / avg_daily_sales)
    return days_until_stockout
