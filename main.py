from fastapi import FastAPI
from app.routers import expenses , budgets
from app.db.database import Base, engine
from app.db.deps import SessionDep
from app.models.budget import Budget
from app.models.expense import Expense


Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Welcome to Personal Finance Manager App"}

@app.get("/reports/monthly")
def get_monthly_report():
    return {"message" : "May Monthly Report is On the Way !!"}

app.include_router(expenses.router , prefix="/expenses")
app.include_router(budgets.router , prefix="/budgets")