from psycopg2 import connect

DATABASE = "fyp-ver2"
USER = "postgres"
PASSWORD = "postgres"
HOST = "127.0.0.1"
PORT = "5432"


def fypDB_Connect():
    try:
        conn = connect(
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        print("Opened database successfully")
        return conn
    except Exception as e:
        print(e)


def cursor(conn):
    try:
        cur = conn.cursor()
        print("Cursor generated")
        return cur
    except Exception as e:
        print(e)


def commit(conn):
    try:
        conn.commit()
        print('query commited')
    except Exception as e:
        print(e)


def execute(conn, query):
    try:
        cur = cursor(conn)
        cur.execute(query)
        print("Query Executed.")
        commit(conn)
    except Exception as e:
        print(e)


def fetch(conn, query):
    try:

        cur = cursor(conn)
        cur.execute(query)
        rows = cur.fetchall()
        print('query fetched')
        return rows

    except Exception as e:
        print(e)


def close(conn):
    try:
        conn.close()
        print('connection closed')
    except Exception as e:
        print(e)
