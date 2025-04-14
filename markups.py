from telegram import ReplyKeyboardMarkup
from supabase_client import supabase

user_state = {}

buttons_markup = ReplyKeyboardMarkup([['Додати категорію'], ['Додати ліки'], ['Вжити ліки'], ['Список ліків']], one_time_keyboard=True, resize_keyboard=True)

def categories_markup():
    categories = supabase.get_categories()
    return ReplyKeyboardMarkup([[category] for category in categories], one_time_keyboard=True, resize_keyboard=True)

def medications_markup(category: str):
    medications = supabase.get_meds()
    meds = []
    for med in medications:
        meds.append([f"{med['name']} - {med['units']} {med['format']}"])

    return ReplyKeyboardMarkup(meds, one_time_keyboard=True, resize_keyboard=True)