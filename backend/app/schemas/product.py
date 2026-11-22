from datetime import datetime

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    image: str | None = None
    category: str = Field(default="Outros", min_length=1, max_length=80)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class StockMovementCreate(BaseModel):
    movement_type: str = Field(..., pattern="^(entrada|saida|ajuste)$")
    quantity: int = Field(..., ge=0)
    reason: str = Field(..., min_length=1, max_length=200)


class StockMovementOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    movement_type: str
    quantity_delta: int
    quantity_before: int
    quantity_after: int
    reason: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
