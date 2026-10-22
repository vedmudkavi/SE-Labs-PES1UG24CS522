import hmac
import os
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path

expenses = []
monthly_budget = 20000


def addExpense(amount, category="Misc", note=""):
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append({"amount" : amount, "category": category,
                     "note": note, "time": datetime.now().isoformat()})
    return True


def totalByCategory():
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def setBudget(newBudget):
    global monthly_budget
    monthly_budget = newBudget


def remainingBudget():
    spent = sum(expense["amount"] for expense in expenses)
    return monthly_budget - spent


def biggestExpense():
    try:
        return max(expenses, key=lambda expense: expense["amount"])
    except Exception:
        return None

def printLedger():
    for i in range(len(expenses)):
        print(i + 1, expenses[i]["category"], expenses[i]["amount"])


def checkSyncPassword(password):
    expected = os.environ.get("BANK_SYNC_PASSWORD")
    return bool(expected) and hmac.compare_digest(
        password.encode("utf-8"), expected.encode("utf-8")
    )


def exportReport():
    # Helper kept for the lab: not called by the demo
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as report:
        return report.name


def openStatement(path):
    # Helper kept for the lab: not called by the demo
    statement = Path(path).resolve(strict=True)
    if not statement.is_file():
        raise ValueError("Statement must be a file")
    return webbrowser.open(statement.as_uri())


def main():
    print("Biggest expense before any entries:", biggestExpense())
    addExpense(450, "Food", "Lunch with team")
    addExpense(1200, "Travel", "Cab to airport")
    addExpense(-50, "Food")
    addExpense(300, "Food", "Groceries")
    addExpense(999, "Bills", "Internet")
    setBudget(5000)
    printLedger()
    print("Totals:", totalByCategory())
    print("Remaining budget:", remainingBudget()) # after setBudget
    print("Biggest expense:", biggestExpense()["note"])
    print("Sync password accepted:", checkSyncPassword("guess"))
    print("Summary:", len(expenses), "expenses recorded against a budget of", monthly_budget)


main()
