import sqlite3
from habit import Habit
from datetime import datetime

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

    def habit_exists(self, name):
        """Check if a habit with the given name exists in the database."""
        cursor = self.conn.execute('SELECT id FROM habits WHERE name = ?', (name,))
        result = cursor.fetchone()
        return result is not None  # Returns True if the habit exists, False otherwise

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
                             VALUES (?, ?)''', (habit_id, completion_date.strftime("%Y-%m-%d %H:%M:%S")))
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
                'completions': self.load_completions(row[0])  # Ensure completions are properly loaded
            }
            habits.append(habit)
        return habits

    def load_completions(self, habit_id):
        """Load all completion dates for a specific habit."""
        cursor = self.conn.execute('SELECT completion_date FROM completions WHERE habit_id = ?', (habit_id,))
        completions = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in cursor.fetchall()]
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

    def insert_test_data(self):
        # Insert sample data for habits
        sample_data = {
            "Exercise": [
                "2023-09-03 10:00:00",  # Correct consecutive weekly data
                "2023-09-12 10:00:00",
                "2023-09-19 10:00:00"
            ],
            "Read": [
                "2023-09-15 10:00:00",  # Consecutive daily data
                "2023-09-16 10:00:00",
                "2023-09-17 10:00:00"
            ],
            "Meditate": [
                "2023-09-15 10:00:00",  # Consecutive daily data
                "2023-09-16 10:00:00",
                "2023-09-17 10:00:00"
            ],
            "Art Class": [
                "2023-08-24 10:00:00",  # Correct consecutive weekly data
                "2023-09-02 10:00:00",
                "2023-09-10 10:00:00",
                "2023-09-18 10:00:00"
            ],
            "Learn French": [
                "2023-09-15 10:00:00",  # Consecutive daily data
                "2023-09-16 10:00:00",
                "2023-09-17 10:00:00"
            ]
        }

        for habit_name, dates in sample_data.items():
            habit_id = self.get_habit_id(habit_name)
            if habit_id is not None:
                for date_str in dates:
                    completion_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    self.save_completion(habit_id, completion_date)


def initialize_predefined_habits(db):
    """Ensure predefined habits always exist in the database and load sample tracking data."""

    predefined_habits = [
        {"name": "Exercise", "description": "Weekly Exercise", "periodicity": "weekly"},
        {"name": "Read", "description": "Read every day", "periodicity": "daily"},
        {"name": "Meditate", "description": "Daily meditation", "periodicity": "daily"},
        {"name": "Art Class", "description": "Attend weekly art class", "periodicity": "weekly"},
        {"name": "Learn French", "description": "Daily French lesson", "periodicity": "daily"}
    ]

    # Insert predefined habits if they don't already exist in the database
    for habit in predefined_habits:
        if not db.habit_exists(habit["name"]):  # Check if the habit already exists
            db.save_habit(Habit(habit["name"], habit["description"], habit["periodicity"]))

    db.insert_test_data()







