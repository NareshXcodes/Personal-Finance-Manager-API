from pydantic import BaseModel , ConfigDict
from typing import Literal , Optional
from datetime import datetime
from decimal import Decimal

class ExpenseCreate(BaseModel):
    title : str
    amount : Decimal
    category : Literal["food","transport","utilities","entertainment","health","education","shopping"]
    budget_id : Optional[int] = None

class ExpenseUpdate(BaseModel):
    title : Optional[str] = None
    amount : Optional[Decimal] = None
    category : Optional[Literal["food","transport","utilities","entertainment","health","education","shopping"]] = None
    budget_id : Optional[int] = None


class ExpenseResponse(ExpenseCreate):
    id : int
    created_at : datetime
    owner_id : int
    model_config = ConfigDict(from_attributes = True)