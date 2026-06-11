from fastapi import FastAPI
from app.routers import expenses , budgets , auth
from app.db.database import Base, engine
from app.models.budget import Budget
from app.models.expense import Expense
from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://finsight-personal-finance.vercel.app",
        "https://finsight-personal-finance.vercel.app/"

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message" : "Welcome to Personal Finance Manager App"}


app.include_router(expenses.router)
app.include_router(budgets.router)
app.include_router(auth.router)