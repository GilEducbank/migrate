import pymongo

def get_client(mongo_config):
    client = pymongo.MongoClient(mongo_config["URI"])
    print("Connect Successful to mongodb")
    return client

def get_database(uri):
    client = pymongo.MongoClient(uri)
    print("Connect Successful to mongodb")
    mydb = client["educbank"]
    return mydb


def insert_collection(db, collection):
    db.create_collection("teste")
    for out_item in collection:
        db["teste"].insert_one(out_item)


def close_connection(client):
    print("Connection closed with mongo Client")
    client.close()
