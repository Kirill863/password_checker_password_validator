import re
from typing import Callable, Any
import csv


# Декоратор password_validator с аннотациями типов
def password_validator(
    min_length: int = 8,
    min_uppercase: int = 1,
    min_lowercase: int = 1,
    min_special_chars: int = 1
) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            password: str = kwargs.get('password') or args[1]  # Получаем пароль из аргументов
            
            errors: list[str] = []

            # Проверка минимальной длины
            if len(password) < min_length:
                errors.append(f"Пароль должен содержать минимум {min_length} символов.")

            # Проверка наличия заглавных букв
            uppercase_count: int = len(re.findall(r'[A-Z]', password))
            if uppercase_count < min_uppercase:
                errors.append(f"Пароль должен содержать минимум {min_uppercase} заглавную букву(вы).")

            # Проверка наличия строчных букв
            lowercase_count: int = len(re.findall(r'[a-z]', password))
            if lowercase_count < min_lowercase:
                errors.append(f"Пароль должен содержать минимум {min_lowercase} строчную букву(вы).")

            # Проверка наличия специальных символов
            special_char_count: int = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
            if special_char_count < min_special_chars:
                errors.append(f"Пароль должен содержать минимум {min_special_chars} специальный символ(ы).")

            # Если есть ошибки, выбрасываем ValueError
            if errors:
                raise ValueError("\n".join(errors))

            # Если все хорошо, вызываем оригинальную функцию
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Декоратор username_validator с аннотациями типов
def username_validator(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        username: str = kwargs.get('username') or args[0]  # Получаем имя пользователя из аргументов
        
        if ' ' in username:
            raise ValueError("Имя пользователя не должно содержать пробелы.")
        
        # Если все хорошо, вызываем оригинальную функцию
        return func(*args, **kwargs)
    return wrapper


# Функция register_user с аннотациями типов
@username_validator
@password_validator(min_length=8, min_uppercase=1, min_lowercase=1, min_special_chars=1)
def register_user(username: str, password: str) -> str:
    # Запись данных в CSV файл
    with open('users.csv', mode='a', newline='', encoding='utf-8') as file:
        writer: csv.writer = csv.writer(file)
        writer.writerow([username, password])
    
    return "Пользователь успешно зарегистрирован!"


# Тестирование функции
try:
    print(register_user("john_doe", "Password1!"))  # Успешная регистрация
    print(register_user("jane doe", "Password1!"))  # Ошибка: пробел в имени пользователя
    print(register_user("alice", "pass"))          # Ошибка: короткий пароль
except ValueError as e:
    print(f"Ошибка: {e}")