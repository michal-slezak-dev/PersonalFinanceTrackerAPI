# database operations (CRUD functions)

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .models import User, Expense, Category
from .schemas import UserCreate, ExpenseCreate, CategoryCreate
from .core.security import get_password_hash
from typing import Type, Dict

def create_item(db: Session, model: Type[User | Expense | Category], item_data: Dict):
    if "password" in item_data.keys() and item_data["password"] is not None:
        item_data["password"] = get_password_hash(item_data["password"])

    db_item = model(**item_data)

    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Error when creating {model.__name__}: {e}")

    return db_item

def update_item(db: Session, model: Type[User | Expense | Category], item_id: int, new_data: Dict):
    db_item = db.query(model).filter(model.id == item_id).first()

    # if not db_item:
    #     return None

    if "password" in new_data.keys() and new_data["password"] is not None:
        new_data["password"] = get_password_hash(new_data["password"])

    for key, value in new_data.items():
        if value is not None:
            setattr(db_item, key, value)

    try:
        db.commit()
        db.refresh(db_item)
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Error when updating {model.__name__}: {e}")

    return db_item

def delete_item(db: Session, model: Type[User | Expense | Category], item_id: int):
    db_item = db.query(model).filter(model.id == item_id).first()

    if db_item:
        try:
            db.delete(db_item)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise SQLAlchemyError(f"Error when deleting {model.__name__}: {e}")

    return False

def get_item_by_id(db: Session, model: Type[Expense | Category], item_id: int):
    db_item = db.query(model).filter(model.id == item_id).first()

    # if not db_item:
    #     return None
    if db_item:
        return db_item

def get_all_items(db: Session, model: Type[Expense | Category]):
    return db.query(model).all()

def create_user(db: Session, user_data: UserCreate):
    return create_item(db, User, user_data.model_dump())

def create_category(db: Session, category_data: CategoryCreate):
    return create_item(db, Category, category_data.model_dump())

def create_expense(db: Session, expense_data: ExpenseCreate):
    return create_item(db, Expense, expense_data.model_dump())

def update_user(db: Session, user_id: int, new_data: Dict):
    return update_item(db, User, user_id, new_data)

# def update_category(db: Session, category_id: int, new_data: Dict):
#     return update_item(db, Category, category_id, new_data)

def update_expense(db: Session, expense_id: int, new_data: Dict):
    return update_item(db, Expense, expense_id, new_data)

def delete_user(db: Session, user_id: int):
    return delete_item(db, User, user_id)

def delete_category(db: Session, category_id):
    return delete_item(db, Category, category_id)

def delete_expense(db: Session, expense_id: int):
    return delete_item(db, Expense, expense_id)

def get_category_by_id(db: Session, category_id: int):
    return get_item_by_id(db, Category, category_id)

def get_expense_by_id(db: Session, expense_id: int):
    return get_item_by_id(db, Expense, expense_id)

def get_all_categories(db: Session):
    return get_all_items(db, Category)

def get_all_expenses(db: Session):
    return get_all_items(db, Expense)
