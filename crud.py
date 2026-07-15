import sqlite3

DB_NAME = './instance/expenses.db'

def add_expense(description, amount, category, d):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    t = (description , amount, category, d)

    data_sql = """INSERT INTO EXPENSES 
    (description, amount, category, date)
    VALUES(?,?,?,?)"""

    cur.execute(data_sql , t)
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM EXPENSES
        ORDER BY date DESC, id DESC
        """) 
    
    expenses = cursor.fetchall()
    conn.close()

    return expenses

def get_filtered_expenses(start_date=None ,end_date=None, category=None):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    query = """
        SELECT *
        FROM expenses
        WHERE 1=1
        """ 

    parameters = []

    if start_date:
        query += " AND date >=?"
        parameters.append(start_date)

    if end_date:
        query += " AND date <=?"
        parameters.append(end_date)

    if category:
        query += " AND category =? "
        parameters.append(category)

    query += " ORDER BY date DESC, id DESC" 
    
    cursor.execute(query, parameters)

    expenses = cursor.fetchall()

    conn.close()

    return expenses

def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
            "DELETE FROM expenses WHERE id = ?", 
            (expense_id,) 
            )

    conn.commit()
    conn.close()
   
def category_totals():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM expenses
        GROUP BY category 
    """)

    data = cursor.fetchall()
    conn.close()

    return data 
