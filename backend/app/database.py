from urllib.parse import urlparse

import pymysql
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database_if_needed():
    parsed = urlparse(DATABASE_URL)
    db_name = parsed.path.lstrip("/") or "stoksMaster"
    conn = pymysql.connect(
        host=parsed.hostname,
        user=parsed.username,
        password=parsed.password,
        port=parsed.port or 3306,
        autocommit=True,
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
    finally:
        conn.close()


def init_db():
    create_database_if_needed()
    from app.models import Product, Store, User  # noqa: F401

    Base.metadata.create_all(bind=engine)
    if "category" not in {column["name"] for column in inspect(engine).get_columns("products")}:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE products ADD COLUMN category VARCHAR(80) NOT NULL DEFAULT 'Outros'"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
