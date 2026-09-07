# FastAPI Product CRUD Management

## Project Overview

A full-stack Product CRUD Management application built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Pydantic**, and **Streamlit**.

The project provides a REST API for managing products and sellers, together with a Streamlit interface for interacting with the API. It supports creating, reading, updating, deleting, searching, sorting, and paginating products.

**Live Demo:** https://fastapi-crud-app.streamlit.app/

### Main Features

- Product CRUD operations
- PostgreSQL database integration
- SQLAlchemy ORM
- Pydantic data validation and business rules
- Seller-product relationship
- Product search, sorting, and pagination
- Product dimensions and seller information
- Computed values such as `final_price` and `volume`
- Interactive Swagger API documentation
- Streamlit frontend
- Deployment with Render and Streamlit Cloud

---

## Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Sathvara-Amitkumar/FastAPI.git
cd FastAPI
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r app/requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database and configure the connection using the `DATABASE_URL` environment variable.

Example:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/project_fastapi
```

Do not commit database credentials to GitHub.

For production, use the PostgreSQL connection URL provided by the hosting platform.

---

## Usage

### Run the FastAPI backend

From the project root:

```bash
cd app
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the API.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | List products with search, sorting, and pagination |
| GET | `/products/{product_id}` | Get a product by UUID |
| POST | `/products` | Create a product |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/del_product/{id}` | Delete a product |

### Run the Streamlit frontend

From the project root:

```bash
streamlit run app/app.py
```

The frontend communicates with the FastAPI backend through HTTP requests.

---

## Implementation Details

### Project Structure

```text
FastAPI/
└── app/
    ├── config/
    │   ├── config.py
    │   └── model_database.py
    ├── data/
    │   └── products.json
    ├── schema/
    │   └── products.py
    ├── services/
    │   └── products.py
    ├── main.py
    ├── app.py
    └── requirements.txt
```

> `products.json` belongs to the earlier JSON-based implementation. The current application uses PostgreSQL as the primary database.

### FastAPI Layer

`main.py` defines the API routes and handles database-session dependency injection.

### Pydantic Schema Layer

`schema/products.py` contains the data models and validation rules for products and sellers.

It includes validation for:

- UUIDs
- SKU format
- Price
- Stock
- Rating
- Discount percentage
- Seller email domains
- Product business rules

It also defines computed values such as:

```text
final_price
volume
```

### Database Layer

`config/config.py` creates the SQLAlchemy engine and database session using `DATABASE_URL`.

`config/model_database.py` defines the SQLAlchemy models, including:

- `Seller`
- `Product`
- Seller-product relationship
- Product dimensions
- PostgreSQL-specific fields

### Service Layer

`services/products.py` contains the database CRUD logic.

It handles:

- Retrieving products
- Finding products by UUID
- Creating products
- Updating products
- Deleting products
- Duplicate SKU checking
- Converting SQLAlchemy objects into API-friendly dictionaries

### Streamlit Frontend

`app.py` provides the user interface and sends HTTP requests to the FastAPI backend.

The interface includes:

- Product dashboard
- Product creation
- Product search
- Product update
- Product deletion
- Sorting and pagination

### Overall Architecture

```text
              Streamlit
                 |
                 | HTTP Requests
                 v
              FastAPI
                 |
                 | SQLAlchemy ORM
                 v
             PostgreSQL
```

---

## Common Problems and Challenges

### 1. PostgreSQL Connection Refused

If you see an error such as:

```text
connection refused
localhost:2580
```

check that PostgreSQL is running locally and that the configured port is correct.

On production, do not use `localhost`. Use the hosted PostgreSQL URL through `DATABASE_URL`.

### 2. Hardcoded Database Credentials

Avoid putting credentials directly into source code.

Use:

```python
import os

db_url = os.getenv("DATABASE_URL")
```

Then configure `DATABASE_URL` in the local environment or hosting platform.

### 3. POST Returns `{}`

A SQLAlchemy ORM object should be converted before returning it from the API.

For example:

```python
return product_to_dict(created_product)
```

Make sure `created_product` is the object returned by the service function, not the route function itself.

### 4. Duplicate SKU

Before inserting a product, check whether the SKU already exists:

```python
existing_product = (
    db.query(model_db.Product)
    .filter(model_db.Product.sku == product["sku"])
    .first()
)
```

If it exists, return an appropriate error.

### 5. Existing Local Data Is Not Automatically Transferred

Moving the application from a local PostgreSQL database to a hosted PostgreSQL database does not automatically copy existing records.

PostgreSQL tools such as `pg_dump` and `pg_restore` can be used to migrate the existing data.

Example backup:

```bash
pg_dump -h localhost -p 2580 -U postgres -d project_fastapi -F c -f fastapi_data.dump
```

A data-only dump can be restored into an already-created database when the target schema already exists.

### 6. `create_all()` Is Not a Full Migration Tool

SQLAlchemy:

```python
Base.metadata.create_all(...)
```

creates missing tables, but it does not handle existing schema changes like a full migration system.

For future production schema changes, consider using **Alembic**.

### 7. Local and Production Databases Are Different

The local and hosted databases are separate.

```text
Local Application
       ↓
Local PostgreSQL
       ↓
project_fastapi


Production Application
       ↓
Render FastAPI
       ↓
Render PostgreSQL
       ↓
fastapi_product_db_...
```

Data created in one environment does not automatically appear in the other.

### 8. Computed Fields

The project uses computed product values such as:

```text
final_price = price × (1 - discount_percent / 100)
volume = length × width × height
```

These can be calculated at the API/model level and, when configured, at the PostgreSQL level using generated columns.

---

## Deployment

### FastAPI Backend

The FastAPI backend can be deployed as a Render Web Service.

Typical start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Set the production database connection as:

```text
DATABASE_URL=<Render PostgreSQL connection URL>
```

Do not expose database credentials publicly.

### Streamlit Frontend

The Streamlit frontend is deployed through Streamlit Community Cloud.

The frontend should use the deployed FastAPI URL as its API base URL rather than the local development URL.

Example:

```python
API_BASE_URL = "https://your-fastapi-service.onrender.com"
```

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/my-feature
```

3. Make your changes.
4. Test the API and frontend.
5. Commit your changes:

```bash
git add .
git commit -m "Add my feature"
```

6. Push your branch:

```bash
git push origin feature/my-feature
```

7. Open a Pull Request.

---

## License

This project is available for learning and development purposes.
