import csv
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.schemas.product import ProductCreate


REPORTS_DIR = Path(__file__).resolve().parents[2] / "data" / "stock_reports"


def get_products_by_store(db: Session, store_id: int):
    return db.query(Product).filter(Product.store_id == store_id).order_by(Product.id.desc()).all()


def get_low_stock_products(db: Session, store_id: int, threshold: int = 5):
    return (
        db.query(Product)
        .filter(Product.store_id == store_id, Product.quantity <= threshold)
        .order_by(Product.quantity.asc(), Product.name.asc())
        .all()
    )


def create_low_stock_report(db: Session, store_id: int, threshold: int) -> Path:
    products = get_low_stock_products(db, store_id, threshold)
    generated_at = datetime.now().astimezone()
    timestamp = generated_at.strftime("%Y%m%d_%H%M%S_%f")
    report_path = REPORTS_DIR / f"estoque_baixo_loja_{store_id}_{timestamp}.csv"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with report_path.open("w", newline="", encoding="utf-8-sig") as report_file:
        writer = csv.writer(report_file)
        writer.writerow(["Relatorio de produtos com estoque baixo"])
        writer.writerow(["Gerado em '", generated_at.strftime("%d/%m/%Y %H:%M:%S %z")])
        writer.writerow(["Limite de estoque", threshold])
        writer.writerow([])
        writer.writerow(["Produto", "Quantidade"])
        for product in products:
            name = product.name
            if name.lstrip().startswith(("=", "+", "-", "@")):
                name = f"'{name}"
            writer.writerow([name, product.quantity])

    return report_path


def create_product(db: Session, store_id: int, product: ProductCreate):
    db_product = Product(
        name=product.name,
        image=product.image,
        category=product.category,
        price=product.price,
        quantity=product.quantity,
        store_id=store_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    if db_product.quantity > 0:
        db.add(StockMovement(
            product_id=db_product.id,
            product_name=db_product.name,
            store_id=store_id,
            movement_type="entrada",
            quantity_delta=db_product.quantity,
            quantity_before=0,
            quantity_after=db_product.quantity,
            reason="Cadastro inicial do produto",
        ))
        db.commit()
    return db_product


def update_product(db: Session, store_id: int, product_id: int, product: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id, Product.store_id == store_id).first()
    if db_product is None:
        return None

    db_product.name = product.name
    db_product.image = product.image
    db_product.category = product.category
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)
    return db_product


def register_stock_movement(
    db: Session,
    store_id: int,
    product_id: int,
    movement_type: str,
    quantity: int,
    reason: str,
):
    db_product = db.query(Product).filter(Product.id == product_id, Product.store_id == store_id).first()
    if db_product is None:
        return None

    quantity_before = db_product.quantity
    if movement_type == "entrada":
        quantity_delta = quantity
        quantity_after = quantity_before + quantity
    elif movement_type == "saida":
        if quantity > quantity_before:
            return False
        quantity_delta = -quantity
        quantity_after = quantity_before - quantity
    else:
        quantity_delta = quantity - quantity_before
        quantity_after = quantity

    db_product.quantity = quantity_after
    db.add(StockMovement(
        product_id=db_product.id,
        product_name=db_product.name,
        store_id=store_id,
        movement_type=movement_type,
        quantity_delta=quantity_delta,
        quantity_before=quantity_before,
        quantity_after=quantity_after,
        reason=reason,
    ))
    db.commit()
    db.refresh(db_product)
    return db_product


def get_stock_movements(db: Session, store_id: int, product_id: int | None = None, limit: int = 100):
    query = db.query(StockMovement).filter(StockMovement.store_id == store_id)
    if product_id is not None:
        query = query.filter(StockMovement.product_id == product_id)
    return query.order_by(StockMovement.created_at.desc(), StockMovement.id.desc()).limit(limit).all()


def delete_product(db: Session, store_id: int, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id, Product.store_id == store_id).first()
    if db_product is None:
        return False

    db.delete(db_product)
    db.commit()
    return True
