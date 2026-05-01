import streamlit as st
from datetime import datetime
import json
import os

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

# Streamlit интерфейс
def main():
    st.title("Карманные деньги")
    
    # Загрузка данных
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
    
    # Отображение баланса
    st.subheader(f"Текущий баланс: {balance} ₽")
    st.subheader(f"Последний сброс: {last_reset_date}")

    # Кнопки для списания
    if st.button('Снять 100 ₽'):
        balance -= 100
        if balance < 0:
            balance = 0
        data["balance"] = balance
        save_data(data)
        st.experimental_rerun()

    if st.button('Снять 50 ₽'):
        balance -= 50
        if balance < 0:
            balance = 0
        data["balance"] = balance
        save_data(data)
        st.experimental_rerun()

    # Формы для разрешения
    mom = st.checkbox('Мама разрешила')
    dad = st.checkbox('Папа разрешил')

    if mom and dad:
        if st.button('Добавить 100 ₽'):
            balance += 100
            data["balance"] = balance
            save_data(data)
            st.experimental_rerun()

if __name__ == "__main__":
    main()
