import sqlite3
from datetime import date

def get_db(name="main.db"):
    """
    Establishes a connection to the SQLite database.

    Args:
        name (str): The name of the database file.
    Returns:
        sqlite3.Connection: The connection object to the SQLite database.
    """
    db = sqlite3.connect(name)
    return db

def create_tables(db):
    """
    Creates the necessary tables in the SQLite database if they don't already exist.
    Args:
        db (sqlite3.Connection): The connection object to the database.
    """
    cur = db.cursor()

    # Create the habits table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            name TEXT PRIMARY KEY,
            description TEXT,
            periodicity TEXT
        )
    """)

    # Create the tracker table (to track when a habit was completed)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tracker (
            completion_date TEXT,
            habit_name TEXT,
            FOREIGN KEY (habit_name) REFERENCES habits(name)
        )
    """)

    db.commit()

def add_habit(db, name, description, periodicity):
    """
    Adds a new habit to the habits table.
    Args:
        db (sqlite3.Connection): The connection object to the database.
        name (str): The name of the habit.
        description (str): A description of the habit.
        periodicity (str): The periodicity of the habit (e.g., 'daily' or 'weekly').
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES (?, ?, ?)", (name, description, periodicity))
    db.commit()

def check_off_habit(db, name, completion_date=None):
    """
    Marks a habit as completed by adding an entry to the tracker table.
    Args:
        db (sqlite3.Connection): The connection object to the database.
        name (str): The name of the habit being completed.
        completion_date (str): The date when the habit was completed (defaults to today).
    """
    cur = db.cursor()

    if not completion_date:
        completion_date = date.today().isoformat()  # Defaults to today's date in YYYY-MM-DD format

    cur.execute("INSERT INTO tracker VALUES (?, ?)", (completion_date, name))
    db.commit()

def get_habits(db):
    """
    Retrieves all habits from the habits table.
    Args:
        db (sqlite3.Connection): The connection object to the database.
    Returns:
        list: A list of tuples containing the name, description, and periodicity of each habit.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    return cur.fetchall()

def get_habit_completion_dates(db, name):
    """
    Retrieves all completion dates for a given habit.
    Args:
        db (sqlite3.Connection): The connection object to the database.
        name (str): The name of the habit.
    Returns:
        list: A list of completion dates for the given habit.
    """
    cur = db.cursor()
    cur.execute("SELECT completion_date FROM tracker WHERE habit_name = ?", (name,))
    return cur.fetchall()

def delete_habit(db, name):
    """
    Deletes a habit from the habits table and all associated completion records from the tracker table.
    Args:
        db (sqlite3.Connection): The connection object to the database.
        name (str): The name of the habit to delete.
    """
    cur = db.cursor()
    cur.execute("DELETE FROM tracker WHERE habit_name = ?", (name,))
    cur.execute("DELETE FROM habits WHERE name = ?", (name,))
    db.commit()
