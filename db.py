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

    def habit_exists(self, name):
        """Check if a habit with the given name already exists in the database."""
        cursor = self.conn.execute('SELECT id FROM habits WHERE LOWER(name) = ?', (name.lower(),))
        result = cursor.fetchone()
        return result is not None  # Returns True if the habit exists, False otherwise

    def save_habit(self, habit):
        """Save the new habit into the database and return its automatically generated ID."""
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

    def update_habit(self, habit_id, new_name, new_description):
        """Update the name and description of a habit in the database."""
        self.conn.execute('''UPDATE habits
                             SET name = ?, description = ?
                             WHERE id = ?''', (new_name, new_description, habit_id))
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
        """Retrieve the habit's ID from the database based on the habit name."""
        cursor = self.conn.execute('SELECT id FROM habits WHERE LOWER(name) = LOWER(?)', (name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def insert_test_data(self):
        """Insert sample data for habits"""
        base_date = datetime(2023, 9, 25)
        sample_data = {
            "Exercise": [
                base_date - timedelta(weeks=3),
                base_date - timedelta(weeks=2),
                base_date - timedelta(weeks=1),
                base_date
            ],
            "Read": [
                base_date - timedelta(days=i) for i in range(28)
            ],
            "Meditate": [
                            base_date - timedelta(days=i + 1) for i in range(3)
                        ] + [
                            base_date - timedelta(days=5),
                            base_date - timedelta(days=6)
                        ],
            "Art Class": [
                base_date - timedelta(weeks=3) + timedelta(days=5),
                base_date - timedelta(weeks=2) + timedelta(days=5),
                base_date - timedelta(weeks=1) + timedelta(days=5),
                base_date + timedelta(days=5)
            ],
            "Learn French": [
                base_date - timedelta(days=0),
                base_date - timedelta(days=1),
                base_date - timedelta(days=2),
                base_date - timedelta(days=3)
            ]
        }

        for habit_name, dates in sample_data.items():
            habit_id = self.get_habit_id(habit_name)
            if habit_id is not None:
                for date in dates:
                    completion_date = date
                    self.save_completion(habit_id, completion_date)


def initialize_predefined_habits(db):
    """Initialize predefined habits in the database and load sample tracking data."""

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









