import pymongo

myclient = pymongo.MongoClient("mongodb://rootuser:your_mongodb_password@172.18.128.3:27017")

mydb = myclient["soft_prac"]

print(myclient.list_database_names())

