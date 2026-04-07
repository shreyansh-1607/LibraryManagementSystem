# type: ignore

import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {
    'user': 'root',
    'password': 'shreyansh@1607',
    'host': 'localhost',
    'database': 'Library'
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

