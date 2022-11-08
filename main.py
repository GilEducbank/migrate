import json
import mongo
import postgres
import util


# loads json file with configurations
def load_config():
    with open('config.json') as json_file:
        return json.load(json_file)


# global variable that holds json dictionary values for configuration
config = load_config()


def tables_from_json():
    return config["tables"]


def treat_collection(inner_collection):
    treated_list = []
    for inner_item in inner_collection:
        treated_list.append(util.treat_document(inner_item))
    return treated_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # connect to mongo client and get database
    mongo_client = mongo.get_client(config["mongo"])
    mongo_db = mongo_client[config["mongo"]["database"]]
    # connect to postgres and get the database cursor
    postgres_conn = postgres.connect(config["postgres"])
    postgres_cursor = postgres_conn.cursor()
    # get tables to work with
    tables = tables_from_json()

    collection = mongo_db["Invoices"].find()

    test_list = treat_collection(collection)
    print(test_list)

    # close clients
    postgres.close_connection(postgres_conn, postgres_cursor)
    mongo.close_connection(mongo_client)



