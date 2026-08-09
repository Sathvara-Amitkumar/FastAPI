from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Hello, PY coder!",
        "error":"i'm stuck."
    }

@app.get("/products/{id}")
def get_products(id: int):
    products = ['Mobile', 'Laptop', 'TV', 'Computer', 'Chair', 'Table', 'PAD']

    if id < 0 or id >= len(products):
        raise HTTPException(status_code=404, detail="Product not found")

    return products[id]
