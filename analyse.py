from functools import reduce #reduce is used to combine elements of a list into a single result by applying a function.

def list_all_habits(habits):
    """Uses map() to create a list of all currently tracked habits."""
    return list(map(lambda habit: habit.get_name(), habits))

def list_habits_by_periodicity(habits, periodicity):
    """Uses filter() to return a list of habits with the same periodicity."""
    return list(filter(lambda habit: habit.get_periodicity() == periodicity, habits))

def longest_streak_all_habits(habits):
    """Uses max() to return the habit with the longest run streak of all habits."""
    return max(habits, key=lambda habit: habit.streak(), default=None)

def longest_streak_for_habit(habit):
    """Return the longest streak for a specific habit."""
    return habit.streak()

# Example of reduce for calculating the longest streak
def longest_streak_using_reduce(habits):
    """Demonstrates how reduce() can be used to find the habit with the longest streak."""
    return reduce(lambda longest, habit: habit if habit.streak() > longest.streak() else longest, habits)

