from fastapi import FastAPI
from app.database import engine, Base
from app.routers import groups, expenses, settle

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Expense Splitter API",
    description="A Splitwise-like backend API to split group expenses and settle debts with minimum transactions.",
    version="1.0.0"
)

app.include_router(groups.router, prefix="/groups", tags=["Groups"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
app.include_router(settle.router, prefix="/settle", tags=["Settle"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to Smart Expense Splitter API 💸", "docs": "/docs"}
