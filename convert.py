import pandas as pd 
# Функция для преобразования файла .csv в файл .xlsx
def convert_to_xlsx(csv_file, xlsx_file):
    df = pd.read_csv(csv_file)
    df.to_excel(xlsx_file, index=False)