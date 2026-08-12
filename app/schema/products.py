from pydantic import BaseModel, Field, AnyUrl
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime

class Product(BaseModel):   
    id: UUID
    
    sku: Annotated[str, Field(min_length=14, max_length=14, title="SKU", 
                              description="Stock Keeping Unit", examples=["REAL-135GB-002", "SAMS-225GB-003"])]
    
    name: Annotated[str, Field(min_length=5, max_length=50, title="Product Name", 
                              description="Product name", examples=["Xiaomi Model Pro", "Realme Model Air"])]
    
    description: Annotated[str, Field(max_length=200, description="Description upto 200 character")]

    category: Annotated[str, Field(max_length=50, description="Category", examples=['electronics', 'laptop', 'mobile'])]

    brand: Annotated[str, Field(max_length=50, description="Brand", examples=["Samsung", "Apple", "Xiaomi"]) ]

    price: Annotated[float, Field(gt=0, description="Product price")]

    currency: Literal["INR"] = "INR"

    discount_percent: Annotated[int, Field(ge=0, le=100, description="Discount percentage")]

    stock: Annotated[int, Field(ge=0, strict=True, description="Available stock quantity")]

    is_active: bool = True

    rating: Annotated[float, Field(ge=0, le=5, strict=True, description="Average product rating", examples=[4.5, 3.9])]

    tags: Annotated[Optional[List[str]], Field(default=None, max_length=10, description="Upto 10 Tags")]

    image_urls: Annotated[List[AnyUrl], Field(max_length=1, description="Images URLs")]

    created_at: datetime