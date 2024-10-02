# Указываем базовый образ с Python
FROM python:3.11-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && \
    apt-get install -qy libsystemd-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Указываем рабочую директорию
WORKDIR /usr/src/notilog

# Копируем файлы проекта в контейнер
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем конфигурационный файл Notilog Agent
COPY examples/docker.yaml /etc/notilog/config.yml

# Задаем точку входа и аргументы по умолчанию
ENTRYPOINT ["python", "main.py"]  # TODO добавить аргументы запуска
CMD ["-config.file=/etc/notilog/config.yml"]
