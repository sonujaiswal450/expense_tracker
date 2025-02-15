import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Database Setup
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        category TEXT,
                        amount REAL,
                        description TEXT)''')
    conn.commit()
    conn.close()

# Add Expense
def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = category_var.get()
    amount = amount_entry.get()
    description = desc_entry.get()
    
    if not amount or not category:
        messagebox.showerror("Input Error", "Amount and Category are required!")
        return
    
    try:
        amount = float(amount)
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                       (date, category, amount, description))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Expense added successfully!")
        amount_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)
        show_expenses()
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")

# Show Expenses
def show_expenses():
    for row in tree.get_children():
        tree.delete(row)
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, category, amount, description FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    for row in rows:
        tree.insert("", tk.END, values=row)

# Expense Analysis
def analyze_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        messagebox.showinfo("No Data", "No expenses recorded yet!")
        return
    
    categories, amounts = zip(*data)
    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%.1f%%", startangle=140)
    plt.title("Expense Breakdown by Category")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x500")

# Input Fields
category_var = tk.StringVar()
category_label = tk.Label(root, text="Category:")
category_label.pack()
category_menu = ttk.Combobox(root, textvariable=category_var, values=["Food", "Transport", "Shopping", "Bills", "Other"])
category_menu.pack()
amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack()
desc_label = tk.Label(root, text="Description:")
desc_label.pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

# Buttons
add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.pack()
show_button = tk.Button(root, text="Show Expenses", command=show_expenses)
show_button.pack()
analyze_button = tk.Button(root, text="Analyze Expenses", command=analyze_expenses)

# Expense Table
columns = ("Date", "Category", "Amount", "Description")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)  # Ensure columns have width

tree.pack()

analyze_button.pack()

# Initialize Database
init_db()
root.mainloop()
