from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['new_year_toys_db']

toys = db['toys']  # Коллекции игрушек пользователей

results = db['results']  # Результаты рассчетов для пользователей
