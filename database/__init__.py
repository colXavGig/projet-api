from pymongo import MongoClient
from .db import Database
import app_config as config

database = Database(connectrion_string = config.CONST_MONGO_URL, database_name = config.CONST_DATABASE)
database.connect()

user_collection = database.database[config.CONST_USER_COLLECTION]
task_collection = database.database[config.CONST_TASK_COLLECTION]