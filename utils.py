import os
import yaml
from pymongo import MongoClient
from urllib.parse import quote
def get_client():
    """This method gets a handle to the database server"""
    with open(os.path.dirname(os.path.realpath(__file__)) + "/config.yml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    endpoint = "mongodb+srv://" + config["database"]["username"] + ":" + quote(config["database"]["password"]) + "@" + config["database"]["endpoint"]
    client = MongoClient(endpoint)
    return client

# client=get_client()
# db_handle = client.main
# users_collection = db_handle.users
# print(users_collection)
# print("in")