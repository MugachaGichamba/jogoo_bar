
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional

class StockBase(BaseModel):
    stock_name: str
    description: str
    quantity : int
    buying_price: float
    selling_price: float


class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id : int
    created_at : date
    class Config:
        orm_mode = True

class PurchaseBase(BaseModel):
    quantity : int
    total: int
    stock_id : int

class Purchase(PurchaseBase):
    id : int
    created_at : date
    owner_id : int
    stock: Stock
    class Config:
        orm_mode = True

class PurchaseCreate(PurchaseBase):
    pass

class ExpenseBase(BaseModel):
    expense_name : str
    price: int

class Expense(ExpenseBase):
    id : int
    created_at : date
    owner_id : int
    class Config:
        orm_mode = True

class Expensecreate(ExpenseBase):
    pass

class SaleBase(BaseModel):
    quantity : int
    total: int
    stock_id : int

class Sale(SaleBase):
    id : int
    created_at : date
    owner_id : int
    stock: Stock
    class Config:
        orm_mode = True

class SaleCreate(SaleBase):
    pass
 
class UserOut(BaseModel):
    id : int
    is_admin : int
    created_at :datetime
    phone_number : str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    phone_number : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None
    