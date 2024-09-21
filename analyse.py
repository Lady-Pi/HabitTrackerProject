def list_all_habits(habits):
    """
    Creates a list of names of all currently tracked habits.

    Args:
        habits (list): A list of Habit objects.

    Returns:
        list: A list of names of all habits.
    """
    return list(map(lambda habit: habit.get_name(), habits))


def list_habits_by_periodicity(habits, periodicity):
    """
    Returns a list of habits that have the specified periodicity.

    Args:
        habits (list): A list of Habit objects.
        periodicity (str): The periodicity to filter habits by ('daily' or 'weekly').

    Returns:
        list: A list of Habit objects with the given periodicity.
    """
    return list(filter(lambda habit: habit.get_periodicity() == periodicity, habits))


def longest_streak_all_habits(habits):
    """
    Returns the habit with the longest run streak among all habits.

    Args:
        habits (list): A list of Habit objects.

    Returns:
        Habit: The habit with the longest streak, or None if there are no habits.
    """
    result = max(habits, key=lambda habit: habit.streak(), default=None)
    return result


def longest_streak_for_habit(habit):
    """
    Returns the longest streak for a specific habit.

    Args:
        habit (Habit): The habit to get the longest streak for.

    Returns:
        int: The longest streak of the habit.
    """
    return habit.streak()




