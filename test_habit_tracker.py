import pytest
from habit import Habit
from habit_tracker import HabitTracker
from datetime import datetime, timedelta


def test_add_habit():
    tracker = HabitTracker()
    habit = Habit("Exercise", "Work out daily", "daily")
    tracker.add_habit(habit)

    assert len(tracker.habits) == 1
    assert tracker.get_habit("Exercise") == habit


def test_streak_calculation():
    habit = Habit("Exercise", "Work out daily", "daily")
    habit._completions = [
        datetime.now() - timedelta(days=2),  # Completed 2 days ago
        datetime.now() - timedelta(days=1),  # Completed 1 day ago
    ]
    assert habit.streak() == 2







