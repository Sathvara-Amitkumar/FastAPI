from fastapi import FastAPI, HTTPException, Query, Path, Depends
from services.products import get_all_products, add_products, remove_product, change_product, load_products, get_db, get_product_id_db
from schema.products import Product
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Session
import config.model_database as model_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8501"],
    allow_methods=["*"]
)

# Search products by name and sort them ----------------------------------------------
@app.get("/products")
def list_products(db: Session = Depends(get_db), # Dependencie Injection
    name: str = Query(min_length=1, max_length=60, default=None, description="Search Peroducts"),
    price: bool = Query(default=False, description="Sort products by price"),
    order: str = Query(default="asc", description="Select order of price (asc or desc)"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=5, ge=1,le=50, description="Maximum number of products to show")
    ):

    # Dependencie Injection
    products = get_all_products(db)

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
        raise HTTPException(status_code=404, detail="No product found!")

    if price:
        rev = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=rev)

    total = len(products)

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    products = products[start:end]
    # products = products[:limit]

    # products = [Product(**p) for p in products]

    return {"Total": total, "Limit": limit, "Items": products}


@app.get("/products/{product_id}")
def get_product_by_id(product_id: UUID = Path(...,description="Search product by product_id", 
                                              examples="6c7b7c69-f07f-4474-992e-58d3c48ac4370"),
                           db: Session = Depends(get_db)):
    
    try:
        return get_product_id_db(product_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Post Methods
@app.post("/products", status_code=201)
def create_product(product: Product, db: Session = Depends(get_db)):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"

    try:
        add_products(product_dict, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product.model_dump(mode="json")


# Delete method
@app.delete("/del_product/{id}", status_code=200)
def delete_product(id: UUID = Path(..., description="Enter product id which u want to delete"), db: Session = Depends(get_db)):
    try:
        res = remove_product(str(id), db)
        return res
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)


# UPdate Method
@app.put("/products/{product_id}")
def update_product(product: Product, product_id: UUID = Path(..., description="Enter product id which u want to delete")):
    try:
        res = change_product(str(product_id), product.model_dump(mode="json", exclude_unset=True))
        return res
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)