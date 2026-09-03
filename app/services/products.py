from pathlib import Path
import json
from typing import List, Dict
from fastapi import Query, Depends

# Database
from sqlalchemy.orm import Session
import config.model_database as model_db
from config.config import session, engine

model_db.base.metadata.create_all(bind=engine)

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

            db.add_all(model_db.Product(**product) for product in products)
            db.commit()
    finally:
        db.close()
        
init_db()


# def get_all_products() -> List[Dict]:
#     return load_products()

def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(model_db.Product).all()
    return db_products


# Save products
def save_products(products: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)


# add product in json and save them
def add_products(product: Dict) -> Dict:
    products = get_all_products()

    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("SKU already exists.")

    products.append(product)
    save_products(products)
    return product


# delete products
def remove_product(id: str) -> str:
    products = get_all_products()

    remove_prod = next((p for p in products if p["id"] == id), None)
    if remove_prod is None:
        raise ValueError("Product not found.")
    
    products.remove(remove_prod)
    save_products(products)
    return "Product removed successfully!"

# This one is also useful !
    # for idx, p in enumerate(products):
	# if p["id"] == str(id):
	# 	delete = products.pop(idx)


# Update product
def change_product(id: str, product: Dict) -> str:
    products = get_all_products()

    update_id = next((p for p in products if p["id"] == id), None)

    if update_id is None:
        raise ValueError("Id is not found!")

    update_id.update(product)
    save_products(products)
    return "Product updated successfully!"