import psycopg2


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
