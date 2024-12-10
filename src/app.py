from datetime import date, datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# データベースモデル
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    purpose = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)


# データベース初期化
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    today = date.today()
    current_year = today.year
    current_month = today.month

    year = request.args.get("year", type=int, default=current_year)
    month = request.args.get("month", type=int, default=current_month)

    # 月の合計金額
    expenses = Expense.query.filter(
        db.extract("year", Expense.date) == year, db.extract("month", Expense.date) == month
    ).all()
    total = sum(expense.amount for expense in expenses)

    # ボタン有効/無効
    can_view_previous = (year > current_year - 1) or (year == current_year - 1 and month > 1)
    can_view_next = (year < current_year) or (year == current_year and month < current_month)

    return render_template(
        "index.html",
        year=year,
        month=month,
        total=total,
        can_view_previous=can_view_previous,
        can_view_next=can_view_next,
    )


@app.route("/add", methods=["GET", "POST"])
def add_memory():
    if request.method == "POST":
        date_str = request.form.get("date")
        purposes = request.form.getlist("purpose")
        amounts = request.form.getlist("amount")

        for purpose, amount in zip(purposes, amounts, strict=False):
            if purpose and amount:
                expense = Expense(date=datetime.strptime(date_str, "%Y-%m-%d"), purpose=purpose, amount=int(amount))
                db.session.add(expense)
        db.session.commit()

        return redirect(url_for("success"))

    today = date.today().strftime("%Y-%m-%d")
    return render_template("add_memory.html", today=today)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
