import mariadb
import logging

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "travel_planner",
    "port": 3306
}


def get_connection():
    """Return a MariaDB connection, or None if unavailable."""
    try:
        conn = mariadb.connect(**DB_CONFIG)
        return conn
    except mariadb.Error as e:
        logging.warning(f"[DB] Could not connect to database: {e}")
        return None


def init_db():
    """Create the database and trips table if they don't exist."""
    try:
        conn = mariadb.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS travel_planner")
        cursor.execute("USE travel_planner")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id          INT AUTO_INCREMENT PRIMARY KEY,
                destination VARCHAR(255),
                start_date  DATE,
                end_date    DATE,
                people      INT,
                budget      VARCHAR(50),
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("[DB] Database initialised successfully.")
    except mariadb.Error as e:
        logging.warning(f"[DB] Could not initialise database: {e}")


def save_trip(destination, start_date, end_date, people, budget):
    """Insert a trip record. Returns the new row id, or None on failure."""
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO trips (destination, start_date, end_date, people, budget)
            VALUES (?, ?, ?, ?, ?)
            """,
            (destination, start_date, end_date, people, budget)
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id
    except mariadb.Error as e:
        logging.warning(f"[DB] Could not save trip: {e}")
        return None


def get_all_trips():
    """Return all trips as a list of dicts, or an empty list on failure."""
    conn = get_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, destination, start_date, end_date, people, budget, created_at FROM trips ORDER BY created_at DESC"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            for key in ("start_date", "end_date", "created_at"):
                if row[key] is not None:
                    row[key] = str(row[key])
        return rows
    except mariadb.Error as e:
        logging.warning(f"[DB] Could not fetch trips: {e}")
        return []
