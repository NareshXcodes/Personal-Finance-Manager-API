from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, DateTime, func
from app.db.database import Base
from decimal import Decimal
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum


class CategoryEnum(str, PyEnum):
    food = "food"
    transport = "transport"
    utilities = "utilities"
    entertainment = "entertainment"
    health = "health"
    education = "education"
    shopping = "shopping"

class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(SQLEnum(CategoryEnum), nullable=False)
    monthly_limit: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    expenses: Mapped[List["Expense"]] = relationship("Expense", back_populates="budget")
    