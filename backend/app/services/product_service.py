from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def get_products_by_store(db: Session, store_id: int):
    return db.query(Product).filter(Product.store_id == store_id).order_by(Product.id.desc()).all()


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
