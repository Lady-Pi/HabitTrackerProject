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

    def complete_habit(self, date=None):
        """Marks a habit as complete by adding the current date to the completions list, ensuring no duplicate entries for the same day."""
        if date is None:
            date = datetime.now()

        # Check if the habit was already completed on this date
        if not any(completion.date() == date.date() for completion in self.get_completions()):
            self._completions.append(date)

    def streak(self) -> int:
        """Calculate the longest streak of consecutive completions."""
        if not self.get_completions():
            return 0

        # Initialize the streak counter
        current_streak = 1
        longest_streak = 1

        # Sort the completion dates in ascending order
        completions = self.get_completions()
        completions.sort()

        # Compare each completion date to the one before it
        for i in range(1, len(completions)):
            current = completions[i]
            previous = completions[i - 1]

            if self.get_periodicity() == "daily":
                # Daily habits: Check if the current completion is exactly 1 day after the previous completion
                if (current.date() - previous.date()).days == 1:
                    current_streak += 1
                else:
                    current_streak = 1  # Reset streak if a day is missed

            elif self.get_periodicity() == "weekly":
                # Weekly habits: Check if the current completion is within 7 days after the previous completion
                if (current.date() - previous.date()).days <= 7:
                    current_streak += 1
                else:
                    current_streak = 1  # Reset streak if more than 7 days passed

            # Track the longest streak encountered
            if current_streak > longest_streak:
                longest_streak = current_streak

        return longest_streak

