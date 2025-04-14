from telegram import Update
from telegram.ext import CallbackContext

from markups import user_state, medications_markup
from handlers.reply import reply
from supabase_client import supabase
# telegrambot2025!
class HandleInput:

    def __init__(self):
        pass

    async def adding_category(self, update: Update, user_id: str):
        category_name = update.message.text
        supabase.insert_data('categories', { "name": category_name })
        user_state[user_id] = None
        await reply(update, f"Категорія '{category_name}' була додана!")
        return
    
    async def choosing_category_for_take_med(self, update: Update, user_id: str, category: str):
        user_state[user_id]['action'] = 'choosing_med_from_category'
        user_state[user_id]['category'] = category
        await reply(update, f"Ви обрали категорію: {category}\nТепер виберіть назву ліків:", medications_markup(category))
        return
    
    async def choosing_med_quantity(self, update: Update, user_id: str, qty: str):
        category = user_state[user_id].get('category')
        medication = user_state[user_id].get('med')
        medications = supabase.get_meds()

        medication = medication.split("-")
        name = medication[0].strip().lower()

        if category and medication:
            for med in medications:
                print(med)
                if med["name"].lower() == name.lower():
                    if med['units'] >= int(qty):
                        supabase.update_data('medications', { 'units': med['units'] - int(qty) }, med["id"])
                        await reply(update, f"Ви прийняли {int(qty)} шт. {med['name']}. Залишилось: {med['units'] - int(qty)} шт.")
                    else:
                        await reply(update, f"Недостатньо {med}. Доступно лише {medication['quantity']} шт.")
                    break
        else:
            await reply(f"Ліки '{med}' не знайдено в категорії '{category}'.")

        user_state[user_id] = None
    
    async def choosing_med_from_category(self, update: Update, user_id: str, med: str):
        user_state[user_id]['action'] = 'choosing_med_quantity'
        user_state[user_id]['med'] = med
        await update.message.reply_text(f"Ви обрали ліки: {med}\nТепер введіть к-сть ліків:")
        return
    
    async def choosing_category_for_med(self, update: Update, user_id: str, category: str):
        user_state[user_id] = {'action': 'adding_med', 'category': category}
        await update.message.reply_text(f"Ви обрали категорію: {category}\nТепер введіть назву ліків (наприклад: Аспірин - 10 - таблетка):")
        return
    
    async def adding_med(self, update: Update, user_id: str, text: str):
        medications = supabase.get_meds()
        category = user_state[user_id]['category']

        med_info = text.split("-")

        name = med_info[0].strip().lower()
        quantity = med_info[1].strip() if len(med_info) > 1 else 0
        format = med_info[2].strip() if len(med_info) > 1 else "-"

        found = False
        for med in medications:
            if med["name"].lower() == name.lower():
                supabase.update_data('medications', { "units": med['units'] + int(quantity) }, med["id"])
                found = True
                break

        if not found:
            supabase.insert_data('medications', {
                "name": name,
                "units": int(quantity),
                "format": format,
                "category": category
            })

        await update.message.reply_text(f"Ліки додано в категорію '{category}': {name} - {quantity} - {format}")
        user_state[user_id] = {}
        await reply(update)

    async def handle_input(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        text = update.message.text

        if user_state.get(user_id, {}).get('action') == 'adding_category':
            await self.adding_category(update, user_id)
            return
        elif user_state.get(user_id, {}).get('action') == 'choosing_category_for_med':
            await self.choosing_category_for_med(update, user_id, text)
            return
        elif user_state.get(user_id, {}).get('action') == 'choosing_category_for_take_med':
            await self.choosing_category_for_take_med(update, user_id, text)
            return
        elif user_state.get(user_id, {}).get('action') == 'choosing_med_from_category':
            await self.choosing_med_from_category(update, user_id, text)
            return
        elif user_state.get(user_id, {}).get('action') == 'choosing_med_quantity':
            await self.choosing_med_quantity(update, user_id, text)
            return
        elif user_state.get(user_id, {}).get('action') == 'adding_med':
            await self.adding_med(update, user_id, text)
            return
        else:
            await reply(update)
            return
    
handler = HandleInput()