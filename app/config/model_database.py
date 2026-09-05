from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid

class Base(DeclarativeBase):
    pass


# Seller Model
class Seller(Base):
    __tablename__ = "sellers"
    
    seller_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    email = Column(String)
    website = Column(String)


# Main Product Part
class Product(Base):   
    __tablename__ = "inventory_management"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
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
    seller_id = Column(UUID(as_uuid=True), ForeignKey("sellers.seller_id"))
    seller = relationship("Seller")
    
    created_at = Column(DateTime, default=datetime.utcnow)