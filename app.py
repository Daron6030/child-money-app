from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

# Путь к файлу с данными
DATA_FILE = "balance_data.json"


# Загрузка данных из файла
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 1000, "last_reset_date": None}
    
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@app.route("/")
def home():
    data = load_data()
    balance = data["balance"]
    last_reset_date = data["last_reset_date"]
    
    # Обновление баланса каждую неделю (в субботу)
    today = datetime.now().date()
    if today.weekday() == 5:  # Проверяем, если сегодня суббота
        if last_reset_date != str(today):
            balance = 1000  # Сброс баланса каждую неделю
            last_reset_date = str(today)
            save_data({"balance": balance, "last_reset_date": last_reset_date})

    return render_template("index.html", balance=balance, last_reset_date=last_reset_date)


@app.route("/spend/<amount>")
def spend(amount):
    amount = int(amount)
    data = load_data()
    
    new_balance = data["balance"] - amount
    if new_balance < 0:
        new_balance = 0  # Баланс не может быть меньше нуля

    data["balance"] = new_balance
    save_data(data)

    return redirect(url_for("home"))


@app.route("/add_bonus", methods=["POST"])
def add_bonus():
    if "mom" in request.form and "dad" in request.form:
        data = load_data()
        data["balance"] += 100
        save_data(data)
    
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)