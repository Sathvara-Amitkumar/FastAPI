import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timezone
from uuid import uuid4

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="FastAPI Product Manager",
    page_icon="📦",
    layout="wide",
)

st.title("📦 Product Management Dashboard")

API_BASE_URL = "http://127.0.0.1:8000"

TIMEOUT = 10


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def api_request(method, endpoint, **kwargs):
    """Make an HTTP request to the FastAPI backend."""
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{endpoint}",
            timeout=TIMEOUT,
            **kwargs,
        )
        return response
    except requests.exceptions.ConnectionError:
        st.error(
            f"Cannot connect to FastAPI at `{API_BASE_URL}`. "
            "Start your FastAPI server first."
        )
    except requests.exceptions.Timeout:
        st.error("Request timed out.")
    except requests.exceptions.RequestException as exc:
        st.error(f"Request failed: {exc}")
    return None


def show_api_error(response):
    if response is None:
        return

    try:
        detail = response.json().get("detail", response.text)
    except ValueError:
        detail = response.text

    st.error(f"HTTP {response.status_code}: {detail}")


def get_products(page=1):
    response = api_request(
        "GET",
        "/products",
        params={"page": page, "limit": 50},
    )

    if response is None or not response.ok:
        if response is not None:
            show_api_error(response)
        return [], 0

    data = response.json()
    return data.get("Items", []), data.get("Total", 0)


def get_product(product_id):
    response = api_request("GET", f"/products/{product_id}")

    if response is None or not response.ok:
        if response is not None:
            show_api_error(response)
        return None

    return response.json()


def safe_list(value):
    return value if isinstance(value, list) else []


def build_product_payload(
    *,
    name,
    sku,
    description,
    category,
    brand,
    price,
    discount_percent,
    stock,
    is_active,
    rating,
    tags,
    image_urls,
    dimensions,
    seller,
    product_id=None,
    created_at=None,
):
    """
    Product schema in the current FastAPI project requires id and
    created_at, even though the POST endpoint replaces those values.
    """
    return {
        "id": product_id or str(uuid4()),
        "sku": sku,
        "name": name,
        "description": description,
        "category": category,
        "brand": brand,
        "price": price,
        "currency": "INR",
        "discount_percent": discount_percent,
        "stock": stock,
        "is_active": is_active,
        "rating": rating,
        "tags": tags or None,
        "image_urls": image_urls,
        "dimensions_cm": dimensions,
        "seller": seller,
        "created_at": created_at
        or datetime.now(timezone.utc).isoformat(),
    }


def product_form(defaults=None, key_prefix="form"):
    """Reusable product form. If defaults are supplied, populate the form."""
    defaults = defaults or {}

    dimensions = defaults.get("dimensions_cm") or {}
    seller = defaults.get("seller") or {}

    default_tags = safe_list(defaults.get("tags"))
    default_images = safe_list(defaults.get("image_urls"))

    st.subheader("Product Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input(
            "Product Name *",
            value=defaults.get("name", ""),
            key=f"{key_prefix}_name",
        )
        sku = st.text_input(
            "SKU *",
            value=defaults.get("sku", ""),
            key=f"{key_prefix}_sku",
        )
        category = st.text_input(
            "Category *",
            value=defaults.get("category", ""),
            key=f"{key_prefix}_category",
        )

    with col2:
        brand = st.text_input(
            "Brand *",
            value=defaults.get("brand", ""),
            key=f"{key_prefix}_brand",
        )
        price = st.number_input(
            "Price (INR) *",
            min_value=0.01,
            value=float(defaults.get("price", 1.0)),
            step=100.0,
            key=f"{key_prefix}_price",
        )
        discount = st.number_input(
            "Discount (%) *",
            min_value=0,
            max_value=100,
            value=int(defaults.get("discount_percent", 0)),
            key=f"{key_prefix}_discount",
        )

    with col3:
        stock = st.number_input(
            "Stock *",
            min_value=0,
            value=int(defaults.get("stock", 0)),
            step=1,
            key=f"{key_prefix}_stock",
        )
        rating = st.number_input(
            "Rating *",
            min_value=0.0,
            max_value=5.0,
            value=float(defaults.get("rating", 0.0)),
            step=0.1,
            key=f"{key_prefix}_rating",
        )
        is_active = st.checkbox(
            "Active",
            value=bool(defaults.get("is_active", True)),
            key=f"{key_prefix}_active",
        )

    description = st.text_area(
        "Description *",
        value=defaults.get("description", ""),
        max_chars=200,
        key=f"{key_prefix}_description",
    )

    tags_text = st.text_input(
        "Tags (comma separated)",
        value=", ".join(str(x) for x in default_tags),
        key=f"{key_prefix}_tags",
    )

    image_text = st.text_input(
        "Image URLs (comma separated, max 5)",
        value=", ".join(str(x) for x in default_images),
        key=f"{key_prefix}_images",
    )

    st.subheader("Dimensions (cm)")
    d1, d2, d3 = st.columns(3)

    with d1:
        length = st.number_input(
            "Length",
            min_value=0.0,
            value=float(dimensions.get("length", 0.0)),
            step=0.1,
            key=f"{key_prefix}_length",
        )
    with d2:
        width = st.number_input(
            "Width",
            min_value=0.0,
            value=float(dimensions.get("width", 0.0)),
            step=0.1,
            key=f"{key_prefix}_width",
        )
    with d3:
        height = st.number_input(
            "Height",
            min_value=0.0,
            value=float(dimensions.get("height", 0.0)),
            step=0.1,
            key=f"{key_prefix}_height",
        )

    st.subheader("Seller")
    s1, s2 = st.columns(2)

    with s1:
        seller_id = st.text_input(
            "Seller UUID *",
            value=str(seller.get("seller_id") or uuid4()),
            key=f"{key_prefix}_seller_id",
        )
        seller_name = st.text_input(
            "Seller Name *",
            value=seller.get("name", ""),
            key=f"{key_prefix}_seller_name",
        )

    with s2:
        seller_email = st.text_input(
            "Seller Email *",
            value=seller.get("email", ""),
            key=f"{key_prefix}_seller_email",
        )
        seller_website = st.text_input(
            "Seller Website *",
            value=seller.get("website", ""),
            key=f"{key_prefix}_seller_website",
        )

    tags = [x.strip() for x in tags_text.split(",") if x.strip()]
    image_urls = [x.strip() for x in image_text.split(",") if x.strip()]

    payload = build_product_payload(
        name=name.strip(),
        sku=sku.strip(),
        description=description.strip(),
        category=category.strip(),
        brand=brand.strip(),
        price=price,
        discount_percent=discount,
        stock=stock,
        is_active=is_active,
        rating=rating,
        tags=tags,
        image_urls=image_urls,
        dimensions={
            "length": length,
            "width": width,
            "height": height,
        },
        seller={
            "seller_id": seller_id.strip(),
            "name": seller_name.strip(),
            "email": seller_email.strip(),
            "website": seller_website.strip(),
        },
        product_id=defaults.get("id"),
        created_at=defaults.get("created_at"),
    )

    return payload


# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
tab_dashboard, tab_create, tab_search, tab_update, tab_delete = st.tabs(
    ["📊 Products", "➕ Create", "🔎 Search by ID", "✏️ Update", "🗑️ Delete"]
)


# ---------------------------------------------------------
# READ / TABLE
# ---------------------------------------------------------
with tab_dashboard:
    st.header("All Products")

    if st.button("🔄 Refresh Products", key="refresh_products"):
        st.rerun()

    # Streamlit pagination is 0-based, FastAPI page is 1-based
    page = st.session_state.get("product_pagination", 1)

    products, total = get_products(page)

    if products:
        df = pd.json_normalize(products)

        preferred_columns = [
            "id", "sku", "name", "category", "brand",
            "price", "discount_percent", "final_price",
            "stock", "is_active", "rating", "volume"
        ]

        available_columns = [
            column for column in preferred_columns
            if column in df.columns
        ]

        remaining_columns = [
            column for column in df.columns
            if column not in available_columns
        ]

        df = df[available_columns + remaining_columns]

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(f"{len(products)} product(s) displayed.")

    total_pages = max(1, (total + 49) // 50)

    # Center Pagination
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.pagination(
            num_pages=total_pages,
            max_visible_pages=7,
            key="product_pagination",
        )




# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
with tab_create:
    st.header("Create Product")
    st.info("Fields marked with * are required by your current Product schema.")

    with st.form("create_product_form"):
        payload = product_form(key_prefix="create")

        submitted = st.form_submit_button(
            "➕ Create Product",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        response = api_request(
            "POST",
            "/products",
            json=payload,
        )

        if response is not None and response.status_code in (200, 201):
            st.success("Product created successfully!")
            st.json(response.json())
        elif response is not None:
            show_api_error(response)


# ---------------------------------------------------------
# SEARCH BY ID
# ---------------------------------------------------------
with tab_search:
    st.header("Search Product by ID")

    search_id = st.text_input(
        "Product UUID",
        placeholder="Enter product ID",
        key="search_id",
    )

    if st.button("🔎 Search", type="primary", key="search_button"):
        if not search_id.strip():
            st.warning("Please enter a product ID.")
        else:
            product = get_product(search_id.strip())

            if product:
                st.success("Product found!")

                # Show a compact table.
                search_df = pd.json_normalize([product])
                st.dataframe(
                    search_df,
                    use_container_width=True,
                    hide_index=True,
                )

                with st.expander("View complete JSON"):
                    st.json(product)


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------
with tab_update:
    st.header("Update Product")

    update_id = st.text_input(
        "Product UUID",
        placeholder="Enter product ID to load",
        key="update_id",
    )

    if st.button("📥 Load Product", key="load_update"):
        if not update_id.strip():
            st.warning("Please enter a product ID.")
        else:
            product = get_product(update_id.strip())

            if product:
                st.session_state["product_to_update"] = product
                st.success("Product loaded. Edit the fields below.")
            else:
                st.session_state.pop("product_to_update", None)

    product_to_update = st.session_state.get("product_to_update")

    if product_to_update:
        with st.form("update_product_form"):
            payload = product_form(
                defaults=product_to_update,
                key_prefix="update",
            )

            submitted = st.form_submit_button(
                "💾 Update Product",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            response = api_request(
                "PUT",
                f"/products/{product_to_update['id']}",
                json=payload,
            )

            if response is not None and response.ok:
                st.success("Product updated successfully!")
                st.session_state.pop("product_to_update", None)
                st.rerun()
            elif response is not None:
                show_api_error(response)


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------
with tab_delete:
    st.header("Delete Product")

    delete_id = st.text_input(
        "Product UUID",
        placeholder="Enter product ID to delete",
        key="delete_id",
    )

    confirm_delete = st.checkbox(
        "I understand that this product will be permanently deleted.",
        key="confirm_delete",
    )

    if st.button(
        "🗑️ Delete Product",
        type="primary",
        disabled=not confirm_delete,
        key="delete_button",
    ):
        if not delete_id.strip():
            st.warning("Please enter a product ID.")
        else:
            response = api_request(
                "DELETE",
                f"/del_product/{delete_id.strip()}",
            )

            if response is not None and response.ok:
                st.success("Product deleted successfully!")
            elif response is not None:
                show_api_error(response)
                