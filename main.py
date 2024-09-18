import questionary  # used to ask the user for input
from habit_tracker import HabitTracker
from habit import Habit
from db import Database, initialize_predefined_habits
from datetime import datetime
from analyse import list_all_habits, list_habits_by_periodicity, longest_streak_all_habits

# Create HabitTracker and Database instances
tracker = HabitTracker()
db = Database()

# Initialize predefined habits if the database is empty
initialize_predefined_habits(db)

# On startup, load existing habits from the database and add them to the HabitTracker
for habit_data in db.load_habits():
    loaded_habit = Habit(habit_data['name'], habit_data['description'], habit_data['periodicity'])
    loaded_habit._creation_date = datetime.strptime(habit_data['creation_date'], "%Y-%m-%d %H:%M:%S.%f")
    loaded_habit._completions = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in habit_data['completions']]
    tracker.add_habit(loaded_habit)


# Via Questionary, the user can choose to add, delete, mark habits as complete, view streaks, or exit
def main():
    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Add Habit",
                "Delete Habit",
                "Mark Habit as Complete",
                "View Habit Streaks",
                "View All Habits",
                "View Habits by Periodicity",
                "View Longest Streak Habit",
                "Exit"
            ]
        ).ask()

        if action == "Add Habit":
            name = questionary.text("Enter habit name:").ask()
            description = questionary.text("Enter habit description:").ask()
            periodicity = questionary.select("Choose periodicity:", choices=["daily", "weekly"]).ask()

            new_habit = Habit(name, description, periodicity)
            tracker.add_habit(new_habit)
            habit_id = db.save_habit(new_habit)
            print(f"Habit '{name}' added with ID {habit_id}.")

        elif action == "Delete Habit":
            name = questionary.text("Enter habit name to delete:").ask()
            habit_to_delete = tracker.get_habit(name)
            if habit_to_delete:
                habit_id = db.get_habit_id(habit_to_delete.get_name())
                db.delete_habit(habit_id)
                print(f"Habit '{name}' deleted.")
            else:
                print("Habit not found.")

        elif action == "Mark Habit as Complete":
            name = questionary.text("Enter habit name to mark as complete:").ask()
            habit_to_complete = tracker.get_habit(name)
            if habit_to_complete:
                habit_to_complete.complete_habit()
                habit_id = db.get_habit_id(name)
                db.save_completion(habit_id, datetime.now())
                print(f"Marked '{name}' as complete.")
            else:
                print("Habit not found.")

        elif action == "View Habit Streaks":
            for current_habit in tracker.habits:
                print(f"Habit '{current_habit.get_name()}' has a streak of {current_habit.streak()} days/weeks.")

        # New options using the analyse.py functions:
        elif action == "View All Habits":
            all_habits = list_all_habits(tracker.habits)
            print("All Habits:", ", ".join(all_habits))

        elif action == "View Habits by Periodicity":
            periodicity = questionary.select("Choose periodicity to view:", choices=["daily", "weekly"]).ask()
            habits_by_period = list_habits_by_periodicity(tracker.habits, periodicity)
            habit_names = [habit.get_name() for habit in habits_by_period]
            print(f"{periodicity.capitalize()} Habits:", ", ".join(habit_names))

        elif action == "View Longest Streak Habit":
            longest_streak_habit = longest_streak_all_habits(tracker.habits)
            if longest_streak_habit:
                print(f"The habit with the longest streak is '{longest_streak_habit.get_name()}' with a streak of {longest_streak_habit.streak()} days/weeks.")
            else:
                print("No habits found.")

        elif action == "Exit":
            break

if __name__ == "__main__":
    main()





