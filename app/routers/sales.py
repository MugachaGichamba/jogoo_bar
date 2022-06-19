from datetime import date
import string

from sqlalchemy import Date, String
from ..schemas import schemas
from .. import models, oauth2
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/sales",
    tags=['sales']
)

@router.get("/", response_model=List[schemas.Sale])
def get_sales(db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    sales = db.query(models.Sale).all()
    # sales = db.query(models.Sale).filter(models.Stock.owner_id == current_user.id).all()
    return sales

@router.get("/sum", response_model=List[schemas.Sale])
def get_sales(db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    sales = db.query(models.Sale).all()
    # sales = db.query(models.Sale).filter(models.Stock.owner_id == current_user.id).all()
    qry = db.query(func.sum(models.Sale.total).label("total_sales"),
                     )
    print(qry.first()[0])
    # qry = qry.group_by(Score.name)
    # for _res in qry.all():
    #     print _res
    return sales


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):

    new_sale = models.Sale(owner_id=current_user.id,
        **sale.dict()
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale
 

@router.get("/{created_at}", response_model=List[schemas.Sale])
def get_sale(created_at: str, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    sales = db.query(models.Sale).filter(models.Sale.created_at == created_at).filter(models.Sale.owner_id == current_user.id).all()

    if not sales:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="sale with that date does not exist")

    return sales
