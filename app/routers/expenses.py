from datetime import date
import string

from sqlalchemy import Date, String
from ..schemas import schemas
from .. import models, oauth2
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/expenses",
    tags=['expenses']
)

@router.get("/", response_model=List[schemas.Expense])
def get_expenses(db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    expenses = db.query(models.Expense).all()
    return expenses


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Expense)
def create_expense(expense: schemas.Expensecreate, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):

    new_expense = models.Expense(owner_id=current_user.id,
        **expense.dict()
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/{created_at}", response_model=List[schemas.Expense])
def get_expense(created_at: str, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    expenses = db.query(models.Expense).filter(models.Expense.created_at == created_at).filter(models.Expense.owner_id == current_user.id).all()

    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="expense with that date does not exist")

    return expenses
