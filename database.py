import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "database")
DB_NAME = os.environ.get("DB_NAME", "finance.db")
DATABASE_URL = os.environ.get("DATABASE_URL")
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(DB_FOLDER, DB_NAME))
USE_POSTGRES = os.environ.get("USE_POSTGRES", "").lower() in {"1", "true", "yes", "on"} and bool(DATABASE_URL)

os.makedirs(DB_FOLDER, exist_ok=True)


class DBCursor:

    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        if USE_POSTGRES and params is not None:
            query = query.replace("?", "%s")
        if USE_POSTGRES:
            if params is None:
                return self.cursor.execute(query, prepare=False)
            return self.cursor.execute(query, params, prepare=False)
        if params is None:
            return self.cursor.execute(query)
        return self.cursor.execute(query, params)

    def executemany(self, query, seq_of_params):
        if USE_POSTGRES:
            query = query.replace("?", "%s")
            return self.cursor.executemany(query, seq_of_params, prepare=False)
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
        try:
            import psycopg
            conn = psycopg.connect(
                DATABASE_URL,
                sslmode="require",
                prepare_threshold=0,
            )
            return DBConnection(conn)
        except Exception:
            pass
    return DBConnection(sqlite3.connect(DB_PATH))


def _column_exists(conn, table_name, column_name):
    cursor = conn.cursor()
    if USE_POSTGRES:
        cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
            (table_name,),
        )
        rows = cursor.fetchall()
        return any(row[0] == column_name for row in rows)
    cursor.execute(f"PRAGMA table_info({table_name})")
    rows = cursor.fetchall()
    return any(row[1] == column_name for row in rows)


