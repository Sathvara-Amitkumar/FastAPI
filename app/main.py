from fastapi import FastAPI, HTTPException, Query
from services.products import get_all_products

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Hello, PY coder!",
        "error":"i'm stuck."
    }

# @app.get("/products/{id}")
# def get_products(id: int):
#     products = ['Mobile', 'Laptop', 'TV', 'Computer', 'Chair', 'Table', 'PAD']

#     if id < 0 or id >= len(products):
#         raise HTTPException(status_code=404, detail="Product not found")

#     return products[id]

@app.get("/prods")
def all_prod():
    return get_all_products()




@app.get("/products")
def list_products(
    name: str = Query(min_length=1, max_length=60, default=None, description="Search Peroducts"),
    price: bool = Query(default=False, description="Sort products by price"),
    order: str = Query(default="asc", description="Select order of price (asc or desc)"),
    limit: int = Query(default=5, ge=1,le=50, description="Maximum number of products to show")
    ):

    products = get_all_products()

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

    return {"Total": total, "Limit": limit, "Items": products}