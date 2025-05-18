from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional
from app.models.models import Sale, Product
from app.schemas.sales import SaleCreate, RevenueAnalysis, RevenueComparison, SalesSummary

def get_filtered_sales(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
    category: Optional[str] = None
) -> List[Sale]:
    query = db.query(Sale)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if category:
        query = query.join(Product).filter(Product.category == category)
    
    return query.all()

def create_sale(db: Session, sale: SaleCreate) -> Sale:
    db_sale = Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_revenue_analysis(
    db: Session,
    period: str,
    start_date: datetime,
    end_date: datetime
) -> RevenueAnalysis:
    query = db.query(
        func.sum(Sale.total_amount).label('total_revenue'),
        func.count(Sale.id).label('total_sales'),
        func.avg(Sale.total_amount).label('average_order_value')
    ).filter(
        Sale.sale_date.between(start_date, end_date)
    )
    
    result = query.first()
    
    return RevenueAnalysis(
        period=period,
        start_date=start_date,
        end_date=end_date,
        total_revenue=result.total_revenue or 0,
        total_sales=result.total_sales or 0,
        average_order_value=result.average_order_value or 0
    )

def compare_revenue(
    db: Session,
    period: str,
    current_start: datetime,
    current_end: datetime
) -> RevenueComparison:
    # Calculate period duration
    duration = current_end - current_start
    
    # Calculate previous period
    previous_start = current_start - duration
    previous_end = current_start
    
    current_period = get_revenue_analysis(db, period, current_start, current_end)
    previous_period = get_revenue_analysis(db, period, previous_start, previous_end)
    
    # Calculate percentage change
    if previous_period.total_revenue == 0:
        percentage_change = 100
    else:
        percentage_change = ((current_period.total_revenue - previous_period.total_revenue) 
                           / previous_period.total_revenue * 100)
    
    return RevenueComparison(
        current_period=current_period,
        previous_period=previous_period,
        percentage_change=percentage_change
    )

def get_sales_summary(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> SalesSummary:
    query = db.query(Sale)
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    
    # Get total revenue and sales
    totals = query.with_entities(
        func.sum(Sale.total_amount).label('total_revenue'),
        func.count(Sale.id).label('total_sales')
    ).first()
    
    # Get top products
    top_products = db.query(
        Product.name,
        func.sum(Sale.total_amount).label('revenue'),
        func.count(Sale.id).label('sales_count')
    ).join(Sale).group_by(Product.id).order_by(desc('revenue')).limit(5).all()
    
    # Get top categories
    top_categories = db.query(
        Product.category,
        func.sum(Sale.total_amount).label('revenue'),
        func.count(Sale.id).label('sales_count')
    ).join(Sale).group_by(Product.category).order_by(desc('revenue')).limit(5).all()
    
    return SalesSummary(
        total_revenue=totals.total_revenue or 0,
        total_sales=totals.total_sales or 0,
        top_products=[{
            'name': p.name,
            'revenue': p.revenue,
            'sales_count': p.sales_count
        } for p in top_products],
        top_categories=[{
            'category': c.category,
            'revenue': c.revenue,
            'sales_count': c.sales_count
        } for c in top_categories]
    )

def get_sales_by_category(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[dict]:
    query = db.query(
        Product.category,
        func.sum(Sale.total_amount).label('revenue'),
        func.count(Sale.id).label('sales_count')
    ).join(Sale)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    
    results = query.group_by(Product.category).all()
    
    return [{
        'category': r.category,
        'revenue': r.revenue,
        'sales_count': r.sales_count
    } for r in results]

def get_sales_by_product(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[dict]:
    query = db.query(
        Product.name,
        Product.category,
        func.sum(Sale.total_amount).label('revenue'),
        func.count(Sale.id).label('sales_count')
    ).join(Sale)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    
    results = query.group_by(Product.id).all()
    
    return [{
        'name': r.name,
        'category': r.category,
        'revenue': r.revenue,
        'sales_count': r.sales_count
    } for r in results]
