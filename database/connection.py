import psycopg2
from config import DB_CONFIG


def get_database_connection():
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Database connection error: {error}")
        return None


def initialise_database():
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        print("🛠️  Initialising database...")
        # check if Database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (DB_CONFIG["dbname"],))
        exists = cursor.fetchone()
        if not exists:
            print(f"Database '{DB_CONFIG['dbname']}' not found, creating...")
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['dbname']};")
        else:
            print(f"Database '{DB_CONFIG['dbname']}' already exists.")

        # create tables if not exists.
        with open("database/schema.sql", "r") as schema:
            cursor.execute(schema.read())
        conn.commit()
        print("All tables are created..")
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
