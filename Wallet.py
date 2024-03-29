import csv
from tabulate import tabulate
import art
import time
import pyttsx3


class Expense:
    """
    A class representing an expense.

    Attributes:
        name (str): The name or description of the expense.
        category (str): The category to which the expense belongs.
        amount (float): The amount of the expense.

    Methods:
        __repr__(): Returns a string representation of the Expense object.
    """
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = float(amount)
        self.category = category
    
        
    def __repr__(self):
        return f"{self.name} - ${self.amount:,.2f} - {self.category}"


def main() -> None:
    """
    Entry point of the script.

    This function executes the main logic of the script or program.
    """
    print(art.text2art('WELCOME TO WALLET!'))
    text_to_speech()
    budget = get_budget()
    expenses = []

    while True:
        print_menu()
        option = input(
            "Enter the number corresponding to the desired operation: "
        ).strip()

        if option == "1":
            print("===============================\nADDING AN EXPENSE\n===============================")
            expense = get_expense()
            expenses.append(expense)
            print("Expense added successfully.")
        elif option == "2":
            save_expenses(expenses)
            print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
        elif option == "3":
            summarize_expenses(budget)
        elif option == "4":
            print("===============================\nDELETING AN EXPENSE\n===============================")
            delete_expense(expenses)
        elif option == "5":
            view_all_expenses(file_path="expense.csv")
        elif option == "6":
            print("Exiting...")
            time.sleep(2)
            print()
            print("See you next time in Wallet!")
            break
        else:
            print("Invalid option. Please try again.")


def print_menu() -> None:
    """
    Prints the main menu for the Wallet application.
    """
    print("\nAvailable Operations:")
    print("1. Add Expense")
    print("2. Save Expenses")
    print("3. Summarize Expenses")
    print("4. Delete an Expense")
    print("5. View Expenses")
    print("6. Exit")


def text_to_speech() -> None:
    """
    This function converts the given text into speech using the pyttsx3 library.
    """
    engine = pyttsx3.init()
    engine.say("WELCOME TO WALLET!")
    engine.runAndWait()


def get_budget() -> float:
    """
    Prompts the user to enter their monthly budget and returns it as a float.
    
    type: int
    return: The user's monthly budget as a float value with 2 decimal places.
    rtype: float
    raises: ValueError: If the input is not a positive number.

    """
    while True:
        try:
            budget = float(input("Enter your monthly budget: "))
            if budget < 0:
                raise ValueError
            else:
                print(f"Your monthly budget is ${budget:,.2f}")
                return budget
        except ValueError:
            print(f"Invalid input. Positive numbers only.")


