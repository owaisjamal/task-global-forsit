import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import Base
from app.db.session import engine
from app.models import models

Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
