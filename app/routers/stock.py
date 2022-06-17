from ..schemas import schemas
from .. import models, oauth2
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/stocks",
    tags=['stocks']
)

@router.get("/", response_model=List[schemas.Stock])
def get_stocks(db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    stocks = db.query(models.Stock).all()
    return stocks


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Stock)
def create_stocks(stock: schemas.StockCreate, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):

    print(current_user.phone_number)
    new_stock = models.Stock(
        **stock.dict()
    )
    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)
    return new_stock

@router.get("/{id}", response_model=schemas.Stock)
def get_stock(id: int, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    stock = db.query(models.Stock).filter(models.Stock.id == id).first()
   
    if not stock:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"stock with id: {id} does not exist")

    return stock

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):
    stock = db.query(models.Stock).filter(models.Stock.id == id)
    if stock.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"stock with id: {id} does not exist")

    if current_user.is_admin != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="you are not authorized to perform action")

    stock.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Stock)
def update_stock(id: int, updated_stock: schemas.StockCreate, db: Session = Depends(get_db),
current_user : int = Depends (oauth2.get_current_user)):

    stock_query = db.query(models.Stock).filter(models.Stock.id == id)
    stock = stock_query.first()
    if stock == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"stock with id: {id} does not exist")
    if current_user.is_admin != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="you are not authorized to perform action")

    stock_query.update(updated_stock.dict(), synchronize_session=False)

    db.commit()


    return stock_query.first()

