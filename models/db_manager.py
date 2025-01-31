from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from datetime import datetime
from models.orders import Order
from models.users import User

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///mokka.db")

# Create an engine for connection manage threads with check_same_thread
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a base for all models derived by DB
Base = declarative_base()

# Crea una sessione
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.utcnow()

# Create listener because SQLAlchemy doesn't support trigger directly
event.listen(Order, "before_update", update_timestamp)
event.listen(User, "before_update", update_timestamp)
