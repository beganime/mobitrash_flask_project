### Настройка и запуск проекта

1. Клонируйте репозиторий:
   `git clone https://github.com/ВАШ_НИКНЕЙМ/ВАШ_РЕПО.git`
   `cd ВАШ_РЕПО`

2. Создайте и активируйте виртуальное окружение:
   `python -m venv venv`
   # Windows: `.\venv\Scripts\activate`
   # macOS/Linux: `source venv/bin/activate`

3. Установите зависимости:
   `pip install -r requirements.txt`

4. **Инициализируйте базу данных:**
   `python init_db.py`

5. Создайте файл `.env` в корне проекта со следующими переменными:
   ```
   DATABASE_URL="postgresql://user:password@host:port/database_name"
   # Или для SQLite:
   # DATABASE_URL="sqlite:///site.db"
   SECRET_KEY="ваша_секретная_фраза"
   ```
   (Не забудьте прописать эти переменные в вашем Flask-приложении, например, через `os.getenv` или Flask-DotEnv).

6. Запустите приложение:
   `flask run`

   (Установите PostgreSQL: Если его нет, вам нужно будет установить PostgreSQL на этот компьютер. Инструкции зависят от вашей ОС (Ubuntu/Debian: sudo apt install postgresql postgresql-contrib, Windows: скачать инсталлятор с postgresql.org).

    Создайте пользователя и базу данных в PostgreSQL: Вам нужно будет создать нового пользователя и новую базу данных в PostgreSQL для вашего приложения. Вы можете сделать это через консоль psql или с помощью графического инструмента (например, PgAdmin):
    
        -- Подключитесь как суперпользователь PostgreSQL (например, `psql -U postgres`)
    CREATE USER myapp_user WITH PASSWORD 'my_strong_and_secure_password';
    CREATE DATABASE myapp_db;
    GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;
    -- \q для выхода из psql)