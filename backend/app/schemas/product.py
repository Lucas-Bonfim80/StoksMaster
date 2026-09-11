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
