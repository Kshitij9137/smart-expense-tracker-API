from typing import List, Optional
from src.models import Expense, ExpenseCreate


class ExpenseStorage:
    """
    In-memory storage for expenses.
    Data lives only as long as the server process is running —
    it resets every time you restart the server. This is fine per
    the assignment spec ("in memory or local JSON file, no DB required").
    """

    def __init__(self):
        self._expenses: List[Expense] = []

    def add(self, expense_data: ExpenseCreate) -> Expense:
        expense = Expense(**expense_data.model_dump())
        self._expenses.append(expense)
        return expense

    def get_all(self, category: Optional[str] = None) -> List[Expense]:
        if category is None:
            return self._expenses
        # case-insensitive match so "food" and "Food" both work
        return [e for e in self._expenses if e.category.lower() == category.lower()]

    def get_total(self, category: Optional[str] = None) -> float:
        matching = self.get_all(category)
        return round(sum(e.amount for e in matching), 2)

    def delete(self, expense_id: str) -> bool:
        original_length = len(self._expenses)
        self._expenses = [e for e in self._expenses if e.id != expense_id]
        return len(self._expenses) < original_length


# A single shared instance used by the whole app.
# This is a simple form of dependency — good enough for this assignment's scope.
storage = ExpenseStorage()