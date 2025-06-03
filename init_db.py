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
                id serial NOT NULL,
                name text NOT NULL,
                email text NOT NULL,
                password text NOT NULL,
                role text NOT NULL DEFAULT 'user'::text,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS product (
                id integer NOT NULL DEFAULT nextval('samsung_mobile_id_seq'::regclass),
                image_url VARCHAR(255),
                name text NOT NULL,
                price integer NOT NULL,
                description character(4000) NOT NULL,
                procesor character(100) NOT NULL,
                batarey integer NOT NULL,
                ram integer NOT NULL,
                rom integer NOT NULL,
                display character(100),
                camera character(100) NOT NULL,
                "like" integer DEFAULT 0,
                created_at timestamp without time zone NOT NULL DEFAULT timezone('utc'::text, now()),
                storage integer,
                category_id integer NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS basket (
                id serial NOT NULL,
                user_id integer NOT NULL,
                product_id integer NOT NULL,
                added_date timestamp without time zone NOT NULL DEFAULT timezone('utc'::text, now()),
                active boolean NOT NULL DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id serial NOT NULL,
                device character(50),
                company character(50)
            );
        """)

        cur.execute("""
            INSERT INTO users (name, password, email,role)
            VALUES ('Bega', '123456789', 'bega@example.com','admin')
            ON CONFLICT (name) DO NOTHING;
        """)
        cur.execute("""
            INSERT INTO users (name, password, email)
            VALUES ('David', '1234567890', 'david@example.com')
            ON CONFLICT (name) DO NOTHING;
        """)
        cur.execute("""
            INSERT INTO product ( name, price, description, procesor, batarey, ram, rom, display, 
            camera, "like", storage, category_id)
            VALUES ( 'testphone1', 544, 'mobileblablbabla', 'fws2', 5000, 8, 128, 'amoled','3(10MP-8MP-4MP)', 
            0, 10, 1)
            ON CONFLICT (name) DO NOTHING;
        """)
        cur.execute("""
            INSERT INTO product ( name, price, description, procesor, batarey, ram, rom, display, 
            camera, "like", storage, category_id)
            VALUES ( 'testphone2', 234, 'mobileblablbabla', 'fws2', 5000, 8, 128, 'amoled','3(10MP-8MP-4MP)', 
            0, 10, 1)
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