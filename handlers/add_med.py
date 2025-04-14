from telegram import Update
from telegram.ext import CallbackContext

from markups import user_state, categories_markup
from handlers.reply import reply

async def add_med(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_state[user_id] = {'action': 'choosing_category_for_med'}
    await reply(update, "Виберіть категорію ліків: ", categories_markup())