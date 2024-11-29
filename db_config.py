#python与mysql连接
import mysql.connector

db_config = {
    'user': 'QRH',
    'password': 'abc.1234',
    'host': '47.115.226.248',
    'port': '3306',
    'database': 'restrount'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)