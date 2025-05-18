# Tech Task Forsit

A comprehensive API for managing operations, including sales analysis, inventory management, and product management.

## Features

### Sales Management
- Retrieve and filter sales data by date range, product, and category
- Analyze revenue on daily, weekly, monthly, and annual basis
- Compare revenue across different periods
- Get sales summaries and breakdowns by product and category

### Inventory Management
- View current inventory status with low stock alerts
- Track inventory changes over time
- Update inventory levels with history tracking
- Get inventory summaries and alerts

### Product Management
- Register and manage products
- Track product categories and pricing
- Monitor product performance

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-admin-api
```


2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the database:
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE ecommerce_db;
exit

# Initialize database tables
python3 -m app.db.init_db

# Populate demo data
python3 -m app.demo.populate_data
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Sales Endpoints

#### GET /sales/
- Get all sales with optional filtering
- Query parameters:
  - start_date: Filter sales from this date
  - end_date: Filter sales until this date
  - product_id: Filter by product
  - category: Filter by category

#### GET /sales/revenue/{period}
- Get revenue analysis for a specific period
- Parameters:
  - period: daily, weekly, monthly, annual
  - start_date: Start date for analysis
  - end_date: End date for analysis

#### GET /sales/revenue/compare
- Compare revenue between current and previous period
- Parameters:
  - period: daily, weekly, monthly, annual
  - current_start: Start date of current period
  - current_end: End date of current period

#### GET /sales/summary
- Get sales summary including top products and categories
- Query parameters:
  - start_date: Optional start date
  - end_date: Optional end date

#### GET /sales/by-category
- Get sales breakdown by category
- Query parameters:
  - start_date: Optional start date
  - end_date: Optional end date

#### GET /sales/by-product
- Get sales breakdown by product
- Query parameters:
  - start_date: Optional start date
  - end_date: Optional end date

### Inventory Endpoints

#### GET /inventory/
- Get all inventory items

#### POST /inventory/
- Create a new inventory item

#### PUT /inventory/{item_id}
- Update inventory quantity
- Body:
  - quantity: New quantity
  - change_reason: Reason for the change

#### GET /inventory/low-stock
- Get all items that are low in stock

#### GET /inventory/history/{product_id}
- Get inventory history for a specific product

#### GET /inventory/summary
- Get inventory summary including low stock alerts

#### GET /inventory/out-of-stock
- Get all items that are out of stock

#### GET /inventory/recently-updated
- Get recently updated inventory items

### Product Endpoints

#### GET /products/
- Get all products

#### POST /products/
- Create a new product
- Body:
  - name: Product name
  - category: Product category
  - price: Product price
  - description: Optional product description

## Database Schema

### Products Table
- id: Primary key
- name: Product name
- category: Product category
- price: Product price
- description: Product description
- created_at: Creation timestamp
- updated_at: Last update timestamp

### Inventory Table
- id: Primary key
- product_id: Foreign key to products
- quantity: Current quantity
- low_stock_threshold: Threshold for low stock alerts
- last_updated: Last update timestamp

### Sales Table
- id: Primary key
- product_id: Foreign key to products
- quantity: Quantity sold
- total_amount: Total sale amount
- sale_date: Sale timestamp

### Inventory History Table
- id: Primary key
- product_id: Foreign key to products
- previous_quantity: Previous quantity
- new_quantity: New quantity
- change_date: Change timestamp
- change_reason: Reason for the change
