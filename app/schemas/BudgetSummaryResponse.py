from pydantic import BaseModel , ConfigDict
from typing import Literal


class BudgetSummaryResponse(BaseModel):
    budget_name : str
    category : Literal["food","transport","utilities","entertainment","health"]
    monthly_limit : float
    total_spent : float
    remaining : float
    percent_used : float
    model_config = ConfigDict(from_attributes=True)