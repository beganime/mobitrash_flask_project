
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_secret_key')
    # Получаем URL базы данных из переменной окружения
    # Если переменная не установлена, используем значение по умолчанию (для отладки)
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/your_db_name')

import psycopg2
from contextlib import contextmanager

@contextmanager
def get_db():
    conn = None
    try:
        # Извлекаем параметры из DATABASE_URL
        from urllib.parse import urlparse
        url = urlparse(Config.DATABASE_URL)
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password
        )
        yield conn 
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        if conn:
            conn.rollback() # Откатываем транзакцию в случае ошибки
        raise # Повторно вызываем исключение, чтобы Flask мог его обработать
    finally:
        if conn:
            conn.close()