import os
import sqlite3
import pandas as pd
import requests

# Функция для создания или подключения к базе данных
def connect_database():
    conn = sqlite3.connect('settings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (id INTEGER PRIMARY KEY, api_key TEXT, database_id TEXT, table_name TEXT)''')
    conn.commit()
    return conn

# Функция для получения пользовательских настроек из базы данных
def get_settings(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM settings WHERE id=1")
    row = c.fetchone()
    if row:
        api_key, database_id, table_name = row[1], row[2], row[3]
        return api_key, database_id, table_name
    else:
        return None

# Функция для сохранения пользовательских настроек в базе данных
def save_settings(conn, api_key, database_id, table_name):
    c = conn.cursor()
    c.execute("DELETE FROM settings")
    c.execute("INSERT INTO settings (id, api_key, database_id, table_name) VALUES (?, ?, ?, ?)",
              (1, api_key, database_id, table_name))
    conn.commit()

# Функция для преобразования файла .csv в файл .xlsx
def convert_to_xlsx(csv_file, xlsx_file):
    df = pd.read_csv(csv_file)
    df.to_excel(xlsx_file, index=False)

# Функция для отправки данных в Airtable
def send_to_airtable(api_key, database_id, table_name, csv_file):
    url = f"https://api.airtable.com/v0/{database_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    df = pd.read_csv(csv_file)
    df = df.astype(str)  # Преобразуем числа в строки
    records = df.to_dict(orient='records')
    data = {"records": records}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

# Функция для вывода сообщения о результате операции
def print_result(success, message):
    if success:
        print("Операция успешно выполнена.")
    else:
        print("Произошла ошибка:", message)

# Функция для выбора действия и взаимодействия с пользователем
def interact():
    conn = connect_database()

    while True:
        print("Выберите действие:")
        print("1. Установить настройки Airtable")
        print("2. Преобразовать файл .csv в файл .xlsx")
        print("3. Отправить данные в Airtable")
        print("4. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == "1":
            api_key = input("Введите API ключ Airtable: ")
            database_id = input("Введите ID базы данных Airtable: ")
            table_name = input("Введите название таблицы Airtable: ")
            save_settings(conn, api_key, database_id, table_name)
            print("Настройки сохранены.")
        elif choice == "2":
            csv_file = input("Введите путь к файлу .csv: ")
            xlsx_file = input("Введите путь для сохранения файла .xlsx: ")
            try:
                convert_to_xlsx(csv_file, xlsx_file)
                print_result(True, "")
            except Exception as e:
                print_result(False, str(e))
        elif choice == "3":
            settings = get_settings(conn)
            if settings:
                csv_file = input("Введите путь к файлу .csv: ")
                try:
                    send_to_airtable(settings[0], settings[1], settings[2], csv_file)
                    print_result(True, "")
                except Exception as e:
                    print_result(False, str(e))
            else:
                print("Настройки не найдены. Установите настройки Airtable.")
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")
            
    conn.close()

# Запуск программы
interact()
