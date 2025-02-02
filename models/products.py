from pandas.core.interchange import column
from sqlalchemy import Column, Integer, String, Float
from models.db_manager import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    model = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        return f"<Product(id={self.id}, model={self.model}, price={self.price})>"
