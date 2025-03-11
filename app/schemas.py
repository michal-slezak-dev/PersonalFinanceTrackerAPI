# define Pydantic schemas (data validation)

from pydantic import BaseModel, field_validator, EmailStr
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

    @field_validator("amount")
    def validate_amount(cls, value):
        if value < 0:
            raise ValueError("amount cannot be negative")
        return value

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
    email: EmailStr
    password: str

    @field_validator("username")
    def validate_username(cls, value):
        if not value.isalnum():
            raise ValueError("username must be alphanumeric")
        return value


    @field_validator("password")
    def validate_password_length(cls, value):
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")

        if any(c.isspace() for c in value):
            raise ValueError("password must not contain spaces")
        return value


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

    @field_validator("username")
    def validate_username(cls, value):
        if not value.isalnum():
            raise ValueError("username must be alphanumeric")
        return value
