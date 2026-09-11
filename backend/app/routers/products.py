from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductOut
from app.security import get_current_user
from app.services.product_service import create_product, delete_product, get_products_by_store, update_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_products_by_store(db, current_user.store_id)


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product_route(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_product(db, current_user.store_id, product)


@router.put("/{product_id}", response_model=ProductOut)
def update_product_route(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = update_product(db, current_user.store_id, product_id, product)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_route(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_product(db, current_user.store_id, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return None
