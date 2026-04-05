from pydantic import BaseModel
from typing import List, Optional


# --- Group Schemas ---
class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class GroupResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True


# --- Member Schemas ---
class MemberCreate(BaseModel):
    name: str
    group_id: int

class MemberResponse(BaseModel):
    id: int
    name: str
    group_id: int

    class Config:
        from_attributes = True


# --- Expense Schemas ---
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    paid_by: int           # member_id who paid
    group_id: int
    split_among: List[int]  # list of member_ids to split among

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    paid_by: int
    group_id: int

    class Config:
        from_attributes = True


# --- Settlement Schemas ---
class Transaction(BaseModel):
    from_member: str
    to_member: str
    amount: float

class SettlementResponse(BaseModel):
    group: str
    total_expenses: float
    transactions: List[Transaction]
