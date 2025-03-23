# entry point of the API
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .crud import create_category
from .schemas import CategoryCreate

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/v1/categories")
async def create_categories(category_data: CategoryCreate, db: db_dependency):
        return create_category(db, category_data)
