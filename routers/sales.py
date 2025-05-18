from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.schemas import sales as schemas
from app.crud import sales as crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.SaleOut])
def get_sales(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None
):
    """Get sales with optional filtering"""
    return crud.get_filtered_sales(db, start_date, end_date, product_id, category)

@router.post("/", response_model=schemas.SaleOut)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    """Create a new sale"""
    return crud.create_sale(db, sale)

@router.get("/revenue/{period}", response_model=schemas.RevenueAnalysis)
def get_revenue_analysis(
    period: str,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db)
):
    """Get revenue analysis for a specific period"""
    return crud.get_revenue_analysis(db, period, start_date, end_date)

@router.get("/revenue/compare", response_model=schemas.RevenueComparison)
def compare_revenue(
    period: str,
    current_start: datetime,
    current_end: datetime,
    db: Session = Depends(get_db)
):
    """Compare revenue between current and previous period"""
    return crud.compare_revenue(db, period, current_start, current_end)

@router.get("/summary", response_model=schemas.SalesSummary)
def get_sales_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get sales summary including top products and categories"""
    return crud.get_sales_summary(db, start_date, end_date)

@router.get("/by-category", response_model=List[dict])
def get_sales_by_category(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get sales breakdown by category"""
    return crud.get_sales_by_category(db, start_date, end_date)

@router.get("/by-product", response_model=List[dict])
def get_sales_by_product(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get sales breakdown by product"""
    return crud.get_sales_by_product(db, start_date, end_date)
