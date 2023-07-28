import os
import telebot
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


def send_notification(expected_return_date: datetime, book: str) -> None:
    notification_text = (f"Borrow date: {datetime.now()}\n"
                         f"Expected return date: {expected_return_date}\n"
                         f"Book: {book}")
    bot.send_message(chat_id=os.environ.get("CHAT_ID"), text=notification_text)
