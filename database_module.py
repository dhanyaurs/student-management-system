import os
import pymysql
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv

# 1. Load the hidden credentials from your .env file into temporary memory
load_dotenv()

# 2. Extract the credentials safely
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "student_db")

# 3. Initialize a secure, reusable connection pool (The Taxi Stand)
# We use standard PyMySQL DictCursor so database rows return as clean dictionaries
try:
    db_pool = PooledDB(
        creator=pymysql,
        maxconnections=5,       # Keep up to 5 permanent connections active
        mincached=2,            # Always keep at least 2 connections ready in the background
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    print("🚀 Cloud database connection pool initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize database connection pool: {e}")
    db_pool = None

def create_connection():
    """
    Borrows an active connection from our pool.
    This integrates seamlessly with your other modules!
    """
    if db_pool:
        return db_pool.connection()
    raise Exception("Database connection pool is offline.")
