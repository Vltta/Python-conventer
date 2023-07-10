# Функция для вывода сообщения о результате операции
def print_result(success, message):
    if success:
        print("Операция успешно выполнена.")
    else:
        print("Произошла ошибка:", message)