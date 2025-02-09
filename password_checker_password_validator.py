import re

def password_checker(func):
    #  Декоратор для проверки пароля
    def wrapper(password):
        # Критерии проверки пароля
        if len(password) < 8:
            return "Ошибка: Пароль должен содержать минимум 8 символов."
        if not re.search(r'\d', password):
            return "Ошибка: Пароль должен содержать хотя бы одну цифру."
        if not re.search(r'[A-Z]', password):
            return "Ошибка: Пароль должен содержать хотя бы одну заглавную букву."
        if not re.search(r'[a-z]', password):
            return "Ошибка: Пароль должен содержать хотя бы одну строчную букву."
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return "Ошибка: Пароль должен содержать хотя бы один специальный символ."
        
        # Если все условия выполнены, вызываем оригинальную функцию
        return func(password)
    
    return wrapper

@password_checker
def register_user(password):
    return "Пользователь успешно зарегистрирован!"

# Тестовые случаи
print(register_user("Password1!"))  # Должен быть успешным
print(register_user("pass"))        # Слишком короткий
print(register_user("password123")) # Нет заглавной буквы
print(register_user("PASSWORD1!")) # Нет строчной буквы
print(register_user("Passw0rd"))   # Нет специального символа
print(register_user("Pass1!"))     # Меньше 8 символов