def get_expense() -> Expense:
    """
    Prompts the user to enter details of an expense and returns an Expense object.

    return: Expense: An Expense object representing the entered expense.
    raises: ValueError: If the user enters an invalid expense amount or no expense name.
    """
    while True:
        if expense_name := input("Enter Expense name: ").strip():
            break
        else:
            print("Invalid input. Expense name cannot be blank.")

    while True:
        try:
            expense_amount = float(input("Enter Expense amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid expense amount.")

    expense_categories = [
        "Food",
        "Transportation",
        "Housing",
        "Entertainment",
        "Shopping",
        "Health and Fitness",
        "Personal Care",
        "Work/Education",
        "Travel",
        "Custom Category",
    ]
    while True:
        print("Select a category:")
        for i, category in enumerate(expense_categories, start=1):
            print(f"{i}. {category}")
        try:
            category_index = int(
                input(
                    f"Enter the number corresponding to the category (1-{len(expense_categories)}): "
                )
           )
            if 1 <= category_index <= len(expense_categories):
                if category_index == len(expense_categories) :
                    new_category_name = input("Enter the new category name: ")
                    expense_categories.append(new_category_name)
                    return Expense(expense_name, expense_amount, new_category_name,)
                else: return Expense(
                    expense_name, expense_amount, expense_categories[category_index - 1],
                )
            else:
                print("Invalid category number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def save_expenses(expenses, file_path="expense.csv") -> None:
    """
    Saves a list of expenses to a csv file.
    
    :param expenses (list): A list of Expense objects to be saved.
    :param file_path (str, optional): The file path to save the CSV file. Defaults to "expense.csv".
    """
    print("Saving expenses...")
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Expense Name", "Amount", "Category"])
        for expense in expenses:
            writer.writerow([expense.name.capitalize(), expense.amount, expense.category])
    time.sleep(2)
    print("Expenses saved successfully.")


def read_expenses(file_path) -> list:
    """
    Read expenses from a CSV file and return a list of Expense objects.

    :param file_path (str): The path to the CSV file containing the expenses.
    :return: A list of Expense objects representing the expenses. (list)
    :rtype: list
    :raises FileNotFoundError: If the specified file_path does not exist.
    """
    expenses = []
    try:
        with open(file_path, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(Expense(row["Expense Name"], float(row["Amount"]), row["Category"]))
    except FileNotFoundError:
        pass
    return expenses


def calculate_summary(expenses, budget) -> tuple:
    """
    Calculate a summary of expenses based on a list of Expense objects and a budget.

    :param: expenses (list): A list of Expense objects representing the expenses.
    :param: budget (float): The allocated budget for expenses.
    :return: A tuple containing the following elements:
            - total_spent (float): The total amount spent on expenses.
            - amount_by_category (dict): A dictionary mapping each expense category to the total amount spent in that category.
            - budget_left (float): The remaining budget after subtracting the total expenses.
    :rtype: tuple

    """
    total_spent = sum(expense.amount for expense in expenses)

    amount_by_category = {}
    for expense in expenses:
        amount_by_category[expense.category] = (
            amount_by_category.get(expense.category, 0) + expense.amount
        )

    budget_left = budget - total_spent

    return total_spent, amount_by_category, budget_left


def generate_summary_text(total_spent, amount_by_category, budget, budget_left) -> str:
    """
    Generate a textual summary of expenses.

    :param: total_spent (float): The total amount spent on expenses.
    :param: amount_by_category (dict): A dictionary mapping each expense category to the total amount spent in that category.
    :param: budget (float): The allocated budget for expenses.
    :param: budget_left (float): The remaining budget after subtracting the total expenses.
    :return: A formatted summary of expenses.
    :rtype: str
    """
    summary = """
        *******************************************
        *** Expense Summary for the Current Month ***
        *******************************************
        """
    summary += "\nExpenses By Category:\n"
    headers = ["Category", "Amount"]
    rows = rows = [[category, f"{amount:,.2f}"] for category, amount in amount_by_category.items()]
    summary += tabulate(rows, headers=headers, tablefmt="heavy_grid") + "\n"
    summary += f"Your Budget was: ${budget:,.2f}\n"
    summary += f"Total spent: ${total_spent:,.2f}\n"
    if budget_left < 0:
        summary += f"You've exceeded your budget by ${abs(budget_left):,.2f}\n"
    else:
        summary += f"Remaining Budget: ${budget_left:,.2f}\n"
    return summary


def summarize_expenses(budget, file_path="expense.csv", print_summary=True) -> str:
    """
    Summarize expenses based on a budget and an optional CSV file path.

    :param: budget (float): The allocated budget for expenses.
    :param: file_path (str, optional): The path to the CSV file containing the expenses. Defaults to "expense.csv".
    :param: print_summary (bool, optional): Whether to print the summary text to the console. Defaults to True.
    :return: The summary text if `print_summary` is False, otherwise an empty string.
    :rtype: str

    """
    expenses = read_expenses(file_path)
    total_spent, amount_by_category, budget_left = calculate_summary(expenses, budget)
    summary = generate_summary_text(total_spent, amount_by_category, budget, budget_left)

    if print_summary:
        print(summary)

    return summary if not print_summary else ""


def delete_expense(expenses) -> None:
    """
    Deletes an expense from a list of expenses.

    :param: expenses (list) A list of Expense objects representing the expenses.
    """
    if not expenses:
        print("No expenses to delete.")
        return

    name_to_delete = input("Enter the name of the expense to delete: ").strip().lower()

    deleted = False
    for expense in expenses[:]:
        if expense.name.lower() == name_to_delete:
            expenses.remove(expense)
            deleted = True

    if deleted:
        print(f"'{name_to_delete.capitalize()}' deleted successfully.")
    else:
        print(f"No expense with the name '{name_to_delete}' found.")


def view_all_expenses(file_path="expense.csv") -> None:
    """
    Display all expenses from a CSV file.

    :param: file_path (str, optional): The path to the CSV file containing the expenses. Defaults to "expense.csv".
    """
    if expenses := read_expenses(file_path):
        expenses_by_category = {}
        for expense in expenses:
            expenses_by_category.setdefault(expense.category, []).append(expense)

        if expenses_by_category:
            print("All Expenses:")
            for category, category_expenses in expenses_by_category.items():
                headers = ["Expense Name", "Amount"]
                rows = [[expense.name, f"${expense.amount}"] for expense in category_expenses]
                print(f"\nCategory: {category}")
                print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No expenses found.")
    else:
        print("No expenses found.")



if __name__ == "__main__":
    main()
