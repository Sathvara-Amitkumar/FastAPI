from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, UUID, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

base = declarative_base()

# Seller Model
class Seller(base):
    __tablename__ = "sellers"
    
    seller_id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    website = Column(String)


# Main Product Part
class Product(base):   
    __tablename__ = "inventory_management"

    id = Column(UUID, primary_key=True, index=True)
    sku = Column(String)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    brand = Column(String)
    price = Column(Float)
    currency = Column(String, default="INR")
    discount_percent = Column(Integer)
    stock = Column(Integer)
    is_active = Column(Boolean, default=True)
    rating = Column(Float)
    tags = Column(String)
    image_urls = Column(String)
    
    # Store dimensions as JSON strings (simpler)
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)
    
    # Foreign key for seller
    seller_id = Column(UUID, ForeignKey("sellers.seller_id"))
    seller = relationship("Seller")
    
    created_at = Column(DateTime, default=datetime.utcnow)