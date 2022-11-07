import pymongo


def get_database(uri):
    client = pymongo.MongoClient(uri)
    print("Connect Successful")
    print(client.list_database_names())
    mydb = client["educbank"]
    return mydb


def insert_collection(db, collection):
    db.create_collection("teste")
    for out_item in collection:
        db["teste"].insert_one(out_item)
