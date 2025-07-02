import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="task_manager",
        user="postgres",
        password="admin123"
    )
    conn.autocommit = True
    return conn
