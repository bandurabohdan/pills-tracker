import os
from dotenv import load_dotenv

load_dotenv()

from supabase import create_client, Client

url = os.getenv("SUPABASE_URL")
token =  os.getenv("SUPABASE_TOKEN")

class Supabase:
    def __init__(self):
        self.supabase: Client = create_client(url, token)

    def get_data(self, table):
        response = self.supabase.table(table).select("*").execute()
        return response

    def insert_data(self, table, data):
        response = self.supabase.table(table).insert(data).execute()
        return response

    def update_data(self, table, data, id):
        response = self.supabase.table(table).update(data).eq("id", id).execute()
        return response

    def delete_data(self, table, name):
        response = self.supabase.table(table).delete().eq("name", name).execute()
        return response
    
    def get_categories(self):
        categories = self.get_data('categories')
        return_cat = []
        for category in categories.data:
            return_cat.append(category['name'])

        return return_cat
    
    def get_meds(self):
        medications = self.get_data('medications')
        return_med = []
        for med in medications.data:
            return_med.append(med)

        return return_med

supabase = Supabase()