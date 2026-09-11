from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routers.auth import router as auth_router
from app.routers.products import router as products_router
from app.routers.stores import router as stores_router

init_db()

app = FastAPI(title="StoksMaster API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(stores_router)
app.include_router(products_router)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "StoksMaster backend is running"}


@app.get("/")
def read_root():
    return {"message": "Welcome to StoksMaster API"}
