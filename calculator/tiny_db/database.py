from tinydb import TinyDB

db = TinyDB('tinydb.json')

table = db.table('collections')
