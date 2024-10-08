from datetime import datetime # used for managing dates and times, setting creation and completion dates and comparing them

class Habit:
    """
    Represents an individual habit with attributes

    Attributes:
        _name (str): The name of the habit.
        _description (str): The description of the habit.
        _periodicity (str): The frequency of the habit ('daily' or 'weekly').
        _creation_date (datetime): The date and time the habit was created.
        _completions (list): List of datetime objects representing when the habit was completed.
    """

    def __init__(self, name: str, description: str, periodicity: str):
        """
        Initializes a new habit.

        Args:
            name (str): The name of the habit.
            description (str): The description of the habit.
            periodicity (str): The frequency of the habit ('daily' or 'weekly').
        """
        self._name = name
        self._description = description
        self._periodicity = periodicity  # 'daily' or 'weekly'
        self._creation_date = datetime.now()
        self._completions = []

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

    def complete_habit(self, completion_date: datetime = None):
        if not completion_date:
            completion_date = datetime.now()

        # Avoid duplicate completions for the same day or calendar week
        if self._completions:
            last_completion = self._completions[-1]
            if self._periodicity == 'daily' and last_completion.date() == completion_date.date():
                print("Habit already completed today.")
                return
            elif self._periodicity == 'weekly' and last_completion.isocalendar()[1] == completion_date.isocalendar()[1]:
                print("Habit already completed this week.")
                return

        # Add the completion date
        self._completions.append(completion_date)

    def edit_habit(self, new_name, new_description):
        """
        Edits the habit's name and description.

        Args:
            new_name (str): The new name of the habit.
            new_description (str): The new description of the habit.
        """
        self._name = new_name
        self._description = new_description

    def streak(self):
        """
        Calculates the current streak of completing the habit.

        Returns:
            int: The current streak of consecutive completions.
        """
        if not self._completions:
            return 0

        sorted_completions = sorted(set(self._completions))  # Ensure unique and sorted entries
        current_streak = 1  # Start with the latest completion

        # Start from the end of the list and move backwards
        for i in range(len(sorted_completions) - 1, 0, -1):
            current = sorted_completions[i]
            previous = sorted_completions[i - 1]

            # Handling daily streaks
            if self._periodicity == 'daily':
                if (current - previous).days == 1:
                    current_streak += 1
                else:
                    break  # Stop counting if a day is missed

            # Handling weekly streaks
            elif self._periodicity == 'weekly':
                current_week = current.isocalendar()[1]
                previous_week = previous.isocalendar()[1]
                current_year = current.isocalendar()[0]
                previous_year = previous.isocalendar()[0]

                # Checking if the calendar weeks are consecutive
                if (current_year == previous_year and current_week == previous_week + 1) or (
                        current_year == previous_year + 1 and current_week == 1 and previous_week in {52, 53}):
                    current_streak += 1
                else:
                    break  # Stop counting if a week is missed

        return current_streak


















