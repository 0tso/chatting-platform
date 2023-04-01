import psycopg2
from psycopg2 import pool
from os import getenv

# A connection pool to make database access more efficient
connection_pool = psycopg2.pool.ThreadedConnectionPool(minconn=getenv("MIN_CONN"),
                                                       maxconn=getenv("MAX_CONN"),
                                                       user=getenv("DB_USER"),
                                                       password=getenv("DB_PASSWORD"),
                                                       database=getenv("DATABASE"),
                                                       host=getenv("HOST"))

# Recommended usage:
# with db.Connection() as conn, conn.cursor() as cur:
class Connection:
    def __enter__(self):
        self.conn = connection_pool.getconn()
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.commit()
        connection_pool.putconn(self.conn)

    def cursor(self):
        return self.conn.cursor()