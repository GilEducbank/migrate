import json
import mongo
import util


def tables_from_json():
    with open('config.json') as json_file:
        data = json.load(json_file)
    return data["tables"]


def treat_collection(inner_collection):
    treated_list = []
    for inner_item in inner_collection:
        treated_list.append(util.treat_document(inner_item))
    return treated_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db = mongo.get_database()
    tables = tables_from_json()

    collection = db["Invoices"].find()

    test_list = treat_collection(collection)

    print(tables)

    mongo.insert_collection(db, test_list)

