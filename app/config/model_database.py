from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, UUID, Float, Integer, literal, Boolean, DateTime

base = declarative_base()

class Seller():
    seller_id = Column(UUID, primary_key=True)
    name = Column(String)
    email = Column(String)
    website = Column(String)


# Dimensions Model
class Dimensions():
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)


# Main Product Part
class Product(base):   
    id = Column(UUID, primary_key=True)
    
    sku = Column(String, )
    
    name = Column(String)
    
    description = Column(String)

    category = Column(String)

    brand = Column(String)

    price = Column(Float)

    currency = Column(literal, default="INR")

    discount_percent = Column(Integer)

    stock = Column(Integer)

    is_active = Column(Boolean, default=True)

    rating = Column(Float)

    tags = Column(String)

    image_urls = Column(String)

    dimensions_cm: Dimensions

    seller: Seller

    created_at: DateTime