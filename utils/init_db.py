import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv() # Загружаем переменные из .env

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/your_db_name')

def init_db():
    conn = None
    try:
        url = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price NUMERIC(10, 2) NOT NULL,
                description TEXT,
                image_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS basket (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
            );
        """)

        # Опционально: вставка начальных данных (seed data)
        # Это полезно для тестов или для того, чтобы приложение сразу было с какими-то данными
        cur.execute("""
            INSERT INTO users (name, password, email)
            VALUES ('testuser', 'your_hashed_password_here', 'test@example.com')
            ON CONFLICT (name) DO NOTHING;
        """)
        cur.execute("""
            INSERT INTO product (name, price, description)
            VALUES ('Samsung Galaxy ZFold 4', 0.00, 'В линейке Samsung Galaxy Z Fold4...')
            ON CONFLICT (name) DO NOTHING;
        """)
        cur.execute("""
            INSERT INTO product (name, price, description)
            VALUES ('iPhone 15 Pro', 999.99, 'Новейший флагман от Apple.')
            ON CONFLICT (name) DO NOTHING;
        """)


        conn.commit()
        print("База данных успешно инициализирована и таблицы созданы.")

    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL при инициализации БД: {e}")
        if conn:
            conn.rollback() 
    except Exception as e:
        print(f"Неожиданная ошибка при инициализации БД: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    init_db()