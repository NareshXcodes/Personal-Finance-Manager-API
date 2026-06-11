from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column , relationship
from sqlalchemy import String, Integer, DateTime, func
from app.db.database import Base
from pydantic import EmailStr
from typing import List , Optional

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True , nullable=False,index=True)
    password: Mapped[EmailStr] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    budgets: Mapped[List["Budget"]] = relationship(
        "Budget", 
        back_populates="user" , 
        cascade="all, delete-orphan"
    )

    expenses: Mapped[List["Expense"]] = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan"
    )