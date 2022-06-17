
from email.policy import default
from enum import unique
import imp
from xmlrpc.client import Boolean, boolean
from .database import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, nullable=False)
    stock_name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    buying_price = Column(Integer, nullable=False)
    selling_price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(Date, nullable=False,
    server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Integer, server_default='0', nullable=False)
    created_at = Column(Date, nullable=False, server_default=text('now()'))
  

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    created_at = Column(Date, nullable=False,
    server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False
    )
    stock_id = Column(Integer, ForeignKey(
        "stocks.id", ondelete="CASCADE"), nullable=False
    )
    stock = relationship("Stock")


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    created_at = Column(Date, nullable=False,
    server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False
    )
    stock_id = Column(Integer, ForeignKey(
        "stocks.id", ondelete="CASCADE"), nullable=False
    )
    stock = relationship("Stock")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, nullable=False)
    expense_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(Date, nullable=False,
    server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False
    )




