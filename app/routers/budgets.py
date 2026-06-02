from fastapi import APIRouter , HTTPException , status , Response
from typing import Optional


router = APIRouter(prefix="/budgets",tags=["Budgets"])


@router.get("/")
def get_all_budget():
    pass

@router.get("/{id}")
def get_budget_by_id(id:int):
    pass

@router.post("/", status_code = status.HTTP_201_CREATED )
def create_budget():
    pass

@router.delete("/{id}", status_code =status.HTTP_204_NO_CONTENT)
def delete_budget(id:int):
    pass

@router.put("/{id}")
def update_budget(id:int):
    pass

@router.get("/{id}/summary")
def get_budget_summary(id:int):
    pass

@router.get("/{id}/expenses")
def get_budget_expenses(id:int):
    pass