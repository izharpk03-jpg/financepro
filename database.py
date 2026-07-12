import os
import sqlite3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "database")
DB_NAME = os.environ.get("DB_NAME", "finance.db")
DATABASE_URL = os.environ.get("DATABASE_URL")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(DB_FOLDER, DB_NAME))
USE_POSTGRES = bool(DATABASE_URL)


os.makedirs(DB_FOLDER, exist_ok=True)


class DBCursor:

    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        if USE_POSTGRES and params is not None:
            query = query.replace("?", "%s")
        if params is None:
            return self.cursor.execute(query)
        return self.cursor.execute(query, params)

    def executemany(self, query, seq_of_params):
        if USE_POSTGRES:
            query = query.replace("?", "%s")
        return self.cursor.executemany(query, seq_of_params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def __getattr__(self, name):
        return getattr(self.cursor, name)


class DBConnection:

    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return DBCursor(self.conn.cursor())

    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()

    def __getattr__(self, name):
        return getattr(self.conn, name)


def get_connection():

    if USE_POSTGRES:
        import psycopg
        return DBConnection(psycopg.connect(DATABASE_URL, sslmode="require"))
    return DBConnection(sqlite3.connect(DB_PATH))


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    if USE_POSTGRES:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            date TEXT,
            amount REAL,
            source TEXT,
            notes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            date TEXT,
            category TEXT,
            amount REAL,
            payment_method TEXT,
            notes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name TEXT,
            purchase_date TEXT,
            amount REAL,
            current_value REAL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_given (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name TEXT,
            date TEXT,
            amount REAL,
            outstanding REAL,
            due_date TEXT,
            payment_status TEXT,
            notes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_taken (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name TEXT,
            date TEXT,
            amount REAL,
            due_date TEXT,
            payment_status TEXT,
            notes TEXT
        )
        """)

        cursor.execute("ALTER TABLE borrow_given ADD COLUMN IF NOT EXISTS outstanding REAL")
        cursor.execute("UPDATE borrow_given SET outstanding=amount WHERE outstanding IS NULL")

        cursor.execute("""
        INSERT INTO users(username,password)
        VALUES (%s,%s)
        ON CONFLICT (username) DO NOTHING
        """,
        ("admin","admin123")
        )

    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS income(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            source TEXT,
            notes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            payment_method TEXT,
            notes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            purchase_date TEXT,
            amount REAL,
            current_value REAL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_given(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            amount REAL,
            outstanding REAL,
            due_date TEXT,
            payment_status TEXT,
            notes TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_taken(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date TEXT,
            amount REAL,
            due_date TEXT,
            payment_status TEXT,
            notes TEXT
        )
        """)

        try:
            cursor.execute("ALTER TABLE borrow_given ADD COLUMN outstanding REAL")
        except Exception:
            pass
        cursor.execute("UPDATE borrow_given SET outstanding=amount WHERE outstanding IS NULL")

        cursor.execute("""
        INSERT OR IGNORE INTO users(username,password)
        VALUES (?,?)
        """,
        ("admin","admin123")
        )

    conn.commit()
    conn.close()