import streamlit as st
import streamlit.components.v1 as components
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

dad_box = "☑" if dad == "1" else "☐"
mom_box = "☑" if mom == "1" else "☐"

plus_opacity = "1" if dad == "1" and mom == "1" else "0.45"

html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin: 0;
    background: white;
    font-family: Arial, sans-serif;
}}

.phone {{
    width: 100%;
    max-width: 360px;
    height: 650px;
    border: 4px solid black;
    background: white;
    box-sizing: border-box;
    overflow: hidden;
}}

.plus {{
    height: 140px;
    background: #18aee8;
    display: flex;
    align-items: center;
    padding-left: 22px;
    font-size: 62px;
    color: black;
    text-decoration: none;
    opacity: {plus_opacity};
    box-sizing: border-box;
}}

.checks {{
    height: 70px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    font-size: 13px;
    color: black;
}}

.checks a {{
    color: black;
    text-decoration: none;
}}

.balance {{
    height: 210px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 58px;
    color: black;
}}

.bottom {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    padding: 0 10px;
}}

.minus {{
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 52px;
    color: black;
    text-decoration: none;
}}

.green {{
    background: #24b84e;
}}

.red {{
    background: #f01825;
}}
</style>
</head>
<body>
    <div class="phone">
        <a class="plus" target="_top" href="?action=plus100&dad={dad}&mom={mom}">+ 100</a>

        <div class="checks">
            <a target="_top" href="?action=dad&dad={dad}&mom={mom}">{dad_box} Папа согласен</a>
            <a target="_top" href="?action=mom&dad={dad}&mom={mom}">{mom_box} Мама согласна</a>
        </div>

        <div class="balance">{data["balance"]} руб.</div>

        <div class="bottom">
            <a class="minus green" target="_top" href="?action=minus50">- 50</a>
            <a class="minus red" target="_top" href="?action=minus100">- 100</a>
        </div>
    </div>
</body>
</html>
"""

st.markdown("""
<style>
header, footer, #MainMenu {
    display: none !important;
}
.block-container {
    padding-top: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    max-width: 390px !important;
}
.stApp {
    background: white !important;
}
</style>
""", unsafe_allow_html=True)

components.html(html, height=680, scrolling=False)
