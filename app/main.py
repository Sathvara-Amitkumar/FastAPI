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

@app.get("/prod")
def all_prod():
    return get_all_products()


@app.get("/products")
def list_products(name: str = Query(min_length=1, max_length=60, default=None, description="Search Peroducts!")):
    products = get_all_products()

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

        if not products:
            raise HTTPException(status_code=404, detail="No product found!")

        total = len(products)

    return {"Total": total, "Items": products}