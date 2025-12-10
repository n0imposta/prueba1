import mysql.connector
from mysql.connector import Error

def get_connection(config):
    """Retorna SIEMPRE una conexión nueva a MySQL"""
    try:
        conn = mysql.connector.connect(
            host=config["db_host"],
            user=config["db_user"],
            password=config["db_pass"],
            database=config["db_name"],
            autocommit=True
        )
        return conn
    except Error as e:
        print("❌ Error MySQL:", e)
        return None
