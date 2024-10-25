from pymongo import MongoClient


__connection_string = ""
with open("mongoDB_connectionString") as f:
    connection_string = f.read()

__db_client = MongoClient(connection_string)
__db = __db_client['xgDB']

user_collection = __db['users']
task_collection = __db["task"]