from collections import defaultdict

from telegram import Update
from telegram.ext import CallbackContext

from handlers.reply import reply
from supabase_client import supabase


async def list_med(update: Update, context: CallbackContext):
    medications = supabase.get_meds()
    if not medications:
        await reply(update, "Список медикаментів порожній.")
        return

    categorized = defaultdict(list)
    for med in medications:
        category = med.get("category", "Без категорії")
        categorized[category].append(med)

    message = ""
    for category, meds in categorized.items():
        message += f"\n<b>{category}</b>:\n"
        for med in meds:
            message += f"• {med['name']} — {med['units']} {med['format']}\n"

    await reply(update, message, parse_mode="HTML")
