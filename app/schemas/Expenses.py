from pydantic import BaseModel , ConfigDict
from typing import Literal , Optional
from datetime import datetime


class ExpenseCreate(BaseModel):
    title : str
    amount : float
    category : Literal["food","transport","utilities","entertainment","health"]
    budget_id : Optional[int] = None

class ExpenseUpdate(BaseModel):
    title : Optional[str] = None
    amount : Optional[float] = None
    category : Optional[Literal["food","transport","utilities","entertainment","health"]] = None
    budget_id : Optional[int] = None


class ExpenseResponse(ExpenseCreate):
    id : int
    created_at : datetime
    model_config = ConfigDict(from_attributes = True)