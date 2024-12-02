import time
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rss_user:rss_password@db/rss_reader")

while True:
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        print("Database is ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for database...")
        time.sleep(1)
