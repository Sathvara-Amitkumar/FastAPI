from pathlib import Path
import json
from typing import List, Dict
from fastapi import Query, Depends, HTTPException
from uuid import UUID

# Database
from sqlalchemy.orm import Session
import config.model_database as model_db
from config.config import session, engine

model_db.Base.metadata.create_all(bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


DATA_FILE = Path(__file__).parent.parent / "data" / "products.json"

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return "File Path not exist"

    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


# Database -> Add all products from JSON
def init_db():
    db = session()
    try:
        count = db.query(model_db.Product).count()

        if count == 0:
            if not DATA_FILE.exists():
                return "File path not exist."

            with open(DATA_FILE, "r", encoding="utf-8") as file:
                products = json.load(file)

            for product in products:
                seller_data = product.get("seller")
                if seller_data:
                    seller = model_db.Seller(
                        seller_id = seller_data["seller_id"],
                        name = seller_data["name"],
                        email = seller_data["email"],
                        website = seller_data["website"]
                    )
                    db.add(seller)

                dimensions = product.get("dimensions_cm", {})

                product_data = {
                    "id": product["id"],
                    "sku": product["sku"],
                    "name": product["name"],
                    "description": product["description"],
                    "category": product["category"],
                    "brand": product["brand"],
                    "price": product["price"],
                    "currency": product["currency"],
                    "discount_percent": product["discount_percent"],
                    "stock": product["stock"],
                    "is_active": product["is_active"],
                    "rating": product["rating"],
                    "tags": product["tags"],
                    "image_urls": product["image_urls"],

                    "length": dimensions.get("length"),
                    "width": dimensions.get("width"),
                    "height": dimensions.get("height"),

                    "seller_id": seller_data.get("seller_id") if seller_data else None,

                    "created_at": product["created_at"]
                }
                db.add(model_db.Product(**product_data))
            
            db.commit()
    finally:
        db.close()
        
init_db()


# def get_all_products() -> List[Dict]:
#     return load_products()

def get_all_products(db: Session) -> List:
    db_products = db.query(model_db.Product).all()
    return db_products


# Get product by id
def get_product_id_db(product_id: UUID, db: Session):
    product = db.get(model_db.Product, product_id)

    if not product:
        raise ValueError("Product not found!")
    return product


# Save products
def save_products(products: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)


# add product in json and save them
def add_products(product: Dict, db: Session) -> Dict:
    products = get_all_products(db)
    sku = product.get("sku")

    if any(p.sku == sku for p in products):
        raise ValueError("SKU already exists.")

    # Seller
    seller_data = product.get("seller")
    if seller_data:
        seller = db.get(model_db.Seller, seller_data["seller_id"])
        if seller is None:
            seller = model_db.Seller(seller_id=seller_data["seller_id"])
            db.add(seller)

        seller.name = seller_data["name"]
        seller.email = str(seller_data["email"])
        seller.website = str(seller_data["website"])

    db.add(seller)

    # Dimensions
    dimensions = product.get("dimensions_cm", {})

    # Product
    db_product = model_db.Product(
        id=product["id"],
        sku=product["sku"],
        name=product["name"],
        description=product["description"],
        category=product["category"],
        brand=product["brand"],
        price=product["price"],
        currency=product["currency"],
        discount_percent=product["discount_percent"],
        stock=product["stock"],
        is_active=product["is_active"],
        rating=product["rating"],
        tags=product["tags"],
        image_urls=product["image_urls"],

        length=dimensions.get("length"),
        width=dimensions.get("width"),
        height=dimensions.get("height"),

        seller_id=seller_data["seller_id"],
        created_at=product["created_at"]
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


# delete products
def remove_product(id: str, db: Session) -> str:
    db_product = db.get(model_db.Product, id)

    if not db_product:
        raise ValueError("Product not found!")

    db.delete(db_product)
    db.commit()
    return "Product deleted successfully!"


# Update product
def change_product(id: str, product: Dict, db: Session) -> str:
    db_product = db.query(model_db.Product).filter(
        model_db.Product.id == id
    ).first()

    if not db_product:
        raise ValueError("Product not found!")

    dimensions = product.get("dimensions_cm", {})

    seller_data = product.get("seller")
    
    if seller_data:
        seller = db.query(model_db.Product).filter(
            model_db.Seller.seller_id == seller_data["seller_id"]
        ).first()

        if not seller:
            raise ValueError("Seller not found!")

        db_product.seller_id = seller.seller_id

    # Product fields
    db_product.sku = product["sku"]
    db_product.name = product["name"]
    db_product.description = product["description"]
    db_product.category = product["category"]
    db_product.brand = product["brand"]
    db_product.price = product["price"]
    db_product.currency = product["currency"]
    db_product.discount_percent = product["discount_percent"]
    db_product.stock = product["stock"]
    db_product.is_active = product["is_active"]
    db_product.rating = product["rating"]
    db_product.tags = product["tags"]
    db_product.image_urls = product["image_urls"]

    # Dimensions
    db_product.length = dimensions.get("length")
    db_product.width = dimensions.get("width")
    db_product.height = dimensions.get("height")

    db_product.created_at = product["created_at"]

    db.commit()
    db.refresh(db_product)

    return db_product