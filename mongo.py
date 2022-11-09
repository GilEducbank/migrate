import pymongo


# get mongo client
def get_client(mongo_config):
    client = pymongo.MongoClient(mongo_config["URI"])
    print("Connect Successful to mongodb")
    return client


# Close mongo db connection
def close_connection(client):
    print("Connection closed with mongo Client")
    client.close()
