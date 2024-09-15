from habit import Habit
from datetime import datetime
from db import check_off_habit, add_habit, get_habit_completion_dates, delete_habit

class HabitTracker:
    """
    The HabitTracker class manages multiple habits and provides the functionality to add, delete, and analyse habits
    """
    def __init__(self):
        self.habits = {}

    def add_habit(self, db, name: str, description: str, periodicity: str):
        """
        Adds a new habit to the tracker and stores it in the database.

        Args:
            db (sqlite3.Connection): The database connection object.
            name (str): The name of the habit.
            description (str): A description of the habit.
            periodicity (str): Can be 'daily' or 'weekly'.
        """
        if name in self.habits:
            raise ValueError("Habit with this name already exists.")

        new_habit = Habit(name, description, periodicity)
        self.habits[name] = new_habit
        add_habit(db, name, description, periodicity)
        print(f"Habit '{name}' added and stored in the database.")

    def check_off_habit(self, db, name: str):
        """
        Marks the habit as complete in both the tracker and the database.

        Args:
            db (sqlite3.Connection): The database connection object.
            name (str): The name of the habit to check off.
        """
        if name in self.habits:
            self.habits[name].check_off()
            check_off_habit(db, name)
            print(f"Habit '{name}' checked off and recorded in the database.")
        else:
            print(f"Habit '{name}' not found.")

    def delete_habit(self, db, name: str):
        """
        Removes a habit from the tracker.

        Args:
            db (sqlite3.Connection): The connection object to the database
            name (str): The name of the habit to be removed.
        """
        if name in self.habits:
            del self.habits[name]
            delete_habit(db, name)
            print(f"Habit '{name}' successfully deleted.")
        else:
            print(f"Habit '{name}' not found.")

    def list_habits(self):
        """
        Lists all the current habits in the tracker.
        """
        if not self.habits:
            print("No habits to display.")
        else:
            for habit in self.habits.values():
                print(habit.name)

    def list_habits_by_periodicity(self, periodicity: str):
        """
        Lists all habits based on the specified periodicity (daily or weekly).
        Args:
            periodicity (str): 'daily' or 'weekly'.
        """
        filtered_habits = [habit for habit in self.habits.values() if habit.periodicity == periodicity]

        if filtered_habits:
            for habit in filtered_habits:
                print(habit.name)
        else:
            print(f"No habits with periodicity '{periodicity}'.")

    def calculate_longest_streak(self):
        """
        Returns the habit with the longest streak.
        """
        if not self.habits:
            print("No habits to analyze.")
            return None

        longest_streak_habit = max(self.habits.values(), key=lambda habit: habit.streak)
        print(
            f"The longest streak is held by '{longest_streak_habit.name}' with a streak of {longest_streak_habit.streak} days.")
        return longest_streak_habit

    def calculate_longest_streak_for_habit(self, name: str):
        """
        Returns the longest streak for a specific habit.

        Args:
            name (str): The name of the habit.
        """
        if name in self.habits:
            habit = self.habits[name]
            print(f"The longest streak for '{name}' is {habit.streak} days.")
            return habit.streak
        else:
            print(f"Habit '{name}' not found.")
            return None

    def calculate_completion_count(self, db, name: str):
        """
        Calculate the number of times a habit has been completed.

        Args:
            db (sqlite3.Connection): The database connection object.
            name (str): The name of the habit to analyze.

        Returns:
            int: The total number of completion events for the habit.
        """
        completion_data = get_habit_completion_dates(db, name)
        return len(completion_data)

    def calculate_current_streak(self, db, name: str, periodicity: str):
        """
        Calculate the current streak for a habit based on its completion history and periodicity.

        Args:
            db (sqlite3.Connection): The database connection object.
            name (str): The name of the habit.
            periodicity (str): The periodicity of the habit ('daily' or 'weekly').

        Returns:
            int: The current streak for the habit.
        """
        completion_data = get_habit_completion_dates(db, name)
        if not completion_data:
            return 0

        completion_dates = [datetime.strptime(date[0], "%Y-%m-%d") for date in completion_data]
        completion_dates.sort(reverse=True)

        streak = 1
        last_date = completion_dates[0]

        for date in completion_dates[1:]:
            if periodicity == 'daily' and (last_date - date).days == 1:
                streak += 1
            elif periodicity == 'weekly' and 0 <= (last_date - date).days <= 7:
                streak += 1
            else:
                break
            last_date = date

        return streak



