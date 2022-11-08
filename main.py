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

    collection = mongo_db["Holidays"].find()

    treated_collection = treat_collection(collection)

    test = util.get_collection_types(treated_collection)

    postgres.create_table(postgres_conn, "Holidays", test)




    #first = test_list[0]
    #for item in first:
    #     print(item)
    #     print(first[item])
    #     print(type(first[item]))
    #     print(util.map_types_explicit(first[item]))
    #     print()
    # query_create_table = """CREATE TABLE IF NOT EXISTS tableTest (id SERIAL PRIMARY KEY, model VARCHAR(255) NOT NULL, price INTEGER)"""
    # query_test = """Insert into tableTest (id, model, price) values (%s,%s,%s)"""
    # record_to_insert = (5, 'OnePlus', 950)
    # postgres_cursor.execute(query_create_table)
    # postgres_cursor.execute(query_test, record_to_insert)
    # postgres_conn.commit()
    # close clients
    postgres.close_connection(postgres_conn, postgres_cursor)
    mongo.close_connection(mongo_client)