def _add_column_if_missing(conn, table_name, column_name, definition):
    if _column_exists(conn, table_name, column_name):
        return
    if USE_POSTGRES:
        conn.cursor().execute(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {definition}")
    else:
        conn.cursor().execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    if USE_POSTGRES:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        _add_column_if_missing(conn, "users", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT,
                type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_methods (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT,
                type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                date TEXT,
                amount REAL,
                source TEXT,
                payment_method TEXT,
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
                current_value REAL,
                investment_type TEXT,
                payment_method TEXT,
                notes TEXT
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
                payment_method TEXT,
                notes TEXT,
                received_amount REAL,
                collection_date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_taken (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name TEXT,
                date TEXT,
                amount REAL,
                outstanding REAL,
                due_date TEXT,
                payment_status TEXT,
                payment_method TEXT,
                notes TEXT,
                repaid_amount REAL,
                repayment_date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_received (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                borrow_given_id BIGINT,
                date TEXT,
                amount REAL,
                payment_method TEXT,
                notes TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_repaid (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                borrow_taken_id BIGINT,
                date TEXT,
                amount REAL,
                payment_method TEXT,
                notes TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO users(username, password) VALUES (%s,%s) ON CONFLICT (username) DO NOTHING",
            ("admin", hash_password("admin123")),
        )
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                created_at TEXT
            )
        """)
        _add_column_if_missing(conn, "users", "created_at", "TEXT")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings(
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_methods(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                source TEXT,
                payment_method TEXT,
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
                current_value REAL,
                investment_type TEXT,
                payment_method TEXT,
                notes TEXT
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
                payment_method TEXT,
                notes TEXT,
                received_amount REAL,
                collection_date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_taken(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date TEXT,
                amount REAL,
                outstanding REAL,
                due_date TEXT,
                payment_status TEXT,
                payment_method TEXT,
                notes TEXT,
                repaid_amount REAL,
                repayment_date TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_received(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                borrow_given_id INTEGER,
                date TEXT,
                amount REAL,
                payment_method TEXT,
                notes TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrow_repaid(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                borrow_taken_id INTEGER,
                date TEXT,
                amount REAL,
                payment_method TEXT,
                notes TEXT
            )
        """)
        cursor.execute(
            "INSERT OR IGNORE INTO users(username, password, created_at) VALUES (?,?,?)",
            ("admin", hash_password("admin123"), datetime.utcnow().isoformat()),
        )

    _add_column_if_missing(conn, "income", "source", "TEXT")
    _add_column_if_missing(conn, "income", "payment_method", "TEXT")
    _add_column_if_missing(conn, "income", "notes", "TEXT")
    _add_column_if_missing(conn, "expenses", "category", "TEXT")
    _add_column_if_missing(conn, "expenses", "payment_method", "TEXT")
    _add_column_if_missing(conn, "expenses", "notes", "TEXT")
    _add_column_if_missing(conn, "investments", "current_value", "REAL")
    _add_column_if_missing(conn, "investments", "investment_type", "TEXT")
    _add_column_if_missing(conn, "investments", "payment_method", "TEXT")
    _add_column_if_missing(conn, "investments", "notes", "TEXT")
    _add_column_if_missing(conn, "borrow_given", "outstanding", "REAL")
    _add_column_if_missing(conn, "borrow_given", "payment_method", "TEXT")
    _add_column_if_missing(conn, "borrow_given", "notes", "TEXT")
    _add_column_if_missing(conn, "borrow_given", "received_amount", "REAL")
    _add_column_if_missing(conn, "borrow_given", "collection_date", "TEXT")
    _add_column_if_missing(conn, "borrow_taken", "outstanding", "REAL")
    _add_column_if_missing(conn, "borrow_taken", "payment_method", "TEXT")
    _add_column_if_missing(conn, "borrow_taken", "notes", "TEXT")
    _add_column_if_missing(conn, "borrow_taken", "repaid_amount", "REAL")
    _add_column_if_missing(conn, "borrow_taken", "repayment_date", "TEXT")

    cursor.execute("UPDATE borrow_given SET outstanding=amount WHERE outstanding IS NULL")
    cursor.execute("UPDATE borrow_taken SET outstanding=amount WHERE outstanding IS NULL")
    cursor.execute("UPDATE borrow_given SET received_amount=0 WHERE received_amount IS NULL")
    cursor.execute("UPDATE borrow_taken SET repaid_amount=0 WHERE repaid_amount IS NULL")

    default_categories = [
        ("Salary", "income"),
        ("Business", "income"),
        ("Food", "expense"),
        ("Fuel", "expense"),
        ("Shopping", "expense"),
        ("Utilities", "expense"),
        ("Rent", "expense"),
        ("Medical", "expense"),
        ("Education", "expense"),
        ("Travel", "expense"),
        ("Entertainment", "expense"),
        ("Other", "expense"),
    ]
    for name, type_ in default_categories:
        cursor.execute("INSERT OR IGNORE INTO categories(name, type) VALUES (?,?)", (name, type_))

    default_payment_methods = [
        ("Cash", "all"),
        ("Bank Account", "all"),
        ("Credit Card", "expense"),
    ]
    for name, type_ in default_payment_methods:
        cursor.execute("INSERT OR IGNORE INTO payment_methods(name, type) VALUES (?,?)", (name, type_))

    cursor.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?,?)", ("currency_symbol", "AED"))
    cursor.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?,?)", ("theme_mode", "light"))
    cursor.execute("INSERT OR IGNORE INTO settings(key, value) VALUES (?,?)", ("backup_path", os.path.join(DB_FOLDER, "backups")))

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    import hashlib
    import os
    import binascii

    salt = os.urandom(16)
    iterations = 310000
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256${iterations}${binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"


def verify_password(password: str, password_hash: str) -> bool:
    import hashlib
    import binascii

    if not password_hash or "$" not in password_hash:
        return False
    algorithm, iterations, salt_hex, hash_hex = password_hash.split("$")
    if algorithm != "pbkdf2_sha256":
        return False
    salt = binascii.unhexlify(salt_hex)
    expected = binascii.unhexlify(hash_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
    return hashlib.compare_digest(dk, expected)


def get_setting(key, default=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default


def set_setting(key, value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings(key, value) VALUES (?,?)", (key, str(value)))
    conn.commit()
    conn.close()


def backup_database():
    import shutil

    backup_dir = get_setting("backup_path", os.path.join(DB_FOLDER, "backups"))
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"finance_backup_{timestamp}.db")
    if USE_POSTGRES:
        raise RuntimeError("Backup is not supported for Postgres from the local app flow.")
    shutil.copy2(DB_PATH, backup_file)
    return backup_file


def restore_database(backup_path):
    import shutil

    if USE_POSTGRES:
        raise RuntimeError("Restore is not supported for Postgres from the local app flow.")
    if not os.path.exists(backup_path):
        raise FileNotFoundError("Backup file does not exist.")
    shutil.copy2(backup_path, DB_PATH)
    return DB_PATH
