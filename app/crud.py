# database operations (CRUD functions)

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import User, Expense, Category
from schemas import UserCreate, ExpenseCreate, CategoryCreate
from security import get_password_hash


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=str(user.email),
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Error when creating the user: {e}")

    return db_user

def update_user(db: Session, user_id: int, new_data: dict):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    if "password" in new_data.keys():
        new_data["password"] = get_password_hash(new_data["password"])

    for key, value in new_data.items():
        setattr(db_user, key, value)

    try:
        db.commit()
        db.refresh(db_user)
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Error when updating user: {e}")

    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user:
        try:
            db.delete(db_user)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise SQLAlchemyError(f"Error when deleting user: {e}")

    return False

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(
        category_name=category.category_name
    )

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Error when deleting category: {e}")

    return db_category

def get_category_by_id(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if not db_category:
        return None

    return db_category

def get_all_categories(db: Session):
    return db.query(Category).all()

def delete_category(db: Session, category_id):
    db_category = db.query(Category).filter(Category.id == category_id).first()

    if db_category:
        try:
            db.delete(db_category)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise SQLAlchemyError(f"Error when deleting category: {e}")
    return False

def create_expense(db: Session, expense: ExpenseCreate):
    db_expense = Expense(
        amount=expense.amount,
        description=expense.description,
        user_id=expense.user_id,
        category_id=expense.category_id
    )

    try:
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Error when creating expense: {e}")

    return db_expense

def get_expense_by_id(db: Session, expense_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not db_expense:
        return None

    return db_expense

def get_all_expenses(db: Session) -> list:
    return db.query(Expense).all()

def update_expense(db: Session, expense_id: int, new_data: dict):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not db_expense:
        return None



    for key, value in new_data.items():
        setattr(db_expense, key, value)

    try:
        db.commit()
        db.refresh(db_expense)
    except SQLAlchemyError as e:
        db.rollback()
        raise SQLAlchemyError(f"Error when updating expense: {e}")

    return db_expense

def delete_expense(db: Session, expense_id):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if db_expense:
        try:
            db.delete(db_expense)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise SQLAlchemyError(f"Error when deleting expense: {e}")
    return False
