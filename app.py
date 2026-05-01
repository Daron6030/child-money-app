import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "balance_data.json"

st.set_page_config(
    page_title="",
    page_icon="💰",
    layout="centered"
)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 1000, "last_reset_date": None}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def rerun():
    st.rerun()

data = load_data()

today = datetime.now().date()
if today.weekday() == 5 and data.get("last_reset_date") != str(today):
    data["balance"] = 1000
    data["last_reset_date"] = str(today)
    save_data(data)

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

div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

button {
    border-radius: 0 !important;
    border: none !important;
    color: black !important;
    font-weight: 500 !important;
}

.top button {
    height: 130px !important;
    background: #11AEE8 !important;
    font-size: 56px !important;
}

.minus button {
    height: 180px !important;
    font-size: 46px !important;
}

.green button {
    background: #24B84E !important;
}

.red button {
    background: #F01825 !important;
}

.balance {
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 58px;
    color: black;
}

.checks {
    padding: 8px 12px 0 12px;
}

label {
    color: black !important;
    font-size: 14px !important;
}

[data-testid="stCheckbox"] {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top">', unsafe_allow_html=True)
add_clicked = st.button("+ 100", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="checks">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    dad_ok = st.checkbox("Папа согласен")

with col2:
    mom_ok = st.checkbox("Мама согласна")

st.markdown('</div>', unsafe_allow_html=True)

if add_clicked:
    if dad_ok and mom_ok:
        data["balance"] += 100
        save_data(data)
        rerun()
    else:
        st.warning("Нужно согласие папы и мамы")

st.markdown(
    f'<div class="balance">{data["balance"]} руб.</div>',
    unsafe_allow_html=True
)

col_green, col_red = st.columns(2)

with col_green:
    st.markdown('<div class="minus green">', unsafe_allow_html=True)
    if st.button("- 50", use_container_width=True):
        data["balance"] = max(0, data["balance"] - 50)
        save_data(data)
        rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_red:
    st.markdown('<div class="minus red">', unsafe_allow_html=True)
    if st.button("- 100", use_container_width=True):
        data["balance"] = max(0, data["balance"] - 100)
        save_data(data)
        rerun()
    st.markdown('</div>', unsafe_allow_html=True)
