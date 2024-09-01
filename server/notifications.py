from .config import settings
import requests


def send_notification(event):
    """
    Отправляет уведомление о событии в Telegram.

    Эта функция формирует сообщение на основе данных о событии и отправляет его в указанный Telegram-чат
    с использованием API Telegram. Если отправка уведомления не удалась, функция генерирует исключение.

    Attributes:
        event (Event): Экземпляр события, содержащий информацию для отправки уведомления. 
                       Используются атрибуты `title`, `level` и `description` для формирования текста сообщения.

    Исключения:
        Exception: Генерируется, если запрос на отправку уведомления в Telegram завершился ошибкой.
    """
    message = f"Новое событие: {event.title}\nУровень: {event.level}\nОписание: {event.description}"
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка отправки уведомления: {response.text}")
