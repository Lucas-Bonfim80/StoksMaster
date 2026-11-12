import csv
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.product import Product
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
        writer.writerow(["Gerado em ", generated_at.strftime("%d/%m/%Y %H:%M:%S %z")])
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
    return db_product


def update_product(db: Session, store_id: int, product_id: int, product: ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id, Product.store_id == store_id).first()
    if db_product is None:
        return None

    db_product.name = product.name
    db_product.image = product.image
    db_product.category = product.category
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, store_id: int, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id, Product.store_id == store_id).first()
    if db_product is None:
        return False

    db.delete(db_product)
    db.commit()
    return True
