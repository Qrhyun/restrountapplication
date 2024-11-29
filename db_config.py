from mysql.connector import pooling
db_config = {
    'user': 'restrount',
    'password': 'abc.123',
    'host': '47.115.226.248',
    'port': '3306',
    'database': 'restrount'
}
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=10,
    **db_config
)

def get_db_connection():
    return connection_pool.get_connection()
