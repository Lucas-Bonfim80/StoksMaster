from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.store import Store
from app.models.user import User
from app.schemas.store import StoreCreate, StoreOut
from app.security import get_current_user

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/", response_model=list[StoreOut])
def list_stores(db: Session = Depends(get_db)):
    return db.query(Store).order_by(Store.id.desc()).all()


@router.post("/", response_model=StoreOut, status_code=status.HTTP_201_CREATED)
def create_store(store: StoreCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Store).filter(Store.name == store.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Store already exists")

    new_store = Store(name=store.name)
    db.add(new_store)
    db.commit()
    db.refresh(new_store)
    return new_store
