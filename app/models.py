from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Many-to-many: expense participants
expense_participants = Table(
    "expense_participants",
    Base.metadata,
    Column("expense_id", Integer, ForeignKey("expenses.id")),
    Column("member_id", Integer, ForeignKey("members.id")),
)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")

    members = relationship("Member", back_populates="group", cascade="all, delete")
    expenses = relationship("Expense", back_populates="group", cascade="all, delete")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="members")
    paid_expenses = relationship("Expense", back_populates="paid_by_member")
    participated_expenses = relationship(
        "Expense", secondary=expense_participants, back_populates="participants"
    )


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    paid_by = Column(Integer, ForeignKey("members.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="expenses")
    paid_by_member = relationship("Member", back_populates="paid_expenses")
    participants = relationship(
        "Member", secondary=expense_participants, back_populates="participated_expenses"
    )
