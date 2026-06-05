from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Numeric, DateTime, func, ForeignKey
from app.db.database import Base
from decimal import Decimal
from app.models.budget import CategoryEnum
from sqlalchemy import Enum as SQLEnum

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(SQLEnum(CategoryEnum), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    budget_id: Mapped[Optional[int]] = mapped_column(ForeignKey("budgets.id", ondelete="SET NULL"), nullable=True)

    budget: Mapped[Optional["Budget"]] = relationship("Budget", back_populates="expenses")