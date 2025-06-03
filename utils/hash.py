from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_pass_security(password: str) -> bool:
    """Проверяет, соответствует ли пароль требованиям безопасности"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):  # Проверка на наличие заглавной буквы
        return False
    if not re.search(r'[a-z]', password):  # Проверка на наличие строчной буквы
        return False
    if not re.search(r'[0-9]', password):  # Проверка на наличие цифры
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Проверка на наличие спец. символа
        return False
    return True

def hash_password(password: str) -> str:
    """Хэширует пароль"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли предоставленный пароль хэшу"""
    return pwd_context.verify(plain_password, hashed_password)

def update_password_hash(hashed_password: str) -> str:
    """Обновляет хэш пароля, если это необходимо"""
    if pwd_context.needs_update(hashed_password):
        return pwd_context.hash(hashed_password)
    return hashed_password

def check_password_strength(password: str) -> bool:
    """Проверяет, соответствует ли пароль требованиям безопасности"""
    return len(password) >= 8