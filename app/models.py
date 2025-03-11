# define database models (tables)

from typing import List
from sqlalchemy import Integer, String, Text, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date
from database import Base

class User(Base):
    __tablename__ =  "User"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now)

    expenses: Mapped[List["Expense"]] = relationship("Expense", back_populates="user")

class Category(Base):
    __tablename__ = "Category"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    expenses: Mapped[List["Expense"]] = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = "Expense"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now)

    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("Category.id"))

    user: Mapped[User] = relationship("User", back_populates="expenses")
    category: Mapped[Category] = relationship("Category", back_populates="expenses")
