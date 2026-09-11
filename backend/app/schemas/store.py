from pydantic import BaseModel, Field


class StoreCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)


class StoreOut(StoreCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
