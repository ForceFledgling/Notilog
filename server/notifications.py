from .config import settings
import requests

def send_notification(event):
    # Пример отправки уведомления в Telegram
    message = f"Новое событие: {event.title}\nУровень: {event.level}\nОписание: {event.description}"
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка отправки уведомления: {response.text}")
