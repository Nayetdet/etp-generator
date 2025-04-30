from config import Config
from pymongo import MongoClient

client = MongoClient(Config.DATABASE_URI, Config.DATABASE_PORT)
db = client.flask_database
etp_collection = db.etp
