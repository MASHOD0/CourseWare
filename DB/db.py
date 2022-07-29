from psycopg2 import connect

import cred as c


def fypDB_Connect():
    try:
        conn = connect(
            database=c.DATABASE,
            user=c.USER,
            password=c.PASSWORD,
            host=c.HOST,
            port=c.PORT
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
