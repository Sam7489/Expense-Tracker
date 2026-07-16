from dotenv import load_dotenv
import os
from flask import Flask, render_template , request , url_for, make_response , flash , redirect , Response
from datetime import date , datetime
import csv
import io
from crud import add_expense, get_all_expenses, get_filtered_expenses , delete_expense , category_pie_chart , daily_spending_chart


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# categories 
CATEGORIES = ["Food", "Travel", "Essentials","Bills", "Others"]

@app.route("/")
def index():
    expenses = get_all_expenses()
    

    # filter request
    start = request.args.get("start_date")
    end   = request.args.get("end_date")
    selected_category = request.args.get("category")

    expenses = get_filtered_expenses(
        start, 
        end,
        selected_category
    )
    # add total sum 
    total = round(sum(e["amount"] for e in expenses), 2)

    #------------pie chart data-------------
    chart_data = category_pie_chart()
    labels =[]
    values =[]
    for row in chart_data:
        labels.append(row["category"])
        values.append(row["total"])

    #----------------------------------------

    #------------bar chart data--------------
    bar_data = daily_spending_chart()
    bar_labels = [row["day"] for row in bar_data]
    bar_values = [row["total"] for row in bar_data]
    # both lines are similar to above 
    
    #-----------------------------------------


    return render_template(
        "index.html" ,
        expenses=expenses,
        today=date.today().isoformat(),
        categories=CATEGORIES,
        total=total, 
        labels=labels,
        values=values,
        bar_labels=bar_labels,
        bar_values=bar_values

         
         
        )

@app.route("/add" , methods=['POST'])
def add():

    #store values from the form
    description = (request.form.get("description") or "").strip()
    amount_str  = (request.form.get("amount") or  "").strip()
    date_str    = (request.form.get("date") or  "").strip()
    category    = (request.form.get("category") or "").strip()

    # if no data is given
    if not description or not amount_str or not category:
        flash("Please fill description, amount and category", "error")
        return redirect(url_for("index"))
    

    # if amount is less than 0 
    try:
        amount = float(amount_str)
        if amount <= 0 : 
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number", "error")
        # return to the index page 
        return redirect(url_for("index"))

    # date expection
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        d = date.today()

    # add data to the database
    add_expense(description , amount , category, d)
    flash("Expense added", "success")
    return redirect(url_for("index"))

@app.route('/delete/<int:expense_id>' , methods=['POST'])
def delete(expense_id):
    delete_expense(expense_id)

    flash("Expense Deleted", "success")
    return redirect(url_for("index"))

@app.route("/export.csv")
def export_csv():
    
    start_date = request.args.get("start_date")
    end_date   = request.args.get("end_date")
    category   = request.args.get("category")

    expenses   = get_filtered_expenses(
        start_date=start_date,
        end_date=end_date,
        category=category
    )

    # csv code 
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Description",
        "Amount",
        "Category",
        "Date"
    ])

    for expense in expenses:
        writer.writerow([
            expense["description"],
            expense["amount"],
            expense["category"],
            expense["date"]
        ])
    
    output.seek(0)

    #------- give the file a suitable name
    if start_date and end_date:
        filename = f"expenses_{start_date}_to_{end_date}.csv"
    elif start_date:
        filename = f"expenses_from_{start_date}.csv"
    elif end_date:
        filename = f"expenses_until_{end_date}.csv"
    else:
        filename = "expenses_all.csv"
    #--------------------------------------- 

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )



if __name__ == "__main__":
    app.run(debug=True, port=5000)
