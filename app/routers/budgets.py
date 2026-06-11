from fastapi import APIRouter , HTTPException , status , Response , Depends
from typing import List
from app.schemas.Budgets import BudgetCreate , BudgetUpdate , BudgetResponse
from app.schemas.BudgetSummaryResponse import BudgetSummaryResponse
from app.models.budget import Budget
from app.models.expense import Expense
from app.models.user import User
from app.db.deps import SessionDep
from decimal import Decimal
from app.schemas.Expenses import ExpenseResponse
from app.utils.oauth2 import get_current_user

router = APIRouter(prefix="/budgets",tags=["Budgets"])


@router.get("/", response_model=List[BudgetResponse])
def get_all_budget(db: SessionDep, current_user: User = Depends(get_current_user)):
    all_budgets = db.query(Budget).filter(Budget.owner_id == current_user.id).all()
    return all_budgets


@router.get("/{id}", response_model=BudgetResponse)
def get_budget_by_id(id: int, db: SessionDep, current_user: User = Depends(get_current_user)):
    budget = db.query(Budget).filter(Budget.id == id , Budget.owner_id == current_user.id).first()
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget


@router.post("/", status_code = status.HTTP_201_CREATED )
def create_budget(new_budget : BudgetCreate , db:SessionDep , current_user: User = Depends(get_current_user)):
    #new_budget = Budget(name = new_budget.name , category = new_budget.category , monthly_limit = new_budget.monthly_limit)
    new_budget =  Budget(**new_budget.model_dump(),owner_id=current_user.id)
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget
    
    

@router.delete("/{id}", status_code =status.HTTP_204_NO_CONTENT)
def delete_budget(id:int,db:SessionDep,current_user: User = Depends(get_current_user) ):
    
    deleted_budget = db.query(Budget).filter(Budget.id == id).first()

    if deleted_budget == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail="Budget not found"
        )

    if deleted_budget.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    db.delete(deleted_budget)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_budget(id:int,update_budget : BudgetUpdate,db:SessionDep , current_user: User = Depends(get_current_user)):
    
    query = db.query(Budget).filter(Budget.id == id)
    updated_budget = query.first()

    if updated_budget == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

    if updated_budget.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    query.update(update_budget.model_dump(exclude_unset=True) , synchronize_session=False)
    db.commit()
    db.refresh(updated_budget)
    return {"data": updated_budget}

@router.get("/{id}/summary", response_model=BudgetSummaryResponse)
def get_budget_summary(id: int, db: SessionDep, current_user: User = Depends(get_current_user)):
    budget = db.query(Budget).filter(Budget.id == id).first()

    if budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    if budget.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    

    total_spent = sum((expense.amount for expense in budget.expenses), Decimal("0"))
    print("total_spent:", total_spent)

    remaining = budget.monthly_limit - total_spent

    if budget.monthly_limit == Decimal("0"):
        percent_used = Decimal("0")
    else:
        percent_used = (total_spent / budget.monthly_limit) * Decimal("100")

    return BudgetSummaryResponse(
        budget_name=budget.name,
        category=budget.category,
        monthly_limit=budget.monthly_limit,
        total_spent=total_spent,
        remaining=remaining,
        percent_used=percent_used,
    )

@router.get("/{id}/expenses" , response_model= List[ExpenseResponse])
def get_budget_expenses(id:int , db: SessionDep,current_user: User = Depends(get_current_user)):
    # query = db.query(Budget).filter(Budget.id == id).first()
    # expenses = query.expenses # One to Many Relationship SQLAlchemy model 
    budget = db.query(Budget).filter(Budget.id == id).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )

    if budget.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    expenses = db.query(Expense).filter(Expense.budget_id == id,Expense.owner_id == current_user.id).all()

    return expenses