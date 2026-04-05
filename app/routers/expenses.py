from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.ExpenseResponse, summary="Add an expense")
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    # Validate group
    group = db.query(models.Group).filter(models.Group.id == expense.group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Validate payer
    payer = db.query(models.Member).filter(models.Member.id == expense.paid_by).first()
    if not payer:
        raise HTTPException(status_code=404, detail="Paying member not found")

    # Validate participants
    participants = db.query(models.Member).filter(models.Member.id.in_(expense.split_among)).all()
    if len(participants) != len(expense.split_among):
        raise HTTPException(status_code=404, detail="One or more participants not found")

    new_expense = models.Expense(
        description=expense.description,
        amount=expense.amount,
        paid_by=expense.paid_by,
        group_id=expense.group_id,
        participants=participants
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/group/{group_id}", response_model=list[schemas.ExpenseResponse], summary="List expenses of a group")
def list_expenses(group_id: int, db: Session = Depends(get_db)):
    return db.query(models.Expense).filter(models.Expense.group_id == group_id).all()


@router.delete("/{expense_id}", summary="Delete an expense")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}
