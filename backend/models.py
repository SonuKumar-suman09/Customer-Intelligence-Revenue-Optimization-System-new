from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(50), default="user")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, unique=True, index=True)
    age = Column(Integer)
    gender = Column(String(50))
    location = Column(String(100))
    annual_income = Column(Float)
    churned = Column(Integer)
    
    # ML Features
    recency = Column(Float, default=0.0)
    frequency = Column(Float, default=0.0)
    monetary = Column(Float, default=0.0)
    segment = Column(Integer, default=-1)
    predicted_clv = Column(Float, default=0.0)
    churn_probability = Column(Float, default=0.0)

    transactions = relationship("Transaction", back_populates="customer")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    transaction_date = Column(DateTime, default=datetime.datetime.utcnow)
    category = Column(String(100))
    amount = Column(Float)

    customer = relationship("Customer", back_populates="transactions")
