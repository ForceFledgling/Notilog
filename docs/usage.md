# Подготовка базы данных PostgreSQL

Создаем базу, пользователя и выдаем ему права:

```
-- Создать базу данных
CREATE DATABASE notilog;

-- Создать пользователя
CREATE USER notilog WITH PASSWORD 'P@ssw0rd123';

-- Предоставить все привилегии на базу данных пользователю
GRANT ALL PRIVILEGES ON DATABASE notilog TO notilog;

-- Отключистесь от базы данных
\q

-- Подключитесь к базе данных как суперпользователь
psql -U postgres -d notilog

-- Убедитесь, что права на схему public установлены
GRANT USAGE ON SCHEMA public TO notilog;
GRANT CREATE ON SCHEMA public TO notilog;
```

# Серверная часть

## Тестовое окружение

Создайте и активируйте виртуальное окружение:

```
python3.11 -m venv venv
source venv/bin/activate
```

Установите зависимости:

```
pip install --upgrade pip
pip install -r server/requirements.txt
```

Запустите сервер:

```
uvicorn server.api:app --host 0.0.0.0 --port 8000
```

123