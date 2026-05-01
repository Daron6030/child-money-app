import streamlit as st
from datetime import datetime
import json
import os

DATA_FILE = "balance_data.json"


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


st.set_page_config(
    page_title="",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    header, footer, #MainMenu {
        visibility: hidden;
    }

    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 390px;
    }

    body {
        background: white;
    }

    .phone-box {
        border: 5px solid #111;
        border-radius: 4px;
        height: 680px;
        max-width: 360px;
        margin: 0 auto;
        background: white;
        overflow: hidden;
    }

    .top-zone {
        background: #12a8df;
        height: 155px;
        display: flex;
        align-items: center;
        padding-left: 18px;
        font-size: 58px;
        color: black;
    }

    .checks {
        height: 65px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-size: 13px;
        color: black;
    }

    .balance-zone {
        height: 165px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 58px;
        color: black;
    }

    .bottom-zone {
        height: 280px;
        display: flex;
        gap: 14px;
        padding: 10px;
    }

    div[data-testid="stButton"] > button {
        border: none;
        border-radius: 0;
        color: black;
        font-size: 48px;
        height: 180px;
        width: 100%;
    }

    .green button {
        background-color: #25b64b !important;
    }

    .red button {
        background-color: #f01825 !important;
    }

    .blue button {
        background-color: #12a8df !important;
        height: 130px !important;
        font-size: 58px !important;
        text-align: left !important;
    }

    label {
        font-size: 13px !important;
    }

    .stCheckbox {
        margin-top: -10px;
    }
</style>
""", unsafe_allow_html=True)


data = load_data()

today = datetime.now().date()
if today.weekday() == 5:
    if data.get("last_reset_date") != str(today):
        data["balance"] = 1000
        data["last_reset_date"] = str(today)
        save_data(data)

balance = data["balance"]

st.markdown('<div class="phone-box">', unsafe_allow_html=True)

st.markdown('<div class="blue">', unsafe_allow_html=True)
add_clicked = st.button("+ 100", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    dad_ok = st.checkbox("Папа согласен")

with col2:
    mom_ok = st.checkbox("Мама согласна")

if add_clicked:
    if dad_ok and mom_ok:
        data["balance"] += 100
        save_data(data)
        rerun()
    else:
        st.warning("Нужно согласие папы и мамы")

st.markdown(
    f"""
    <div class="balance-zone">
        {data["balance"]} руб.
    </div>
    """,
    unsafe_allow_html=True
)

col_green, col_red = st.columns(2)

with col_green:
    st.markdown('<div class="green">', unsafe_allow_html=True)
    if st.button("- 50", use_container_width=True):
        data["balance"] = max(0, data["balance"] - 50)
        save_data(data)
        rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_red:
    st.markdown('<div class="red">', unsafe_allow_html=True)
    if st.button("- 100", use_container_width=True):
        data["balance"] = max(0, data["balance"] - 100)
        save_data(data)
        rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
