from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict
from app.database import get_db
from app import models, schemas

router = APIRouter()


def minimize_transactions(balances: dict) -> list:
    """
    Greedy debt minimization algorithm.
    Calculates the minimum number of transactions to settle all debts.
    """
    creditors = []  # people who are owed money (positive balance)
    debtors = []    # people who owe money (negative balance)

    for member, balance in balances.items():
        if balance > 0.01:
            creditors.append([balance, member])
        elif balance < -0.01:
            debtors.append([balance, member])

    creditors.sort(reverse=True)
    debtors.sort()

    transactions = []

    i, j = 0, 0
    while i < len(creditors) and j < len(debtors):
        credit_amount, creditor = creditors[i]
        debt_amount, debtor = debtors[j]

        settle_amount = min(credit_amount, -debt_amount)
        settle_amount = round(settle_amount, 2)

        transactions.append({
            "from": debtor,
            "to": creditor,
            "amount": settle_amount
        })

        creditors[i][0] -= settle_amount
        debtors[j][0] += settle_amount

        if creditors[i][0] < 0.01:
            i += 1
        if debtors[j][0] > -0.01:
            j += 1

    return transactions


@router.get("/{group_id}", response_model=schemas.SettlementResponse, summary="Get minimum transactions to settle group debts")
def settle_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    expenses = db.query(models.Expense).filter(models.Expense.group_id == group_id).all()
    if not expenses:
        return schemas.SettlementResponse(
            group=group.name,
            total_expenses=0,
            transactions=[]
        )

    # Build member id -> name map
    members = db.query(models.Member).filter(models.Member.group_id == group_id).all()
    member_map = {m.id: m.name for m in members}

    # Calculate net balance for each member
    balances = defaultdict(float)

    total_expenses = 0
    for expense in expenses:
        total_expenses += expense.amount
        num_participants = len(expense.participants)
        if num_participants == 0:
            continue

        share = round(expense.amount / num_participants, 2)

        # Payer gets credit
        balances[member_map[expense.paid_by]] += expense.amount

        # Each participant owes their share
        for participant in expense.participants:
            balances[member_map[participant.id]] -= share

    # Run minimization algorithm
    raw_transactions = minimize_transactions(dict(balances))

    transactions = [
        schemas.Transaction(
            from_member=t["from"],
            to_member=t["to"],
            amount=t["amount"]
        )
        for t in raw_transactions
    ]

    return schemas.SettlementResponse(
        group=group.name,
        total_expenses=round(total_expenses, 2),
        transactions=transactions
    )
