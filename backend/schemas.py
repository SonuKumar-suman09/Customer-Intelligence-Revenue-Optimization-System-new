from pydantic import BaseModel
from typing import List, Optional
import datetime

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class CustomerBase(BaseModel):
    customer_id: int
    age: int
    gender: str
    location: str
    annual_income: float
    churned: int
    recency: float = 0.0
    frequency: float = 0.0
    monetary: float = 0.0
    segment: int = -1
    predicted_clv: float = 0.0
    churn_probability: float = 0.0

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    transaction_id: int
    customer_id: int
    transaction_date: datetime.datetime
    category: str
    amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True
