from fastapi import FastAPI
from app.routers import expenses , budgets

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "Welcome to Personal Finance Manager App"}

@app.get("/reports/monthly")
def get_monthly_report():
    pass

app.include_router(expenses.router , prefix="/expenses")
app.include_router(budgets.router , prefix="/budgets")