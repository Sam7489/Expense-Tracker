import sqlite3

DB_NAME = './instance/expenses.db'

def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
            "DELETE FROM expenses WHERE id = ?", 
            (expense_id,) 
            )

    conn.commit()
    conn.close()
   
