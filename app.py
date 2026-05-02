from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "balance_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 1000, "last_reset_date": None}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def check_weekly_reset(data):
    today = datetime.now().date()

    # суббота = 5
    if today.weekday() == 5 and data.get("last_reset_date") != str(today):
        data["balance"] = 1000
        data["last_reset_date"] = str(today)
        save_data(data)

    return data

@app.route("/")
def home():
    data = load_data()
    data = check_weekly_reset(data)
    return render_template("index.html", balance=data["balance"])

@app.route("/minus/<int:amount>", methods=["POST"])
def minus(amount):
    data = load_data()
    data["balance"] = max(0, data["balance"] - amount)
    save_data(data)
    return redirect(url_for("home"))

@app.route("/plus100", methods=["POST"])
def plus100():
    dad_ok = request.form.get("dad_ok")
    mom_ok = request.form.get("mom_ok")

    if dad_ok == "on" and mom_ok == "on":
        data = load_data()
        data["balance"] += 100
        save_data(data)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
