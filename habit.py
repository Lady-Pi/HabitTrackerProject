from datetime import datetime

class Habit:
    def __init__(self, name: str, description: str, periodicity: str):
        """Create a new Habit with the given name, description, and periodicity."""
        self._name = name
        self._description = description
        self._periodicity = periodicity  # 'daily' or 'weekly'
        self._creation_date = datetime.now()
        self._completions = []  # A list of dates when the habit was marked complete.

    # Getter methods to access non-public attributes
    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_periodicity(self):
        return self._periodicity

    def get_creation_date(self):
        return self._creation_date

    def get_completions(self):
        """Return the list of completion dates."""
        return self._completions

    def complete_habit(self):
        """Marks a habit as complete by adding the current date to the completions list."""
        self._completions.append(datetime.now())

    def streak(self) -> int:
        """Calculate the streak of consecutive completions."""
        if not self.get_completions():
            return 0

        # Initialize the streak counter
        streak = 1

        # Sort the completion dates in ascending order
        completions = self.get_completions()
        completions.sort()

        # Compare each completion date to the one before it
        for i in range(1, len(completions)):
            current = completions[i]
            previous = completions[i - 1]
            # For daily habits, check if the current completion is exactly 1 day after the previous completion
            # If it is consecutive, increase the streak. If it is broken, reset the streak to 1
            if self.get_periodicity() == "daily":
                if (current - previous).days == 1:
                    streak += 1
                else:
                    streak = 1
            # For weekly habits, check if the completion is within 7 days after the previous completion.
            # If within a week, increase the streak. If more than 7 days passed, reset the streak to 1.
            elif self.get_periodicity() == "weekly":
                if (current - previous).days <= 7:
                    streak += 1
                else:
                    streak = 1

        return streak





