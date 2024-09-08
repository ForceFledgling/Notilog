## Быстрый запуск сервера

После клонирования репозитория, создаем виртуальное окружение, входим в него, устанавливаем зависимости и запускает приложение как модуль:

```
git clone https://github.com/ForceFledgling/notilog.git
cd notilog
python -m venv venv
source venv/bin/activate
python -m pip install server/requirements.txt
python -m server
```

После мы увидим успешный запуск:

```
INFO:     Will watch for changes in these directories: ['/Users/vladimir/Desktop/Репозитории/notilog']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [6480] using WatchFiles
INFO:     Started server process [6482]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```