class Habit:
    """
    The Habit class represents an individual habit that the user wants to track.
    """

    def __init__(self, name: str, description: str, periodicity: str):
        """
        Initializes a new habit with a name, description, and periodicity

        Arguments:
            name (str): The name of the habit.
            description (str): A description of the habit.
            periodicity (str): Can be 'daily' or 'weekly'.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.streak = 0
        self.completed_dates = []

    def check_off(self):
        """Marks the habit as completed and updates the streak."""
        from datetime import datetime
        self.completed_dates.append(datetime.now())
        self.update_streak()

    def update_streak(self):
        """
        Updates the streak based on the last completion date.
        The streak only increases if the habit is completed on consecutive days or weeks.
        """
        from datetime import timedelta

        if not self.completed_dates:
            self.streak = 0
            return

        # Sort the completion dates in order to compare consecutive streaks
        self.completed_dates.sort()

        last_date = self.completed_dates[-1]
        streak = 1  # Start with a streak of 1 for the last completed date

        # Iterate through the previous dates and check for consecutive days/weeks depending on periodicity
        for i in range(len(self.completed_dates) - 2, -1, -1):
            previous_date = self.completed_dates[i]

            if self.periodicity == 'daily':
                # For daily habits, check if the previous completion is exactly 1 day before
                if last_date - previous_date == timedelta(days=1):
                    streak += 1
                    last_date = previous_date  # Move back to the previous date
                else:
                    break  # If a day is missed, the streak is broken

            elif self.periodicity == 'weekly':
                # For weekly habits, check if the previous completion was within 7 days
                if last_date - previous_date <= timedelta(days=7):
                    streak += 1
                    last_date = previous_date  # Move back to the previous date
                else:
                    break  # If more than 7 days have passed, the streak is broken

        self.streak = streak

    def __str__(self):
        return f"{self.name}: {self.description} (Streak: {self.streak})"





