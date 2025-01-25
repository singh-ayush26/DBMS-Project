import sqlite3
from tkinter import *
from tkinter import messagebox

# Database setup
def init_db():
    conn = sqlite3.connect("banking.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Branch (
        BranchID INTEGER PRIMARY KEY AUTOINCREMENT,
        BranchName TEXT,
        Address TEXT,
        City TEXT,
        State TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT,
        LastName TEXT,
        Address TEXT,
        PhoneNumber TEXT,
        Email TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Account (
        AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
        CustomerID INTEGER,
        BranchID INTEGER,
        AccountType TEXT,
        Balance REAL DEFAULT 0,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (BranchID) REFERENCES Branch(BranchID)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS [Transaction] (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        AccountID INTEGER,
        TransactionDate TEXT,
        Amount REAL,
        TransactionType TEXT,
        FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
    )
    """)
    conn.commit()
    conn.close()

# GUI application
class BankingApp:
    def __init__(self, root):  # Corrected constructor name here
        self.root = root
        self.root.title("Banking System")
        self.root.geometry("600x400")
        
        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Banking System", font=("Arial", 20)).pack(pady=20)
        Button(self.root, text="Customer Management", width=30, command=self.customer_management).pack(pady=10)
        Button(self.root, text="Account Management", width=30, command=self.account_management).pack(pady=10)
        Button(self.root, text="Transaction Management", width=30, command=self.transaction_management).pack(pady=10)
        Button(self.root, text="Exit", width=30, command=self.root.quit).pack(pady=10)

    def customer_management(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Customer Management", font=("Arial", 20)).pack(pady=20)
        Button(self.root, text="Add Customer", width=30, command=self.add_customer).pack(pady=10)
        Button(self.root, text="View Customers", width=30, command=self.view_customers).pack(pady=10)
        Button(self.root, text="Back to Main Menu", width=30, command=self.main_menu).pack(pady=10)

    def add_customer(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Add Customer", font=("Arial", 20)).pack(pady=20)
        Label(self.root, text="First Name").pack()
        first_name = Entry(self.root)
        first_name.pack()
        Label(self.root, text="Last Name").pack()
        last_name = Entry(self.root)
        last_name.pack()
        Label(self.root, text="Address").pack()
        address = Entry(self.root)
        address.pack()
        Label(self.root, text="Phone Number").pack()
        phone = Entry(self.root)
        phone.pack()
        Label(self.root, text="Email").pack()
        email = Entry(self.root)
        email.pack()

        def save_customer():
            conn = sqlite3.connect("banking.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Customer (FirstName, LastName, Address, PhoneNumber, Email) VALUES (?, ?, ?, ?, ?)",
                           (first_name.get(), last_name.get(), address.get(), phone.get(), email.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer added successfully!")
            self.customer_management()

        Button(self.root, text="Save", command=save_customer).pack(pady=10)
        Button(self.root, text="Back", command=self.customer_management).pack(pady=10)

    def view_customers(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("banking.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customer")
        customers = cursor.fetchall()
        conn.close()

        Label(self.root, text="Customer List", font=("Arial", 20)).pack(pady=20)

        if customers:
            for customer in customers:
                Label(self.root, text=f"ID: {customer[0]} | Name: {customer[1]} {customer[2]} | Phone: {customer[4]} | Email: {customer[5]}").pack()
        else:
            Label(self.root, text="No customers found.").pack(pady=10)

        Button(self.root, text="Back", command=self.customer_management).pack(pady=20)

    def account_management(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Account Management", font=("Arial", 20)).pack(pady=20)
        Button(self.root, text="Create Account", width=30, command=self.create_account).pack(pady=10)
        Button(self.root, text="View Accounts", width=30, command=self.view_accounts).pack(pady=10)
        Button(self.root, text="Back to Main Menu", width=30, command=self.main_menu).pack(pady=10)

    def create_account(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Create Account", font=("Arial", 20)).pack(pady=20)
        Label(self.root, text="Customer ID").pack()
        customer_id = Entry(self.root)
        customer_id.pack()
        Label(self.root, text="Branch ID").pack()
        branch_id = Entry(self.root)
        branch_id.pack()
        Label(self.root, text="Account Type (Savings/Checking)").pack()
        account_type = Entry(self.root)
        account_type.pack()

        def save_account():
            conn = sqlite3.connect("banking.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Account (CustomerID, BranchID, AccountType) VALUES (?, ?, ?)",
                           (customer_id.get(), branch_id.get(), account_type.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Account created successfully!")
            self.account_management()

        Button(self.root, text="Save", command=save_account).pack(pady=10)
        Button(self.root, text="Back", command=self.account_management).pack(pady=10)

    def transaction_management(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Transaction Management", font=("Arial", 20)).pack(pady=20)
        Button(self.root, text="Deposit", width=30, command=self.deposit).pack(pady=10)
        Button(self.root, text="Withdraw", width=30, command=self.withdraw).pack(pady=10)
        Button(self.root, text="Back to Main Menu", width=30, command=self.main_menu).pack(pady=10)

    def deposit(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Deposit", font=("Arial", 20)).pack(pady=20)
        Label(self.root, text="Account ID").pack()
        account_id = Entry(self.root)
        account_id.pack()
        Label(self.root, text="Amount").pack()
        amount = Entry(self.root)
        amount.pack()

        def process_deposit():
            conn = sqlite3.connect("banking.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE Account SET Balance = Balance + ? WHERE AccountID = ?", (amount.get(), account_id.get()))
            cursor.execute("INSERT INTO [Transaction] (AccountID, TransactionDate, Amount, TransactionType) VALUES (?, datetime('now'), ?, 'Deposit')", (account_id.get(), amount.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Deposit successful!")
            self.transaction_management()

        Button(self.root, text="Submit", command=process_deposit).pack(pady=10)
        Button(self.root, text="Back", command=self.transaction_management).pack(pady=10)

    def withdraw(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(self.root, text="Withdraw", font=("Arial", 20)).pack(pady=20)
        Label(self.root, text="Account ID").pack()
        account_id = Entry(self.root)
        account_id.pack()
        Label(self.root, text="Amount").pack()
        amount = Entry(self.root)
        amount.pack()

        def process_withdrawal():
            conn = sqlite3.connect("banking.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Balance FROM Account WHERE AccountID = ?", (account_id.get(),))
            balance = cursor.fetchone()
            if balance and float(balance[0]) >= float(amount.get()):
                cursor.execute("UPDATE Account SET Balance = Balance - ? WHERE AccountID = ?", (amount.get(), account_id.get()))
                cursor.execute("INSERT INTO [Transaction] (AccountID, TransactionDate, Amount, TransactionType) VALUES (?, datetime('now'), ?, 'Withdrawal')", (account_id.get(), amount.get()))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Withdrawal successful!")
            else:
                messagebox.showerror("Error", "Insufficient balance!")
            self.transaction_management()

        Button(self.root, text="Submit", command=process_withdrawal).pack(pady=10)
        Button(self.root, text="Back", command=self.transaction_management).pack(pady=10)

# Initialize the database and run the application
if __name__ == "__main__":
    init_db()
    root = Tk()
    app = BankingApp(root)
    root.mainloop()
