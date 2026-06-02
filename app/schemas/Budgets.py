from pydantic import BaseModel , ConfigDict
from typing import Literal , Optional
from datetime import datetime


class BudgetCreate(BaseModel):
    id : int
    name : str
    category : Literal["food","transport","utilities","entertainment","health"]
    monthly_limit : float
    created_at : datetime

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[Literal["food", "transport", "utilities", "entertainment", "health"]] = None
    monthly_limit: Optional[float] = None

class BudgetResponse(BudgetCreate):
    id : int
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)