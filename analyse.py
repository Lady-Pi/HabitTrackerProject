def calculate_completion_count(db, habit_name):
    """
    Calculate the number of times a habit has been marked as complete and returns the count
    This function retrieves all the completion dates for a given habit from the tracker table in the database.
    If no completion data is found, it returns 0 and prints a message.

    Args:
        db (sqlite3.Connection): The database connection object.
        habit_name (str): The name of the habit to analyze.

    Returns:
        int: The total number of completion events for the habit.
    """
    completion_data = get_habit_completion_dates(db, habit_name)
    if not completion_data:
        print(f"No completion data found for habit '{habit_name}'.")
        return 0
    return len(completion_data)


from db import get_habit_completion_dates
from datetime import datetime

def calculate_current_streak(db, habit_name, periodicity):
    """
    Calculate the current streak for a habit, based on the periodicity and completion history.
    The function checks if the habit was completed daily (exactly 1 day apart) or weekly (within 7 days).

    Args:
        db (sqlite3.Connection): The database connection object.
        habit_name (str): The name of the habit to analyze.
        periodicity (str): The periodicity of the habit ('daily' or 'weekly').

    Returns:
        int: The current streak of the habit (number of consecutive completions).
    """
    completion_data = get_habit_completion_dates(db, habit_name)
    if not completion_data:
        print(f"No completion data found for habit '{habit_name}'.")
        return 0

    completion_dates = [datetime.strptime(date[0], "%Y-%m-%d") for date in completion_data]
    completion_dates.sort(reverse=True)  # Sort dates from most recent to oldest

    streak = 1
    last_date = completion_dates[0]

    for current_date in completion_dates[1:]:
        if periodicity == 'daily':
            if (last_date - current_date).days == 1:
                streak += 1
                last_date = current_date
            else:
                break  # Streak is broken
        elif periodicity == 'weekly':
            if (last_date - current_date).days <= 7:
                streak += 1
                last_date = current_date
            else:
                break  # Streak is broken

    return streak


def calculate_longest_streak(db, habit_name, periodicity):
    """
    Calculate the longest streak for a habit so far, based on the periodicity and completion history.

    Args:
        db (sqlite3.Connection): The database connection object.
        habit_name (str): The name of the habit to analyze.
        periodicity (str): The periodicity of the habit ('daily' or 'weekly').

    Returns:
        int: The longest streak (consecutive completions) of the habit.
    """
    completion_data = get_habit_completion_dates(db, habit_name)
    if not completion_data:
        print(f"No completion data found for habit '{habit_name}'.")
        return 0

    completion_dates = [datetime.strptime(date[0], "%Y-%m-%d") for date in completion_data]
    completion_dates.sort()

    longest_streak = 0
    current_streak = 1
    last_date = completion_dates[0]

    for current_date in completion_dates[1:]:
        if periodicity == 'daily':
            if (current_date - last_date).days == 1:
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1  # Reset streak
        elif periodicity == 'weekly':
            if (current_date - last_date).days <= 7:
                current_streak += 1
            else:
                longest_streak = max(longest_streak, current_streak)
                current_streak = 1  # Reset streak

        last_date = current_date

    # Ensure the longest streak is updated at the end of the loop
    longest_streak = max(longest_streak, current_streak)

    return longest_streak
