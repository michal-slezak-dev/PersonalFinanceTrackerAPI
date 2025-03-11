# define Pydantic schemas (data validation)

from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class CategoryCreate(BaseModel):
    category_name: str


class CategoryResponse(BaseModel):
    id: int
    category_name: str

    class Config: # returns data from the DB
        from_attributes = True

class ExpenseCreate(BaseModel):
    amount: float
    description: Optional[str]
    date: date
    category_id: int
    user_id: int


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    date: date
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    category: CategoryResponse

    class Config: # returns data from the DB
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: Optional[datetime]
    expenses: List["ExpenseResponse"]

    class Config: # returns data from the DB
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str
