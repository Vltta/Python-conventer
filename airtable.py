import requests
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