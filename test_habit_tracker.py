import pytest
from habit import Habit
from datetime import datetime, timedelta
from analyse import list_all_habits, list_habits_by_periodicity, longest_streak_all_habits, longest_streak_for_habit

# The function sample_habits() is marked as a fixture using the @pytest.fixture decorator, to be used in multiple tests.
@pytest.fixture
def sample_habits():
    habit1 = Habit("Exercise", "Weekly Exercise", "weekly")  # 4-week streak
    habit2 = Habit("Read", "Read every day", "daily")  # 2-day streak
    habit3 = Habit("Meditate", "Meditation session", "daily")  # 3-day streak
    habit4 = Habit("Art Class", "Attend weekly art class", "weekly")  # 1-week streak
    habit5 = Habit("Learn French", "Daily French lesson", "daily")  # 2-day streak

    # Simulate completions for a 4-week streak
    habit1.complete_habit(datetime.now() - timedelta(weeks=4))  # Completed 4 weeks ago
    habit1.complete_habit(datetime.now() - timedelta(weeks=3))  # Completed 3 weeks ago
    habit1.complete_habit(datetime.now() - timedelta(weeks=2))  # Completed 2 weeks ago
    habit1.complete_habit(datetime.now() - timedelta(weeks=1))  # Completed 1 week ago

    habit2.complete_habit(datetime.now() - timedelta(days=2))  # Completed 2 days ago
    habit2.complete_habit(datetime.now() - timedelta(days=1))  # Completed 1 day ago

    habit3.complete_habit(datetime.now() - timedelta(days=3))  # completed 3 days ago
    habit3.complete_habit(datetime.now() - timedelta(days=2))  # completed 2 days ago
    habit3.complete_habit(datetime.now() - timedelta(days=1))  # completed 1 day ago

    habit4.complete_habit(datetime.now() - timedelta(weeks=1))  # Completed 1 week ago

    habit5.complete_habit(datetime.now() - timedelta(days=2))  # Completed 2 days ago
    habit5.complete_habit(datetime.now() - timedelta(days=1))  # Completed 1 day ago

    return [habit1, habit2, habit3, habit4, habit5]

# Test listing all habits
def test_list_all_habits(sample_habits):
    result = list_all_habits(sample_habits)
    assert result == ["Exercise", "Read", "Meditate", "Art Class", "Learn French"]

# Test listing habits by periodicity
def test_list_habits_by_periodicity(sample_habits):
    # Daily habits
    daily_habits = list_habits_by_periodicity(sample_habits, "daily")
    assert len(daily_habits) == 3
    assert daily_habits[0].get_name() == "Read"
    assert daily_habits[1].get_name() == "Meditate"
    assert daily_habits[2].get_name() == "Learn French"

    # Weekly habits
    weekly_habits = list_habits_by_periodicity(sample_habits, "weekly")
    assert len(weekly_habits) == 2
    assert weekly_habits[0].get_name() == "Exercise"
    assert weekly_habits[1].get_name() == "Art Class"

# Test longest streak across all habits
def test_longest_streak_all_habits(sample_habits):
    longest_habit = longest_streak_all_habits(sample_habits)
    assert longest_habit.get_name() == "Exercise"

# Test streak for each habit
def test_longest_streak_for_habit(sample_habits):
    assert longest_streak_for_habit(sample_habits[0]) == 4  # Exercise: 4-week streak
    assert longest_streak_for_habit(sample_habits[1]) == 2  # Read: 2-day streak
    assert longest_streak_for_habit(sample_habits[2]) == 3  # Meditate: 3-day streak
    assert longest_streak_for_habit(sample_habits[3]) == 1  # Art Class: 1-week streak
    assert longest_streak_for_habit(sample_habits[4]) == 2  # Learn French: 2-day streak

# Test for an empty database (no habits)
def test_no_habits():
    no_habits = []
    assert list_all_habits(no_habits) == []
    assert longest_streak_all_habits(no_habits) is None  # No habit should return None for longest streak

# Test for breaking a streak (missing a daily habit for a day)
def test_break_streak_daily(sample_habits):
    habit = sample_habits[1]  # Read habit (daily)
    habit.complete_habit(datetime.now() - timedelta(days=3))  # Complete 3 days ago
    habit.complete_habit(datetime.now() - timedelta(days=2))  # Complete 2 days ago
    # Simulate missing yesterday's completion
    assert habit.streak() == 2  # The streak should be 2

# Test for breaking a streak (missing a weekly habit for a week)
def test_break_streak_weekly(sample_habits):
    habit = sample_habits[0]  # Exercise habit (weekly)
    habit.complete_habit(datetime.now() - timedelta(weeks=5))  # Completed 5 weeks ago
    habit.complete_habit(datetime.now() - timedelta(weeks=4))  # Completed 4 weeks ago
    habit.complete_habit(datetime.now() - timedelta(weeks=2))  # Missed 3 weeks ago (streak should break)
    assert habit.streak() == 1  # The streak should be reset

# Test for handling duplicate habit names
def test_duplicate_habit_names():
    habit1 = Habit("Exercise", "Weekly Exercise", "weekly")
    habit2 = Habit("Exercise", "Another weekly exercise habit", "weekly")  # Same name
    assert habit1.get_name() == habit2.get_name()  # Names are the same
    # Additional logic in your system should handle this case, depending on the desired behavior (e.g., raising an error)

# Test for completing a daily habit multiple times in the same day
def test_multiple_completions_same_day(sample_habits):
    habit = sample_habits[1]  # Read habit (daily)
    habit.complete_habit(datetime.now())  # Complete once today
    habit.complete_habit(datetime.now())  # Complete again today
    assert habit.streak() == 1  # The streak should only count as 1









