from pydantic import BaseModel, Field
from datetime import date as date_type
import uuid


class ExpenseCreate(BaseModel):
    """
    This is what the CLIENT sends us when creating an expense.
    No 'id' field here — we generate that ourselves, the client shouldn't set it.
    """
    title: str = Field(..., min_length=1, description="Short description of the expense")
    amount: float = Field(..., gt=0, description="Amount spent, must be greater than 0")
    category: str = Field(..., min_length=1, description="e.g. Food, Travel, Utilities")
    date: date_type = Field(..., description="Date the expense occurred, format YYYY-MM-DD")


class Expense(ExpenseCreate):
    """
    This is what we STORE and RETURN to the client.
    It extends ExpenseCreate by adding the server-generated id.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))