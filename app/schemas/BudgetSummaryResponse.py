from pydantic import BaseModel , ConfigDict
from typing import Literal
from decimal import Decimal


class BudgetSummaryResponse(BaseModel):
    budget_name : str
    category : Literal["food","transport","utilities","entertainment","health"]
    monthly_limit : Decimal
    total_spent : Decimal
    remaining : Decimal
    percent_used : Decimal
    model_config = ConfigDict(from_attributes=True)