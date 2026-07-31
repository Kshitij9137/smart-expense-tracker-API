from fastapi import FastAPI, HTTPException, status
from typing import Optional, List

from src.models import Expense, ExpenseCreate
from src.storage import storage
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A simple REST API to add, view, filter, total, and delete personal expenses.",
    version="1.0.0",
)



@app.get("/", include_in_schema=False)
def root():
    """Redirect the root URL to the interactive API docs."""
    return RedirectResponse(url="/docs")


@app.post("/expenses", response_model=Expense, status_code=status.HTTP_201_CREATED)
def add_expense(expense: ExpenseCreate):
    """Add a new expense."""
    return storage.add(expense)


@app.get("/expenses", response_model=List[Expense])
def list_expenses(category: Optional[str] = None):
    """
    List all expenses.
    Optional query param: /expenses?category=Food
    """
    return storage.get_all(category=category)


@app.get("/expenses/search", response_model=List[Expense])
def search_expenses(q: str):
    """
    Search expenses by keyword in the title.
    Example: /expenses/search?q=coffee
    """
    return storage.search(q)


@app.get("/expenses/total")
def get_total(category: Optional[str] = None):
    """
    Get total expenses.
    - /expenses/total          -> overall total
    - /expenses/total?category=Food -> total for that category only
    """
    total = storage.get_total(category=category)
    if category:
        return {"category": category, "total": total}
    return {"total": total}


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: str):
    """Delete an expense by id."""
    deleted = storage.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return None