import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conectar():
    return psycopg2.connect(
        host="db.qmpmfxpskjyiseuzuond.supabase.co",
        database="postgres",
        user="postgres",
        password=os.getenv("DB_PASSWORD"),
        port="5432"
    )
