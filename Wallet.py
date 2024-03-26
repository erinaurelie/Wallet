import csv
import datetime
import time
import smtplib  # Simple Mail Transfer Protocol
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from tabulate import tabulate
from confidential import password
from fpdf import FPDF, XPos, YPos
import fpdf
import socket
import validators
import art

#requirement.txt
# pip install tabulate
# pip install fpdf
# pip install validators
# pip install art

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
            print("===============================\nSENDING EXPENSE REPORT TO EMAIL\n===============================")
            to_email = input("Enter recipient email address: ").strip()
            while True:
                try:
                    if validators.email(to_email.lower()):
                        break
                    else:
                        print("Invalid Email Address. Please Try Again.")
                except validators.ValidationError as e:
                    print(e.message)
                to_email = input("Enter recipient email address: ").strip()
            subject = "Expense Summary"
            body = "Please find attached the summary of expenses."
            attachment_path = "expense_summary.pdf"
            from_email = "walletapp.contact@gmail.com"
            email_password = password
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            summarize_and_send_expense(
                budget,
                from_email,
                email_password,
                to_email,
                attachment_path,
                smtp_server,
                smtp_port,
            )
            print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-__-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")
        elif option == "6":
            view_all_expenses(file_path="expense.csv")
        elif option == "7":
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
    print("5. Send expense report to email")
    print("6. View Expenses")
    print("7. Exit")


def generate_pdf_summary(summary, pdf_file_path) -> None:
    """
    Generate a PDF summary with the provided summary content and save it to the specified file path.

    :param summary (str): The content of the summary to be included in the PDF.
    :param pdf_file_path (str): The file path where the generated PDF will be saved
    return: None
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    summary_bytes = summary.encode('latin-1', 'ignore').decode('latin-1')

    # Add text to the PDF
    pdf.cell(0, 10, txt=f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d')}", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Here's the breakdown of your expenses for the current month:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=summary_bytes)

    pdf.output(pdf_file_path)




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
            writer.writerow([expense.name, expense.amount, expense.category])
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


def summarize_expenses(budget, file_path="expense.csv", print_summary=True, print_pdf=False) -> str:
    """
    Summarize expenses based on a budget and an optional CSV file path.

    :param: budget (float): The allocated budget for expenses.
    :param: file_path (str, optional): The path to the CSV file containing the expenses. Defaults to "expense.csv".
    :param: print_summary (bool, optional): Whether to print the summary text to the console. Defaults to True.
    :param: print_pdf (bool, optional): Whether to generate a PDF summary. Defaults to False.
    :return: The summary text if `print_summary` is False, otherwise an empty string.
    :rtype: str

    """
    expenses = read_expenses(file_path)
    total_spent, amount_by_category, budget_left = calculate_summary(expenses, budget)
    summary = generate_summary_text(total_spent, amount_by_category, budget, budget_left)

    if print_summary:
        print(summary)

    if print_pdf:
        pdf_file_path = "report.pdf"
        generate_pdf_summary(summary, pdf_file_path)

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
        if expense.name == name_to_delete:
            expenses.remove(expense)
            deleted = True

    if deleted:
        print(f"'{name_to_delete}' deleted successfully.")
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


def send_email(to_email, subject, body, attachment_path, from_email, email_password, 
               smtp_server="smtp.gmail.com", smtp_port=587) -> None:
    """
    Sends an email with an attachment using the SMTP protocol.

    :param: to_email (str): The email address of the recipient.
    :param: subject (str): The subject of the email.
    :param: body (str): The body or content of the email.
    :param: attachment_path (str): The file path to the attachment.
    :param: from_email (str): The email address of the sender.
    :param: email_password (str): The password for the sender's email account.
    :param: smtp_server (str, optional): The SMTP server address. Defaults to "smtp.gmail.com".
    :param: smtp_port (int, optional): The SMTP server port. Defaults to 587.

    """
    try:
        with open(attachment_path, "rb") as attachment_file:
            attachment_data = attachment_file.read()

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment_data)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment_path)}",
        )
        msg.attach(part)

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, email_password)
            server.send_message(msg)
        print("Email sent successfully.")

    except FileNotFoundError:
        print(f"Attachment file '{attachment_path}' not found.")
    except (smtplib.SMTPConnectError, socket.gaierror) as e:
        print(
            f"Failed to connect to the SMTP server. Please check your internet connection."
        )
    except smtplib.SMTPException as e:
        print(f"An error occurred while sending email: {e}")


def summarize_and_send_expense(budget, from_email, email_password, attachment_path, to_email,
                               smtp_server="smtp_server", smtp_port=587, file_path="expense.csv") -> str:
    
    """
    Summarize expenses, generate a PDF summary, and send it via email.

    :param budget (float): The budget amount.
    :param from_email (str): The email address of the sender.
    :param email_password (str): The password for the sender's email account.
    :param attachment_path (str): The file path to the attachment.
    :param to_email: (str) The email address of the recipient.
    :param smtp_server (str, optional): The SMTP server address. Defaults to "smtp_server".
    :param smtp_port (int, optional): The SMTP server port. Defaults to 587.
    :param file_path (str, optional): The path to the CSV file containing the expenses. Defaults to "expense.csv".

     :return: The summary of expenses.
     rtype: str

    """

    summary = summarize_expenses(
        budget, file_path=file_path, print_summary=False, print_pdf=False
    )
    amount_by_category = summary[1] if isinstance(summary, tuple) and len(summary) > 1 else {}
    summary_file_path = "expense_summary.pdf"
    generate_pdf_summary(summary, summary_file_path)

    subject = "Expense Summary"
    body = "Please find attached the summary of expenses."
    send_email(
        to_email,
        subject,
        body,
        summary_file_path,
        from_email,
        email_password,
        smtp_server,
        smtp_port,
    )
    return summary


if __name__ == "__main__":
    main()
