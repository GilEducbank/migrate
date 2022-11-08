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


# tables to export from mongodb
def tables_from_json():
    return config["tables"]


# transform each document in a collection to ber inserted into postgres DB
def treat_collection(inner_collection):
    treated_list = []
    for inner_item in inner_collection:
        treated_list.append(util.treat_document(inner_item))
    return treated_list


# create tables
def create_tables_and_insert(mongo_db):
    tables = tables_from_json()
    for table in tables:
        collection = mongo_db[table].find()
        treated_collection = treat_collection(collection)
        type_names_and_postgres_types = util.get_collection_types(treated_collection)
        postgres.create_table(postgres_conn, table, type_names_and_postgres_types)
        postgres.insert_many(postgres_conn, table, treated_collection)





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

    # create tables
    create_tables_and_insert(mongo_db)

    doc = mongo_db["AbpTenants"].find_one()
    treated_doc = util.treat_document(doc)
    postgres.insert(postgres_conn, "AbpTenants", treated_doc)

    postgres.close_connection(postgres_conn, postgres_cursor)
    mongo.close_connection(mongo_client)

    # use this to find field types in documents in each table (which is in the list tables variable)
    # types = dict()
    # for table in tables:
    #     collection = mongo_db[table].find()
    #     treated_collection = treat_collection(collection)
    #     for document in treated_collection:
    #         for field in document:
    #             if type(document[field]) in types and types[type(document[field])] is not None:
    #                 continue
    #             else:
    #                 types[type(document[field])] = type(document[field])
    #
    # for typ in types:
    #     print(types[typ])
