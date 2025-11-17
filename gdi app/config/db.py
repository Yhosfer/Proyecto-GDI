# config/db.py
import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_conn():
    """
    Devuelve una conexión a MySQL.
    """
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="colegiopalermo",
        charset="utf8mb4"
    )
    try:
        yield cnx
    finally:
        cnx.close()
