from psycopg2 import pool
from config.settings import DB

_connection = None


def init_pool():
    global _connection
    if not _connection:
        _connection = pool.SimpleConnectionPool(1, 5, **DB)


def get_conn():
    return _connection.getconn()


def put_conn(conn):
    _connection.putconn(conn)


def close_pool():
    _connection.closeall()
