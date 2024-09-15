import os
from db import get_db, add_habit, check_off_habit, get_habit_completion_dates
from analyse import calculate_completion_count, calculate_current_streak, calculate_longest_streak
from db import create_tables

class TestHabitTracker:

    def setup_method(self):
        """
        Setup method to initialize a new test database.
        This method is called before each test.
        """
        self.db = get_db("test_habit.db")  # Create a test database

        # Drop existing tables (if they exist)
        cur = self.db.cursor()
        cur.execute("DROP TABLE IF EXISTS habits")
        cur.execute("DROP TABLE IF EXISTS tracker")
        self.db.commit()

        # Recreate the tables
        create_tables(self.db)

        add_habit(self.db, "Test Habit", "Test description", "daily")  # Add a sample habit
        check_off_habit(self.db, "Test Habit", "2024-09-01")
        check_off_habit(self.db, "Test Habit", "2024-09-02")
        check_off_habit(self.db, "Test Habit", "2024-09-03")
        check_off_habit(self.db, "Test Habit", "2024-09-04")

    def teardown_method(self):
        """
        Teardown method to remove the test database.
        This method is called after each test.
        """
        self.db.close()  # Close the database connection before removing the file
        os.remove("test_habit.db")  # Delete the test database after each test

    def test_add_habit(self):
        """
        Test adding a habit to the database.
        """
        add_habit(self.db, "Test Habit 2", "Test description 2", "weekly")
        habits = get_habit_completion_dates(self.db, "Test Habit 2")
        assert habits == [], "New habit should have no completion dates."

    def test_check_off_habit(self):
        """
        Test marking a habit as completed.
        """
        completions = get_habit_completion_dates(self.db, "Test Habit")
        assert len(completions) == 4, "Habit should have 4 completion dates."

    def test_calculate_completion_count(self):
        """
        Test calculating the number of completions for a habit.
        """
        count = calculate_completion_count(self.db, "Test Habit")
        assert count == 4, "Habit should have 4 completions."

    def test_current_streak(self):
        """
        Test calculating the current streak for a habit.
        """
        streak = calculate_current_streak(self.db, "Test Habit", "daily")
        assert streak == 4, "Current streak should be 4 days."

    def test_longest_streak(self):
        """
        Test calculating the longest streak for a habit.
        """
        longest_streak = calculate_longest_streak(self.db, "Test Habit", "daily")
        assert longest_streak == 4, "Longest streak should be 4 days."





