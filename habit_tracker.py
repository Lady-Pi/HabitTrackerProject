class HabitTracker:
    """Class to manage a collection of habits."""

    def __init__(self):
        """Initialize a new HabitTracker with an empty list of habits."""
        self.habits = []

    def add_habit(self, habit):
        """
        Add a new habit to the tracker.

        Args:
            habit (Habit): The habit to be added.
        """
        self.habits.append(habit)

    def delete_habit(self, habit_name):
        """
        Delete a habit by its name.

        Args:
            habit_name (str): The name of the habit to be deleted.
        """
        # Use a list comprehension to filter out the habit with the specified name
        self.habits = [habit for habit in self.habits if habit.get_name() != habit_name]

    def get_habit(self, name: str):
        """
        Retrieve a habit by its name.

        Args:
            name (str): The name of the habit to retrieve.

        Returns:
            Habit: The habit with the specified name, or None if not found.
        """
        # Convert both the stored habit names and input name to lowercase for comparison
        name_lower = name.lower()
        for habit in self.habits:
            if habit.get_name().lower() == name_lower:  # Case-insensitive comparison
                return habit
        return None







