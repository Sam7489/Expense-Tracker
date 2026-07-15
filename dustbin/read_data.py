import sqlite3

DB_NAME = './instance/expenses.db'

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
