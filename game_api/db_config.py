import os
import psycopg
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def get_connection():
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    return conn
