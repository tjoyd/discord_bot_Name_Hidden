import pymongo
from pymongo import MongoClient
import urllib.parse
import os


try:
    mango_url = "mongodb+srv://" + os.environ['user'] + ":" + urllib.parse.quote_plus(os.environ['password']) + os.environ['cluster']
    cluster = MongoClient(mango_url)
    db = cluster[os.environ['database']]
    collection = db[os.environ['collec']]
    banlist = db['Bans']
    levelxp = db['levelxp']
    levelroleDb = db['LevelRoles']
    giveawayDB = db['Giveaway']
    globalDB = db['Global']
    print('Data Loaded')
except Exception as e:
    print(e)
    print("Data can't be Loaded")

