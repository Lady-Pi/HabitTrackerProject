from datetime import datetime, timedelta

class Habit:
    def __init__(self, name: str, description: str, periodicity: str):
        self._name = name
        self._description = description
        self._periodicity = periodicity  # 'daily' or 'weekly'
        self._creation_date = datetime.now()
        self._completions = []

    def complete_habit(self, completion_date: datetime = None):
        if not completion_date:
            completion_date = datetime.now()

        # Avoid duplicate completions for the same day/week
        if self._completions:
            last_completion = self._completions[-1]
            if self._periodicity == 'daily':
                if last_completion.date() == completion_date.date():
                    print("Habit already completed today.")
                    return
            elif self._periodicity == 'weekly':
                last_week = last_completion.isocalendar()[1]
                current_week = completion_date.isocalendar()[1]
                if last_week == current_week:
                    print("Habit already completed this week.")
                    return

        # Add the completion date
        self._completions.append(completion_date)

    def streak(self):
        if not self._completions:
            return 0

        current_streak = 1
        completions = sorted(self._completions)  # Sort completions in case they are out of order

        # Iterate over completions and calculate streak
        for i in range(1, len(completions)):
            current = completions[i]
            previous = completions[i - 1]

            if self._periodicity == 'daily':
                # If the days are consecutive, increase the streak
                if (current.date() - previous.date()).days == 1:
                    current_streak += 1
                else:
                    # If a day is missed, break the streak
                    return current_streak

            elif self._periodicity == 'weekly':
                current_week = current.isocalendar()[1]
                previous_week = previous.isocalendar()[1]
                current_year = current.isocalendar()[0]
                previous_year = previous.isocalendar()[0]

                # Check if weeks are consecutive
                if (current_year == previous_year and current_week == previous_week + 1) or \
                   (current_year == previous_year + 1 and current_week == 1 and previous_week == 52):
                    current_streak += 1
                else:
                    print("Resetting streak due to missed week.")
                    return 1  # Reset to 1 when a week is missed

        print(f"Final streak: {current_streak}")
        return current_streak

    def get_name(self):
        return self._name

    def get_periodicity(self):
        return self._periodicity













