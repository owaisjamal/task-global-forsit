from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_amount: float

class SaleCreate(SaleBase):
    pass

class SaleOut(SaleBase):
    id: int
    sale_date: datetime

    class Config:
        orm_mode = True

class SaleFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    product_id: Optional[int] = None
    category: Optional[str] = None

class RevenueAnalysis(BaseModel):
    period: str  # daily, weekly, monthly, annual
    start_date: datetime
    end_date: datetime
    total_revenue: float
    total_sales: int
    average_order_value: float

class RevenueComparison(BaseModel):
    current_period: RevenueAnalysis
    previous_period: RevenueAnalysis
    percentage_change: float

class SalesSummary(BaseModel):
    total_revenue: float
    total_sales: int
    top_products: List[dict]
    top_categories: List[dict]
