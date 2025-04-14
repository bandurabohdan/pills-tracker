import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from handlers.reply import reply
from handlers.add_category import add_category
from handlers.add_med import add_med
from handlers.list_med import list_med
from handlers.take_med import take_med
from handlers.handle_input import handler

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    await reply(update, f"Привіт, {user.first_name}! Я бот для відслідковування ліків.💊\n")

def main():
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Text('Додати категорію'), add_category))
    application.add_handler(MessageHandler(filters.Text('Додати ліки'), add_med))
    application.add_handler(MessageHandler(filters.Text('Вжити ліки'), take_med))
    application.add_handler(MessageHandler(filters.Text('Список ліків'), list_med))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.handle_input))

    application.run_polling()

if __name__ == '__main__':
    main()