from unittest.mock import patch
import pytest
from Wallet import *



@pytest.fixture
def tmp_path(tmp_path):
    return tmp_path

def test_expense_attributes(tmp_path):
    expense = Expense("Groceries", 50.0, "Food")
    assert expense.name == "Groceries"
    assert expense.amount == 50.0
    assert expense.category == "Food"

def test_repr(capsys):
    expense = Expense("books", 34, "work")
    assert repr(expense) == "books - $34.00 - work"
    expense = Expense("dresses", 100, "clothing")
    assert repr(expense) == "dresses - $100.00 - clothing"

def test_get_budget_positive():
    with patch('builtins.input', return_value='1000'):
        assert get_budget() == 1000

def test_get_budget_zero():
    with patch('builtins.input', return_value='0'):
        assert get_budget() == 0

def test_read_expenses_file_not_found(tmp_path):
    file_path = tmp_path / "nonexistent_file.csv"
    expenses = read_expenses(file_path)
    assert expenses == []

def test_calculate_summary_empty_expenses(capsys):
    expenses = []
    budget = 1000.0

    total_spent, amount_by_category, budget_left = calculate_summary(expenses, budget)

    assert total_spent == 0.0
    assert amount_by_category == {}
    assert budget_left == 1000.0

def test_calculate_summary_filled_with_expenses(capsys):
    expenses = [
        Expense("Expense 1", 100.0, "Category 1"),
        Expense("Expense 2", 200.0, "Category 1"),
        Expense("Expense 3", 400.0, "Category 2")
    ]
    budget = 1000.0

    total_spent, amount_by_category, budget_left = calculate_summary(expenses, budget)

    assert total_spent == 700.0
    assert amount_by_category == {"Category 1": 300.0, "Category 2": 400.0}
    assert budget_left == 300.0

def test_delete_expense_with_empty_expenses(capsys):
    expenses = []
    with patch("builtins.input", return_value="Expense"):
        delete_expense(expenses)

    captured = capsys.readouterr()
    assert "No expenses to delete." in captured.out



