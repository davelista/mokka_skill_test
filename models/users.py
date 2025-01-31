import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db_manager import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(320), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with orders
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        salt = bcrypt.gensalt()  # Generate a salt
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash password
        return self.password.decode('utf-8')  # Convert bytes to string for storage

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))  # Compare 2 password in bytes

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
