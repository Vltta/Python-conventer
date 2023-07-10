import sqlite3

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