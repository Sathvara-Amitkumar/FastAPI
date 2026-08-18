from fastapi import FastAPI, HTTPException, Query, Path, Depends
from services.products import get_all_products, add_products, remove_product, change_product, load_products
from schema.products import Product
from uuid import uuid4, UUID
from datetime import datetime

app = FastAPI()

# @app.get("/")
# def home():
#     return {
#         "message": "Hello, PY coder!",
#         "error":"i'm stuck."
#     }

# @app.get("/products/{id}")
# def get_products(id: int):
#     products = ['Mobile', 'Laptop', 'TV', 'Computer', 'Chair', 'Table', 'PAD']

#     if id < 0 or id >= len(products):
#         raise HTTPException(status_code=404, detail="Product not found")

#     return products[id]


# All pproducts---------------------------------------------------------------
# @app.get("/prods")
# def all_prod():
#     return get_all_products()


# Search products by name and sort them ----------------------------------------------
@app.get("/products")
def list_products(dep=Depends(load_products), # Dependencie Injection
    name: str = Query(min_length=1, max_length=60, default=None, description="Search Peroducts"),
    price: bool = Query(default=False, description="Sort products by price"),
    order: str = Query(default="asc", description="Select order of price (asc or desc)"),
    limit: int = Query(default=5, ge=1,le=50, description="Maximum number of products to show")
    ):

    # Dependencie Injection
    products = dep

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
        raise HTTPException(status_code=404, detail="No product found!")

    if price:
        rev = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=rev)

    total = len(products)
    products = products[:limit]

    # products = [Product(**p) for p in products]

    return {"Total": total, "Limit": limit, "Items": products}


@app.get("/products/{product_id}")
def get_product_by_id(product_id: str = Path(..., min_length=36, max_length=36, 
                           description="Search product by product_id", example="6c7b7c69-f07f-4474-992e-58d3c48ac4370")):
    
    products = get_all_products()

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail=f"Product Not Found with id => {product_id}")


# Post Methods
@app.post("/products", status_code=201)
def create_product(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"

    try:
        add_products(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return product.model_dump(mode="json")


# Delete method
@app.delete("/del_product/{product_id}", status_code=200)
def delete_product(id: UUID = Path(..., description="Enter product id which u want to delete")):
    try:
        res = remove_product(str(id))
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