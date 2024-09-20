class HabitTracker:
    def __init__(self):
        """Initialize a new HabitTracker with an empty list of habits."""
        self.habits = []

    def add_habit(self, habit):
        """Add a new habit to the tracker."""
        self.habits.append(habit)

    def delete_habit(self, habit_name):
        """Delete a habit by its name."""
        self.habits = [habit for habit in self.habits if habit.get_name != habit_name]

    def get_habit(self, name: str):
        # Convert both the stored habit names and input name to lowercase for comparison
        name_lower = name.lower()
        for habit in self.habits:
            if habit.get_name().lower() == name_lower:  # Case-insensitive comparison
                return habit
        return None

    def analyze_habits(self):
        """Placeholder for habit analysis functionality."""
        # This method will later use functions from the 'analyse.py' module.
        pass




