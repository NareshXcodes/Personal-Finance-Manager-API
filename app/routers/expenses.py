from fastapi import APIRouter , HTTPException , status , Response
from typing import Optional
from app.models.expense import Expense
from app.schemas.Expenses import ExpenseCreate , ExpenseUpdate , ExpenseResponse
from app.db.deps import SessionDep
from datetime import datetime

router = APIRouter(prefix="/expenses",tags=["Expenses"])

@router.get("/",response_model=list[ExpenseResponse])
def get_expense(db: SessionDep , category: Optional[str] = None ):
    if category :
        all_expense = db.query(Expense).filter(Expense.category == category).all()
        return all_expense
    else :
        all_expense = db.query(Expense).all()
        return all_expense

@router.get("/{id}",response_model=ExpenseResponse)
def get_expense_by_id(id:int,db: SessionDep):
    expense = db.query(Expense).filter(Expense.id == id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense Not Found")
    return expense

@router.post("/" , status_code = status.HTTP_201_CREATED )
def create_expense(db:SessionDep, new_expense : ExpenseCreate):
    new_expense = Expense(**new_expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.delete("/{id}" , status_code =status.HTTP_204_NO_CONTENT)
def delete_expense(id:int,db:SessionDep):
    deleted_expense = db.query(Expense).filter(Expense.id == id)

    if deleted_expense.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense Not Found!!")

    deleted_expense.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_expense(id:int, db:SessionDep ,update_expense : ExpenseUpdate ):
    query = db.query(Expense).filter(Expense.id == id)
    updated_expense = query.first()

    if updated_expense == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail="Expense Not Found!!")

    query.update(update_expense.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(updated_expense)
    return updated_expense

@router.get("/report/monthly")
def last_month_report(db:SessionDep):
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    if now.month == 12:
        end_of_month = datetime(now.year + 1, 1, 1)
    else:
        end_of_month = datetime(now.year, now.month + 1, 1)

    expenses = db.query(Expense).filter(Expense.created_at >= start_of_month , Expense.created_at < end_of_month).all()

    totals = dict()

    for expense in expenses:
        category = expense.category
        if category not in totals:
            totals[category] = 0

        totals[category] += expense.amount
        
    result = []

    for category , spent in totals.items():
        data = {"category" : category , "total" : spent}
        result.append(data)

    return result