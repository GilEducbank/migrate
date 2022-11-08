import psycopg2

import util


def connect(postgres_config):
    try:
        conn = psycopg2.connect(
            host=postgres_config["host"],
            database=postgres_config["database"],
            user=postgres_config["user"],
            password=postgres_config["password"],
            port=postgres_config["port"])

        print("Connect Successful to postgres")

        return conn
    except:
        print("Unable to connect to postgres DB.")


def close_connection(connection, cursor):
    print("Connection closed with postgres")
    cursor.close()
    connection.close()


# given a postgres connection, a DB name and list of fieldName, type, create a table, dropping if it already exists
def create_table(connection, table_name, fields_types):
    print("Creating table " + table_name)
    cursor = connection.cursor()
    drop_query = "DROP TABLE IF EXISTS \""+table_name+"\"; \n"
    create_table_query = "CREATE TABLE " + "\"" + table_name + "\"("

    items_to_add = []
    for item in fields_types:
        items_to_add.append(" \""+item+"\" " + util.map_types_by_type(fields_types[item]) + "\n")

    create_table_query += ','.join(items_to_add)
    create_table_query += ")"
    print(drop_query)
    print(create_table_query)

    final_query = drop_query + create_table_query
    cursor.execute(final_query)
    connection.commit()

def insert(table_name, fields_values):
    print("inserting row")
