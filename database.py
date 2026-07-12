import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    else:
        raise Exception("DATABASE_URL not found")


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()


    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)


    # Income Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income(
        id SERIAL PRIMARY KEY,
        date TEXT,
        amount REAL,
        source TEXT,
        notes TEXT
    )
    """)


    # Expense Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id SERIAL PRIMARY KEY,
        date TEXT,
        category TEXT,
        amount REAL,
        payment_method TEXT,
        notes TEXT
    )
    """)


    # Investment Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investments(
        id SERIAL PRIMARY KEY,
        name TEXT,
        purchase_date TEXT,
        amount REAL,
        current_value REAL
    )
    """)


    # Borrow Given Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow_given(
        id SERIAL PRIMARY KEY,
        name TEXT,
        date TEXT,
        amount REAL,
        outstanding REAL,
        due_date TEXT,
        payment_status TEXT,
        notes TEXT
    )
    """)
# Borrow Taken Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS borrow_taken(
    id SERIAL PRIMARY KEY,
    name TEXT,
    date TEXT,
    amount REAL,
    outstanding REAL,
    due_date TEXT,
    payment_status TEXT,
    notes TEXT
)
""")

    conn.commit()
    cursor.close()
    conn.close()
