## Запуск в DEV режиме

Разворачиваем базу данных:

```
backend % docker-compose -f docker-compose.dev.yml up db
```

Установка зависимостей:

```
backend % hatch env create
```

Активируем окружение:

```
backend % hatch shell
```

Появится приставка `(app)`, указывающая что вы находитесь в окружении.

Выполняем играции:

```
backend % alembic upgrade head
```

Выполняем инициализацию:

```
backend % chmod +x scripts/*     
backend % ./scripts/prestart.sh 
```

Запускаем бекенд

```
backend % fastapi run app/main.py
```