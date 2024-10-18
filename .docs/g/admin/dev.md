## Запуск в DEV режиме

Разворачиваем базу данных:

```
docker-compose -f docker-compose.dev.yml up db
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

Запускаем бекенд

```
backend % fastapi run app/main.py
```