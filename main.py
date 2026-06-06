from fastapi import FastAPI
from app.routers import expenses , budgets
from app.db.database import Base, engine
from app.db.deps import SessionDep
from app.models.budget import Budget
from app.models.expense import Expense
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://personal-finance-manager-app-one.vercel.app/",
        "https://personal-finance-manager-app-nareshxcodes-projects.vercel.app/"

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