import sqlite3
from habit import Habit
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name="habit_tracker.db"):
        """Initialize the database connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Create habits and completions tables."""
        self.conn.execute('''CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            periodicity TEXT,
            creation_date DATE
        )''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completion_date DATE,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )''')
        self.conn.commit()

    def save_habit(self, habit):
        self.conn.execute('''INSERT INTO habits (name, description, periodicity, creation_date)
                                 VALUES (?, ?, ?, ?)''',
                          (habit.get_name(), habit.get_description(), habit.get_periodicity(),
                           habit.get_creation_date()))
        habit_id = self.conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        self.conn.commit()
        return habit_id

    def save_completion(self, habit_id, completion_date):
        """Saves the completion date for a specific habit in the completions table."""
        self.conn.execute('''INSERT INTO completions (habit_id, completion_date)
                             VALUES (?, ?)''', (habit_id, completion_date))
        self.conn.commit()

    def load_habits(self):
        """Load all habits and their completion dates from the database."""
        habits = []
        cursor = self.conn.execute('SELECT * FROM habits')
        habit_data = cursor.fetchall()
        for row in habit_data:
            habit = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'periodicity': row[3],
                'creation_date': row[4],
                'completions': self.load_completions(row[0])
            }
            habits.append(habit)
        return habits

    def load_completions(self, habit_id):
        """Load all completion dates for a specific habit."""
        cursor = self.conn.execute('SELECT completion_date FROM completions WHERE habit_id = ?', (habit_id,))
        completions = [row[0] for row in cursor.fetchall()]
        return completions

    def delete_habit(self, habit_id):
        """Delete a habit and its completions from the database."""
        self.conn.execute('DELETE FROM completions WHERE habit_id = ?', (habit_id,))
        self.conn.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
        self.conn.commit()

    def get_habit_id(self, name):
        """Retrieve the habit_id by habit name."""
        cursor = self.conn.execute('SELECT id FROM habits WHERE name = ?', (name,))
        result = cursor.fetchone()
        return result[0] if result else None


def initialize_predefined_habits(db):
    """Function to initialize the database with predefined habits and example tracking data."""

    # Check if the database is empty
    if not db.load_habits():
        print("Initializing predefined habits...")

        # Define the predefined habits
        habits = [
            Habit("Exercise", "Weekly Exercise", "weekly"),
            Habit("Read", "Read every day", "daily"),
            Habit("Meditate", "Daily meditation", "daily"),
            Habit("Art Class", "Attend weekly art class", "weekly"),
            Habit("Learn French", "Daily French lesson", "daily")
        ]

        # Simulate completion data over the last 4 weeks
        for habit in habits:
            if habit.get_periodicity() == "daily":
                # Add 28 consecutive days of completion for daily habits
                for i in range(28):
                    habit.complete_habit(datetime.now() - timedelta(days=i))
            elif habit.get_periodicity() == "weekly":
                # Add 4 consecutive weeks of completion for weekly habits
                for i in range(4):
                    habit.complete_habit(datetime.now() - timedelta(weeks=i))

            # Save the habit to the database
            db.save_habit(habit)

        print("Predefined habits initialized.")
    else:
        print("Habits already exist in the database.")


