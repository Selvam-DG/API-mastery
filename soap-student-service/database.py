import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")  # Auto-create if not exists
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")

# Encode the password
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

def get_postgres_engine():
    default_db = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/postgres"
    target_db = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(target_db)
    
    # Try to connect to target DB
    try:
        engine = create_engine(target_db)
        engine.connect()
        print(f"[INFO] Connected to existing database: {DB_NAME}")
        return engine
    except OperationalError:
        print(f"[WARN] Database '{DB_NAME}' not found. Creating .....")
        
        conn = psycopg2.connect(default_db)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        cur.close()
        conn.close()
        print(f"[INFO] Database '{DB_NAME}' created successfully. ")
        return create_engine(target_db)

engine = get_postgres_engine()
print(engine)