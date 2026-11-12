from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.product import ProductCreate, ProductOut
from app.security import get_current_user
from app.services.product_service import (
    create_low_stock_report,
    create_product,
    delete_product,
    get_low_stock_products,
    get_products_by_store,
    update_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_products_by_store(db, current_user.store_id)


@router.get("/low-stock", response_model=list[ProductOut])
def list_low_stock_products(
    threshold: int = Query(default=5, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_low_stock_products(db, current_user.store_id, threshold)


@router.post("/low-stock/report")
def create_low_stock_report_route(
    threshold: int = Query(default=5, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report_path = create_low_stock_report(db, current_user.store_id, threshold)
    return FileResponse(
        report_path,
        media_type="text/csv",
        filename=report_path.name,
    )


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
