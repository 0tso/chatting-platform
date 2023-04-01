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
# with db.connection() as cursor:
class Connection:
    def __enter__(self):
        self.conn = connection_pool.getconn()
        self.cur = self.conn.cursor()
        return self.cur
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.commit()
        self.cur.close()
        connection_pool.putconn(self.conn)