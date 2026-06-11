from fastapi import APIRouter , HTTPException , status , Response , Depends
from typing import Optional
from app.models.expense import Expense
from app.models.user import User
from app.schemas.Expenses import ExpenseCreate , ExpenseUpdate , ExpenseResponse
from app.db.deps import SessionDep
from datetime import datetime
from app.utils.oauth2 import get_current_user


router = APIRouter(prefix="/expenses",tags=["Expenses"])

@router.get("/",response_model=list[ExpenseResponse])
def get_expense(db: SessionDep , category: Optional[str] = None,current_user: User = Depends(get_current_user)):
    if category :
        all_expense = db.query(Expense).filter(
            Expense.category == category,
            Expense.owner_id == current_user.id
        ).all()
        return all_expense
    else :
        all_expense = db.query(Expense).filter(Expense.owner_id == current_user.id).all()
        return all_expense


@router.get("/report/monthly")
def last_month_report(db:SessionDep , current_user: User = Depends(get_current_user)):

    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    if now.month == 12:
        end_of_month = datetime(now.year + 1, 1, 1)
    else:
        end_of_month = datetime(now.year, now.month + 1, 1)

    expenses = db.query(Expense).filter(Expense.owner_id == current_user.id, Expense.created_at >= start_of_month , Expense.created_at < end_of_month).all()

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


@router.get("/{id}",response_model=ExpenseResponse)
def get_expense_by_id(id:int,db: SessionDep,current_user: User = Depends(get_current_user)):
    expense = db.query(Expense).filter(Expense.id == id,Expense.owner_id == current_user.id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense Not Found")
    return expense

@router.post("/" , status_code = status.HTTP_201_CREATED )
def create_expense(db:SessionDep, new_expense : ExpenseCreate, current_user: User = Depends(get_current_user)):
    new_expense = Expense(**new_expense.model_dump(), owner_id = current_user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.delete("/{id}" , status_code =status.HTTP_204_NO_CONTENT)
def delete_expense(id:int,db:SessionDep, current_user: User = Depends(get_current_user)):
    deleted_expense = db.query(Expense).filter(Expense.id == id).first()

    if deleted_expense == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense Not Found!!")

    if deleted_expense.owner_id != current_user.id:
        raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )

    db.delete(deleted_expense)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_expense(id:int, db:SessionDep ,update_expense : ExpenseUpdate ,current_user: User = Depends(get_current_user)):
    query = db.query(Expense).filter(Expense.id == id)
    updated_expense = query.first()

    if updated_expense == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail="Expense Not Found!!")

    if updated_expense.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    query.update(update_expense.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(updated_expense)
    return updated_expense
