import json
import mongo
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
    db = mongo.get_database(config["URI"])
    tables = tables_from_json()

    collection = db["Invoices"].find()

    test_list = treat_collection(collection)

    print(tables)

    #mongo.insert_collection(db, test_list)

