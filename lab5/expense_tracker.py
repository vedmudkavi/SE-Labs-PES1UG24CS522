"""Track monthly expenses and provide report and statement helpers."""

import hmac
import os
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path


class ExpenseTracker:
    """Keep the expenses and budget for one tracker."""

    def __init__(self, monthly_budget=20000):
        self.expenses = []
        self.monthly_budget = monthly_budget

    def add_expense(self, amount, category="Misc", note=""):
        """Add a positive expense and return whether it was accepted."""
        if amount <= 0:
            print("Ignoring invalid amount", amount)
            return False
        self.expenses.append({"amount": amount, "category": category,
                              "note": note,
                              "time": datetime.now().isoformat()})
        return True

    def total_by_category(self):
        """Return the total spending in each category."""
        totals = {}
        for expense in self.expenses:
            category = expense["category"]
            totals[category] = totals.get(category, 0) + expense["amount"]
        return totals

    def set_budget(self, new_budget):
        """Update the monthly budget."""
        self.monthly_budget = new_budget

    def remaining_budget(self):
        """Return the budget minus recorded spending."""
        spent = sum(expense["amount"] for expense in self.expenses)
        return self.monthly_budget - spent

    def biggest_expense(self):
        """Return the largest expense, or None for an empty ledger."""
        return max(self.expenses, key=lambda expense: expense["amount"],
                   default=None)

    def print_ledger(self):
        """Print each expense with its entry number."""
        for index, expense in enumerate(self.expenses, start=1):
            print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check the configured password; reject access when it is unset."""
    expected = os.environ.get("BANK_SYNC_PASSWORD")
    return bool(expected) and hmac.compare_digest(
        password.encode("utf-8"), expected.encode("utf-8")
    )


def export_report():
    """Create an empty report file and return its path for the caller."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as report:
        return report.name


def open_statement(path):
    """Open an existing local file as a URI in the default browser."""
    statement = Path(path).resolve(strict=True)
    if not statement.is_file():
        raise ValueError("Statement must be a file")
    return webbrowser.open(statement.as_uri())


def main():
    """Run the example expense ledger."""
    tracker = ExpenseTracker()
    print("Biggest expense before any entries:", tracker.biggest_expense())
    tracker.add_expense(450, "Food", "Lunch with team")
    tracker.add_expense(1200, "Travel", "Cab to airport")
    tracker.add_expense(-50, "Food")
    tracker.add_expense(300, "Food", "Groceries")
    tracker.add_expense(999, "Bills", "Internet")
    tracker.set_budget(5000)
    tracker.print_ledger()
    print("Totals:", tracker.total_by_category())
    print("Remaining budget:", tracker.remaining_budget())  # after set_budget
    print("Biggest expense:", tracker.biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print("Summary:", len(tracker.expenses),
          "expenses recorded against a budget of", tracker.monthly_budget)


if __name__ == "__main__":
    main()
