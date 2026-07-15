import sqlite3

conn = sqlite3.connect("./instance/expenses.db")

cur = conn.cursor()

data = """CREATE TABLE IF NOT EXISTS EXPENSES
(   
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description VARCHAR(255) NOT NULL,
    amount REAL NOT NULL,
    category VARCHAR(50) NOT NULL,
    date TEXT NOT NULL DEFAULT CURRENT_DATE 
)
"""


cur.execute(data)
conn.commit()
conn.close()
