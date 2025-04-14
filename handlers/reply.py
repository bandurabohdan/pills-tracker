from typing import Optional
from telegram import ReplyKeyboardMarkup, Update

from markups import buttons_markup

async def reply(update: Update, message: Optional[str] = None, reply_markup: Optional[ReplyKeyboardMarkup] = None, parse_mode: Optional[str] = None):
    await update.message.reply_text(
        message or "Будь ласка, скористайтесь кнопками меню.",
        reply_markup = reply_markup or buttons_markup,
        parse_mode = parse_mode
    )