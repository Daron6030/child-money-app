import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "balance_data.json"

st.set_page_config(page_title="Деньги", page_icon="💰", layout="centered")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 1000, "last_reset_date": None}
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

data = load_data()

today = datetime.now().date()
if today.weekday() == 5 and data.get("last_reset_date") != str(today):
    data["balance"] = 1000
    data["last_reset_date"] = str(today)
    save_data(data)

action = st.query_params.get("action")

if action == "minus50":
    data["balance"] = max(0, data["balance"] - 50)
    save_data(data)
    st.query_params.clear()
    st.rerun()

if action == "minus100":
    data["balance"] = max(0, data["balance"] - 100)
    save_data(data)
    st.query_params.clear()
    st.rerun()

if action == "plus100":
    data["balance"] += 100
    save_data(data)
    st.query_params.clear()
    st.rerun()

st.markdown("""
<style>
header, footer, #MainMenu {
    display: none !important;
}

.stApp {
    background: #ffffff !important;
}

.block-container {
    padding: 0 !important;
    max-width: 390px !important;
}

.phone {
    width: 100%;
    height: 720px;
    background: white;
    border: 4px solid black;
    box-sizing: border-box;
    overflow: hidden;
}

.btn {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: black !important;
    font-size: 58px;
    font-weight: 500;
    box-sizing: border-box;
}

.plus {
    height: 150px;
    background: #14AEEA;
    padding-left: 22px;
}

.plus-disabled {
    height: 150px;
    background: #14AEEA;
    color: rgba(0,0,0,0.35) !important;
    padding-left: 22px;
}

.checks {
    padding: 8px 16px 0 16px;
    color: black;
    font-size: 14px;
}

.balance {
    height: 230px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 62px;
    color: black;
}

.bottom {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    padding: 0 10px 10px 10px;
}

.minus {
    height: 180px;
    justify-content: center;
}

.green {
    background: #24B84E;
}

.red {
    background: #F01825;
}

label {
    color: black !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)

dad_ok = st.checkbox("Папа согласен")
mom_ok = st.checkbox("Мама согласна")

if dad_ok and mom_ok:
    plus_html = '<a class="btn plus" href="?action=plus100">+ 100</a>'
else:
    plus_html = '<div class="btn plus-disabled">+ 100</div>'

st.markdown(f"""
<div class="phone">
    {plus_html}

    <div class="checks">
        ✅ Папа: {'да' if dad_ok else 'нет'} &nbsp;&nbsp;&nbsp;
        ✅ Мама: {'да' if mom_ok else 'нет'}
    </div>

    <div class="balance">
        {data["balance"]} руб.
    </div>

    <div class="bottom">
        <a class="btn minus green" href="?action=minus50">- 50</a>
        <a class="btn minus red" href="?action=minus100">- 100</a>
    </div>
</div>
""", unsafe_allow_html=True)
