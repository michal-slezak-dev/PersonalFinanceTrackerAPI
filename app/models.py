# define database models (tables)

from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Date, Integer, Boolean
from sqlalchemy.orm import relationship
from .database import (Base)
from sqlalchemy import func

class User(Base):
    __tablename__ =  "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
    is_admin = Column(Boolean, default=False)

    expenses = relationship("Expense", back_populates="user")

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, unique=True, nullable=False)

    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    user_id = Column(ForeignKey("user.id"))
    category_id = Column(ForeignKey("category.id"))

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

