import psycopg2
from config.config import DBConfig

def execute(query: str):
    """
    Execute a SQL query on the database.
    """
    conn = psycopg2.connect(
        host=DBConfig.HOST,
        database=DBConfig.DATABASE,
        user=DBConfig.USER,
        password=DBConfig.PASSWORD
    )

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        cursor.close()
        conn.close()