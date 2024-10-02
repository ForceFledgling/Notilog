import argparse
import os
import sys
import threading
import logging
from datetime import datetime

from agent import NotilogAgent
from settings import Config, tracing

# Установка логирования с красивым форматированием
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)

# Инициализация блокировки
mtx = threading.Lock()

def exit_program(code):
    """Завершение программы с указанием кода завершения."""
    logging.shutdown()
    sys.exit(code)

def parse_args():
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Notilog Agent")
    parser.add_argument("-version", action="store_true", help="Вывести информацию о версии сборки")
    parser.add_argument("-print-config-stderr", action="store_true", help="Вывести весь объект конфигурации Notilog в stderr")
    parser.add_argument("-log-config-reverse-order", action="store_true", help="Вывести весь объект конфигурации Notilog на уровне Info в обратном порядке.")
    parser.add_argument("-dry-run", action="store_true", help="Запустить Notilog Agent, но выводить записи вместо отправки их на сервер.")
    parser.add_argument("-check-syntax", action="store_true", help="Проверить файл конфигурации на синтаксис")
    parser.add_argument("-inspect", action="store_true", help="Позволяет детально проверить стадии конвейера")
    parser.add_argument("-config.file", type=str, help="YAML файл для загрузки")
    parser.add_argument("-config.expand-env", action="store_true", help="Расширяет ${var} в конфигурации в соответствии со значениями переменных окружения.")
    
    return parser.parse_args()

def main():
    args = parse_args()

    # Проверка версии
    if args.version:
        logger.info(f"Notilog Agent версия: {Config.VERSION}")
        exit_program(0)

    # Инициализируем конфигурацию
    config = Config()
    
    # Загрузка конфигурации, включая параметры командной строки
    try:
        config.load_from_args(args)
    except Exception as e:
        logger.error("Не удалось разобрать конфигурацию: %s", e)
        exit_program(1)

    if args.check_syntax:
        if not args.config.file:
            logger.error("Недействительный файл конфигурации")
            exit_program(1)
        logger.info("Корректный файл конфигурации! Ошибок синтаксиса не найдено")
        exit_program(0)

    if args.print_config_stderr:
        try:
            config.print_to_stderr()
        except Exception as e:
            logger.error("Не удалось вывести конфигурацию в stderr: %s", e)

    if args.log_config:
        try:
            config.log_to_info()
        except Exception as e:
            logger.error("Не удалось зафиксировать объект конфигурации: %s", e)

    # Инициализация трассировки
    if config.tracing_enabled:
        try:
            trace = tracing.initialize("notilog-agent")
        except Exception as e:
            logger.error("Ошибка инициализации трассировки. Трассировка не будет включена: %s", e)
            trace = None

    # Создание экземпляра Notilog Agent
    with mtx:
        try:
            agent = NotilogAgent(config, args.dry_run)
        except Exception as e:
            logger.error("Ошибка создания Notilog Agent: %s", e)
            exit_program(1)

    logger.info("Запуск Notilog Agent")
    
    try:
        agent.run()
    except Exception as e:
        logger.error("Ошибка запуска Notilog Agent: %s", e)
        exit_program(1)
    
    if trace:
        trace.close()

if __name__ == "__main__":
    main()
