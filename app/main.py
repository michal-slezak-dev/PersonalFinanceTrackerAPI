# entry point of the API
import jwt
from jwt import PyJWTError
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated, Dict
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from .crud import create_category, create_user, update_user, delete_user, get_all_categories, delete_category, \
    create_expense, get_all_expenses, update_expense, delete_expense
from .models import User, Category, Expense
from .schemas import CategoryCreate, UserResponse, UserCreate, UserUpdate, Token, ExpenseCreate, ExpenseUpdate
from .core.security import verify_password, create_access_token, verify_token, SECRET_KEY, ALGORITHM

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")
db_dependency = Annotated[Session, Depends(get_db)]


def get_current_user(db: db_dependency, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate given credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user

user_dependency = Annotated[User, Depends(get_current_user)]


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.post("/v1/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: db_dependency):
    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )


    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return create_user(db, user_data)


@app.post("/v1/auth/token", response_model=Token)
async def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )

    access_token = create_access_token(data={"sub": user.username, "id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/v1/users/me")
async def get_authenticated_user_info(db: db_dependency, current_user: user_dependency):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

    return {"user": current_user}


@app.patch("/v1/users/me", response_model=UserResponse)
async def update_user_data(user_update: UserUpdate, db: db_dependency, current_user: user_dependency):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_update_data: Dict = {}
    if user_update.first_name and user_update.first_name is not None:
        user_update_data["first_name"] = user_update.first_name

    if user_update.last_name and user_update.last_name is not None:
        user_update_data["last_name"] = user_update.last_name

    if user_update.password and user_update.password is not None:
        user_update_data["password"] = user_update.password

    user_update_data["updated_at"] = func.now()


    return update_user(db, current_user.id, user_update_data)


@app.delete("/v1/users/me", response_model=UserResponse)
async def remove_user(db: db_dependency, current_user: user_dependency):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return delete_user(db, current_user.id)


@app.get("/v1/categories")
async def list_all_categories(db: db_dependency):
    return get_all_categories(db)


@app.post("/v1/categories")
async def create_new_category(category_data: CategoryCreate, db: db_dependency, current_user: user_dependency):
    """Only admins can create new categories (for now)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to create categories"
        )
    return create_category(db, category_data)


@app.delete("/v1/categories/{category_id}")
async def remove_category(category_id: int, db: db_dependency, current_user: user_dependency):
    """Only admins can delete categories"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete categories"
        )

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return delete_category(db, category_id)


@app.post("/v1/expenses")
async def create_new_expense(expense_data: ExpenseCreate, db: db_dependency, current_user: user_dependency):
    existing_expense = db.query(Expense).filter(Expense.description == expense_data.description).first()

    if existing_expense:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expense already exists"
        )
    return create_expense(db, current_user.id, expense_data)


@app.get("/v1/expenses")
async def list_all_expenses(db: db_dependency, current_user: user_dependency):
    return get_all_expenses(db, current_user.id)


@app.patch("/v1/expenses/{expense_id}")
async def update_expense_data(expense_id: int, expense_update: ExpenseUpdate, db: db_dependency, current_user: user_dependency):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    expense_update_data: Dict = {}
    if expense_update.amount and expense_update.amount is not None:
        expense_update_data["amount"] = expense_update.amount

    if expense_update.description and expense_update.description is not None:
        expense_update_data["description"] = expense_update.description

    if expense_update.date and expense_update.date is not None:
        expense_update_data["date"] = expense_update.date

    if expense_update.category_id and expense_update.category_id is not None:
        expense_update_data["category_id"] = expense_update.category_id

    return update_expense(db, expense_id, expense_update_data)


@app.delete("/v1/expenses/{expense_id}")
async def remove_expense(expense_id: int, db: db_dependency, current_user: user_dependency):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )

    return delete_expense(db, expense_id)
