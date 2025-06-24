### Настройка и запуск проекта
 Для начала вы можете установить конфиг который поможет устанавливать зависимосты с другого сайта (зеркало) 
 
 ```bash
 pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
 ```
1. Клонируйте репозиторий:
   `git clone https://github.com/ВАШ_НИКНЕЙМ/ВАШЕ_ИМЯ_РЕПОЗИТОРИЯ.git`
   `cd ВАШЕ_ИМЯ_РЕПОЗИТОРИЯ`

2. Создайте и активируйте виртуальное окружение:
   `python -m venv venv`
   `source venv/bin/activate` # Или `.\venv\Scripts\activate` для Windows

3. Установите зависимости:
   `pip install -r requirements.txt`

4. **Настройте PostgreSQL:**
   * Установите PostgreSQL, если у вас его нет.
   * Создайте базу данных и пользователя в PostgreSQL (например, `myapp_db` и `myapp_user`).
   * Создайте файл `.env` в корне проекта со строкой подключения к вашей БД и секретным ключом:
     ```
      DB_USER=postgres
      DB_PASSWORD=12345
      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=mobitrash
     ```

5. Запустите Flask-приложение:
   `python app.py`

   (Установите PostgreSQL: Если его нет, вам нужно будет установить PostgreSQL на этот компьютер. Инструкции зависят от вашей ОС (Ubuntu/Debian: sudo apt install postgresql postgresql-contrib, Windows: скачать инсталлятор с postgresql.org).

    Создайте пользователя и базу данных в PostgreSQL: Вам нужно будет создать нового пользователя и новую базу данных в PostgreSQL для вашего приложения. Вы можете сделать это через консоль psql или с помощью графического инструмента (например, PgAdmin):
    
        -- Подключитесь как суперпользователь PostgreSQL (например, `psql -U postgres`)
        CREATE USER myapp_user WITH PASSWORD 'my_strong_and_secure_password';
        CREATE DATABASE myapp_db;
        GRANT ALL PRIVILEGES ON DATABASE myapp_db TO myapp_user;
        -- \q для выхода из psql)