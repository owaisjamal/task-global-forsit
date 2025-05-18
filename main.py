from fastapi import FastAPI
from app.routers import sales, inventory, products

app = FastAPI(title="E-commerce Admin API")

app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(products.router, prefix="/products", tags=["Products"])
