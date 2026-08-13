from pydantic import BaseModel, Field, AnyUrl, field_validator, model_validator, computed_field
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


    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value: str):
        if "-" not in value:
            raise ValueError("Value must contain '-'")

        last = value.split("-")[-1]
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("Last digit must be 3 like '-123'.")

        return value


    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock 0, then is_active must be False.")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have rating.")

        return model


    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - (self.discount_percent / 100)), 2)