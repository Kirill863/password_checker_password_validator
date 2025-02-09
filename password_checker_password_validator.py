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

# **Функция `register_user`**
	# - **Аргументы**: Принимает пароль в качестве аргумента.
	# - **Возвращаемое значение**: Сообщение об успешной регистрации, если пароль прошел проверку, или сообщение об ошибке в противном случае.
	# - **Применение декоратора**: Используйте `@password_checker` для автоматической проверки пароля. 
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

import re

def password_validator(min_length=8, min_uppercase=1, min_lowercase=1, min_special_chars=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            password = kwargs.get('password') or args[1]  # Получаем пароль из аргументов
            
            errors = []

            # Проверка минимальной длины
            if len(password) < min_length:
                errors.append(f"Пароль должен содержать минимум {min_length} символов.")

            # Проверка наличия заглавных букв
            uppercase_count = len(re.findall(r'[A-Z]', password))
            if uppercase_count < min_uppercase:
                errors.append(f"Пароль должен содержать минимум {min_uppercase} заглавную букву(вы).")

            # Проверка наличия строчных букв
            lowercase_count = len(re.findall(r'[a-z]', password))
            if lowercase_count < min_lowercase:
                errors.append(f"Пароль должен содержать минимум {min_lowercase} строчную букву(вы).")

            # Проверка наличия специальных символов
            special_char_count = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
            if special_char_count < min_special_chars:
                errors.append(f"Пароль должен содержать минимум {min_special_chars} специальный символ(ы).")

            # Если есть ошибки, выбрасываем ValueError
            if errors:
                raise ValueError("\n".join(errors))

            # Если все хорошо, вызываем оригинальную функцию
            return func(*args, **kwargs)
        return wrapper
    return decorator

def username_validator(func):
    def wrapper(*args, **kwargs):
        username = kwargs.get('username') or args[0]  # Получаем имя пользователя из аргументов
        
        if ' ' in username:
            raise ValueError("Имя пользователя не должно содержать пробелы.")
        
        # Если все хорошо, вызываем оригинальную функцию
        return func(*args, **kwargs)
    return wrapper

import csv

@username_validator
@password_validator(min_length=8, min_uppercase=1, min_lowercase=1, min_special_chars=1)
def register_user(username, password):
    # Запись данных в CSV файл
    with open('users.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    
    return "Пользователь успешно зарегистрирован!"
