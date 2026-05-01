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

params = st.query_params
action = params.get("action", "")
dad = params.get("dad", "0")
mom = params.get("mom", "0")

if action == "dad":
    dad = "0" if dad == "1" else "1"
    st.query_params["dad"] = dad
    st.query_params["mom"] = mom
    st.query_params["action"] = ""
    st.rerun()

if action == "mom":
    mom = "0" if mom == "1" else "1"
    st.query_params["dad"] = dad
    st.query_params["mom"] = mom
    st.query_params["action"] = ""
    st.rerun()

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
    if dad == "1" and mom == "1":
        data["balance"] += 100
        save_data(data)
    st.query_params.clear()
    st.rerun()

dad_mark = "✅" if dad == "1" else "⬜"
mom_mark = "✅" if mom == "1" else "⬜"

plus_link = "?action=plus100&dad=1&mom=1" if dad == "1" and mom == "1" else "#"

st.markdown("""
<style>
header, footer, #MainMenu {
    display: none !important;
}

.stApp {
    background: white !important;
}

.block-container {
    padding: 0 !important;
    max-width: 390px !important;
}

.phone {
    width: 100%;
    height: 720px;
    border: 4px solid black;
    background: white;
    overflow: hidden;
}

.plus {
    height: 150px;
    background: #18aee8;
    display: flex;
    align-items: center;
    padding-left: 22px;
    font-size: 64px;
    color: black !important;
    text-decoration: none !important;
}

.plus.locked {
    opacity: 0.45;
}

.checks {
    height: 70px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    font-size: 15px;
    color: black;
}

.checks a {
    color: black !important;
    text-decoration: none !important;
}

.balance {
    height: 210px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 64px;
    color: black;
}

.bottom {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    padding: 0 10px;
}

.minus {
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    color: black !important;
    text-decoration: none !important;
}

.green {
    background: #24b84e;
}

.red {
    background: #f01825;
}
</style>
""", unsafe_allow_html=True)

html = f"""
<div class="phone">
    <a class="plus {'locked' if not (dad == '1' and mom == '1') else ''}" href="{plus_link}">+ 100</a>

    <div class="checks">
        <a href="?action=dad&dad={dad}&mom={mom}">{dad_mark} Папа согласен</a>
        <a href="?action=mom&dad={dad}&mom={mom}">{mom_mark} Мама согласна</a>
    </div>

    <div class="balance">{data["balance"]} руб.</div>

    <div class="bottom">
        <a class="minus green" href="?action=minus50">- 50</a>
        <a class="minus red" href="?action=minus100">- 100</a>
    </div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)
