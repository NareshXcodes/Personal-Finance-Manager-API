from fastapi import APIRouter , HTTPException , status , Response
from typing import Optional

router = APIRouter(prefix="/expenses",tags=["Expenses"])

@router.get("/")
def get_expense(category: Optional[str] = None):
    if category :
        pass
    else :
        pass

@router.get("/{id}")
def get_expense_by_id(id:int):
    pass

@router.post("/" , status_code = status.HTTP_201_CREATED )
def create_expense():
    pass

@router.delete("/{id}" , status_code =status.HTTP_204_NO_CONTENT)
def delete_expense(id:int):
    pass

@router.put("/{id}")
def update_expense(id:int):
    pass



#Budgets
@router2.get("/")
def get_all_budget():
    pass

@router2.get("/{id}")
def get_budget_by_id(id:int):
    pass

@router2.post("/", status_code = status.HTTP_201_CREATED )
def create_budget():
    pass

@router2.delete("/{id}", status_code =status.HTTP_204_NO_CONTENT)
def delete_budget(id:int):
    pass

@router2.put("/{id}")
def update_budget(id:int):
    pass

@router2.get("/{id}/summary")
def get_budget_summary(id:int):
    pass

@router2.get("/{id}/expenses")
def get_budget_expenses(id:int):
    pass