from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.store import Store
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserProfile, UserRegister
from app.security import create_access_token, get_current_user, get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_store = db.query(Store).filter(Store.name == user.store_name).first()
    if existing_store is None:
        store = Store(name=user.store_name)
        db.add(store)
        db.commit()
        db.refresh(store)
    else:
        store = existing_store

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        store_id=store.id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(new_user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(db_user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login-form")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(db_user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email,
        "store_name": current_user.store.name,
    }
