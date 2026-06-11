from pydantic import BaseModel , ConfigDict
from typing import Literal , Optional
from datetime import datetime
from decimal import Decimal


class BudgetCreate(BaseModel):
    name : str
    category : Literal["food","transport","utilities","entertainment","health","education","shopping"]
    monthly_limit : Decimal

class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[Literal["food", "transport", "utilities", "entertainment", "health","education","shopping"]] = None
    monthly_limit: Optional[Decimal] = None

class BudgetResponse(BudgetCreate):
    id : int
    created_at : datetime
    owner_id : int
    model_config = ConfigDict(from_attributes=True)