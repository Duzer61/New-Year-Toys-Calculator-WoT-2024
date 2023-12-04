from tinydb import Query, TinyDB

db = TinyDB('tinydb.json')

table = db.table('toys')
