import sqlite3
import os


DB_FOLDER = "database"
DB_NAME = "finance.db"


os.makedirs(DB_FOLDER, exist_ok=True)


DB_PATH = os.path.join(DB_FOLDER, DB_NAME)



def get_connection():

    return sqlite3.connect(DB_PATH)



def create_tables():

    conn = get_connection()
    cursor = conn.cursor()


    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)


    # Income Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amount REAL,
        source TEXT,
        notes TEXT
    )
    """)


    # Expense Table
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


    # Investment Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS investments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        purchase_date TEXT,
        amount REAL,
        current_value REAL
    )
    """)

    # Borrow Given Table
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
    try:
        cursor.execute("ALTER TABLE borrow_given ADD COLUMN outstanding REAL")
    except Exception:
        pass
    cursor.execute("UPDATE borrow_given SET outstanding=amount WHERE outstanding IS NULL")

    # Borrow Taken Table
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


    # Create Default User

    cursor.execute("""
    INSERT OR IGNORE INTO users(username,password)
    VALUES (?,?)
    """,
    ("admin","admin123")
    )


    conn.commit()
    conn.close()