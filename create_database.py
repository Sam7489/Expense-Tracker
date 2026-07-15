import sqlite3
connection = sqlite3.connect("./instance/expenses.db")

print("Database Created successfully")

connection.close()
