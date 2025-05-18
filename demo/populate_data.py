from app.db.session import SessionLocal
from app.models.models import Product, Inventory, Sale, InventoryHistory
import datetime
import random
from decimal import Decimal

def create_demo_data():
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Sale).delete()
        db.query(InventoryHistory).delete()
        db.query(Inventory).delete()
        db.query(Product).delete()
        db.commit()

        # Create products
        products = [
            # Electronics
            Product(name="iPhone 13", category="Electronics", price=799.99, description="Latest iPhone model"),
            Product(name="Samsung Galaxy S21", category="Electronics", price=699.99, description="Flagship Android phone"),
            Product(name="MacBook Pro", category="Electronics", price=1299.99, description="Professional laptop"),
            Product(name="Sony WH-1000XM4", category="Electronics", price=349.99, description="Noise-cancelling headphones"),
            Product(name="iPad Air", category="Electronics", price=599.99, description="Versatile tablet"),
            
            # Clothing
            Product(name="Nike Air Max", category="Clothing", price=129.99, description="Popular running shoes"),
            Product(name="Levi's 501", category="Clothing", price=59.99, description="Classic jeans"),
            Product(name="Adidas T-Shirt", category="Clothing", price=29.99, description="Casual wear"),
            Product(name="North Face Jacket", category="Clothing", price=199.99, description="Winter jacket"),
            Product(name="Under Armour Shorts", category="Clothing", price=34.99, description="Athletic shorts"),
            
            # Home & Kitchen
            Product(name="Instant Pot", category="Home & Kitchen", price=89.99, description="Multi-cooker"),
            Product(name="KitchenAid Mixer", category="Home & Kitchen", price=299.99, description="Stand mixer"),
            Product(name="Dyson Vacuum", category="Home & Kitchen", price=399.99, description="Cordless vacuum"),
            Product(name="Calphalon Pan Set", category="Home & Kitchen", price=199.99, description="Non-stick cookware"),
            Product(name="Ninja Blender", category="Home & Kitchen", price=79.99, description="High-speed blender")
        ]
        
        db.add_all(products)
        db.commit()
        
        # Create inventory with varying levels
        for product in products:
            # Random initial quantity between 50 and 200
            initial_quantity = random.randint(50, 200)
            # Random low stock threshold between 10 and 30
            low_stock_threshold = random.randint(10, 30)
            
            inventory = Inventory(
                product_id=product.id,
                quantity=initial_quantity,
                low_stock_threshold=low_stock_threshold
            )
            db.add(inventory)
        db.commit()
        
        # Create sales records for the last 90 days
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=90)
        
        # Generate sales for each day
        current_date = start_date
        while current_date <= end_date:
            # Generate 5-20 sales per day
            num_sales = random.randint(5, 20)
            
            for _ in range(num_sales):
                # Randomly select a product
                product = random.choice(products)
                # Random quantity between 1 and 5
                quantity = random.randint(1, 5)
                # Calculate total amount
                total_amount = float(Decimal(str(product.price)) * Decimal(str(quantity)))
                
                # Create sale record
                sale = Sale(
                    product_id=product.id,
                    quantity=quantity,
                    total_amount=total_amount,
                    sale_date=current_date
                )
                db.add(sale)
                
                # Update inventory
                inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()
                if inventory:
                    # Create inventory history record
                    history = InventoryHistory(
                        product_id=product.id,
                        previous_quantity=inventory.quantity,
                        new_quantity=inventory.quantity - quantity,
                        change_reason="Sale"
                    )
                    db.add(history)
                    
                    # Update inventory quantity
                    inventory.quantity -= quantity
            
            # Move to next day
            current_date += datetime.timedelta(days=1)
        
        # Add some inventory adjustments
        for product in products:
            inventory = db.query(Inventory).filter(Inventory.product_id == product.id).first()
            if inventory:
                # Random adjustment between -20 and +50
                adjustment = random.randint(-20, 50)
                if adjustment != 0:
                    history = InventoryHistory(
                        product_id=product.id,
                        previous_quantity=inventory.quantity,
                        new_quantity=inventory.quantity + adjustment,
                        change_reason="Stock adjustment"
                    )
                    db.add(history)
                    inventory.quantity += adjustment
        
        db.commit()
        print("Demo data successfully populated!")
        
    except Exception as e:
        print(f"Error populating demo data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_data()
