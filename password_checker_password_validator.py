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