import sqlite3


def add_expense(description, amount, category, d):
    conn = sqlite3.connect("./instance/expenses.db")
    cur = conn.cursor()
    t = (description , amount, category, d)

    data_sql = """INSERT INTO EXPENSES 
    (description, amount, category, date)
    VALUES(?,?,?,?)"""

    cur.execute(data_sql , t)
    conn.commit()
    conn.close()

# if __name__ == "__main__":
#     add_expense("Coffee", 30.5, "Food", "2026-07-15")
