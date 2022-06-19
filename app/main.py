
from fastapi import FastAPI
from . import models
from.database import engine
from passlib.context import CryptContext
from .routers import stock, users, auth, purchase, sales, expenses

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(stock.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(purchase.router)
app.include_router(sales.router)
app.include_router(expenses.router)

@app.get("/")
def root():
    return {"message": "welcome to jogoo bar"}