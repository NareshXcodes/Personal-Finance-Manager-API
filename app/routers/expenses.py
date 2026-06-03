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
