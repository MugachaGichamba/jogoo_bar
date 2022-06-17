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
    prefix="/purchases",
    tags=['purchases']
)

@router.get("/", response_model=List[schemas.Purchase])
def get_purchases(db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    purchases = db.query(models.Purchase).all()
    return purchases


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Purchase)
def create_purchases(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):

    new_purchase = models.Purchase(owner_id=current_user.id,
        **purchase.dict()
    )
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    return new_purchase

@router.get("/{created_at}", response_model=List[schemas.Purchase])
def get_purchase(created_at: str, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    purchases = db.query(models.Purchase).filter(models.Purchase.created_at == created_at).filter(models.Purchase.owner_id == current_user.id).all()
    if not purchases:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="purchase with that date does not exist")

    return purchases

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db),
# current_user : int = Depends (oauth2.get_current_user)):
#     stock = db.query(models.Stock).filter(models.Stock.id == id)
#     if stock.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"stock with id: {id} does not exist")
    
#     stock.delete(synchronize_session=False)
#     db.commit()

# @router.put("/{id}", response_model=schemas.Stock)
# def update_stock(id: int, updated_stock: schemas.StockCreate, db: Session = Depends(get_db),
# current_user : int = Depends (oauth2.get_current_user)):

#     stock_query = db.query(models.Stock).filter(models.Stock.id == id)
#     stock = stock_query.first()

#     if stock == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"stock with id: {id} does not exist")

#     stock_query.update(updated_stock.dict(), synchronize_session=False)

#     db.commit()


#     return stock_query.first

