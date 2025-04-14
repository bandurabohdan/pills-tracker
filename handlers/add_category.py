from telegram import Update
from telegram.ext import CallbackContext

from markups import user_state
from handlers.reply import reply

async def add_category(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_state[user_id] = {'action':  'adding_category'}
    await reply(update, "Введіть назву категорії: ")