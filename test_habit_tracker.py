import pytest
from datetime import datetime, timedelta
from habit import Habit
from analyse import list_all_habits, list_habits_by_periodicity, longest_streak_all_habits, longest_streak_for_habit


# Fixture to set up sample habits that can be reused for testing
@pytest.fixture
def sample_habits():
    habit1 = Habit("Exercise", "Weekly Exercise", "weekly")
    habit2 = Habit("Read", "Read every day", "daily")
    habit3 = Habit("Meditate", "Meditation session", "daily")
    habit4 = Habit("Art Class", "Attend weekly art class", "weekly")
    habit5 = Habit("Learn French", "Daily French lesson", "daily")
    return [habit1, habit2, habit3, habit4, habit5]


# Fixture to set up completion dates for habits, to be reused for testing
@pytest.fixture
def setup_completions(sample_habits):
    base_date = datetime(2023, 9, 25)

    # Setup completions for Exercise (Monday completions)
    for i in range(4):
        sample_habits[0].complete_habit(base_date - timedelta(weeks=i))

    # Setup completions for Read (daily habit)
    for i in range(28):
        sample_habits[1].complete_habit(base_date - timedelta(days=i))

    # Setup completions for Meditate (daily habit)
    for i in range(3):
        sample_habits[2].complete_habit(base_date - timedelta(days=i + 1))
    sample_habits[2].complete_habit(base_date - timedelta(days=5))
    sample_habits[2].complete_habit(base_date - timedelta(days=6))

    # Setup completions for Art Class (Saturday completions)
    for i in range(4):
        saturdays = base_date - timedelta(days=base_date.weekday()) + timedelta(days=5)
        sample_habits[3].complete_habit(saturdays - timedelta(weeks=i))

    # Setup completions for Learn French (daily completions)
    for i in range(4):
        sample_habits[4].complete_habit(base_date - timedelta(days=i))


# Test listing all habits based on their names
def test_list_all_habits(sample_habits):
    assert list_all_habits(sample_habits) == [habit.get_name() for habit in sample_habits]


# Test listing habits by periodicity
def test_list_habits_by_periodicity(sample_habits):
    daily_habits = list_habits_by_periodicity(sample_habits, "daily")
    weekly_habits = list_habits_by_periodicity(sample_habits, "weekly")
    assert len(daily_habits) == 3  # There are three daily habits
    assert len(weekly_habits) == 2  # There are two weekly habits


# Test which habit has the longest streak across all habits
def test_longest_streak_all_habits(sample_habits, setup_completions):
    longest_streak_habit = longest_streak_all_habits(sample_habits)
    assert longest_streak_habit.get_name() == "Read"  # We expect "Read" to have the longest streak (28 days)


# Test the longest streak for a specific habit
def test_longest_streak_for_habit(sample_habits, setup_completions):
    assert longest_streak_for_habit(sample_habits[0]) == 4  # Exercise habit
    assert longest_streak_for_habit(sample_habits[1]) == 28  # Read habit
    assert longest_streak_for_habit(sample_habits[2]) == 3  # Meditate habit
    assert longest_streak_for_habit(sample_habits[3]) == 4  # Art Class habit
    assert longest_streak_for_habit(sample_habits[4]) == 4  # Learn French habit


# Test the streak functionality for daily habits with a reset after a missed day
def test_daily_habit_streak(sample_habits):
    habit = sample_habits[1]  # "Read" habit
    base_date = datetime(2023, 9, 25)
    habit.complete_habit(base_date + timedelta(days=2))
    habit.complete_habit(base_date + timedelta(days=4))
    assert habit.streak() == 1  # Streak should reset after missed days


# Test the streak functionality for weekly habits with a reset after a missed week
def test_weekly_habit_streak(sample_habits):
    habit = sample_habits[0]  # "Exercise" habit
    base_week_start = datetime(2023, 9, 25) - timedelta(days=datetime(2023, 9, 25).weekday())
    habit.complete_habit(base_week_start - timedelta(weeks=1))  # Last week
    habit.complete_habit(base_week_start + timedelta(weeks=1))  # Next week
    assert habit.streak() == 1  # Expect streak to reset after a missed week


# Test habit creation
def test_habit_creation():
    habit = Habit("Test Habit", "Test description", "daily")
    assert habit.get_name() == "Test Habit"
    assert habit.get_description() == "Test description"
    assert habit.get_periodicity() == "daily"

# Test habit editing
def test_habit_editing(sample_habits):
    habit = sample_habits[0]
    habit.edit_habit("New Exercise", "Updated description")
    assert habit.get_name() == "New Exercise"
    assert habit.get_description() == "Updated description"

# Test habit deletion
def test_habit_deletion(sample_habits):
    habit = sample_habits[0]
    sample_habits.remove(habit)
    assert habit not in sample_habits


# Test analytics for daily habits with intermittent completions
def test_daily_habit_with_intermittent_completions(sample_habits):
    habit = sample_habits[1]  # "Read" habit
    base_date = datetime(2023, 9, 25)
    for i in range(3):
        habit.complete_habit(base_date + timedelta(days=i))
    assert habit.streak() == 3  # Streak should be 3
    habit.complete_habit(base_date + timedelta(days=5))
    assert habit.streak() == 1  # Streak should reset to 1 after a missed day


# Test analytics for weekly habits with intermittent completions
def test_weekly_habit_with_intermittent_completions(sample_habits):
    habit = sample_habits[0]  # "Exercise" habit
    base_date = datetime(2023, 9, 25)
    habit.complete_habit(base_date)
    habit.complete_habit(base_date - timedelta(weeks=2))
    assert habit.streak() == 1  # Streak should reset after a missed week












