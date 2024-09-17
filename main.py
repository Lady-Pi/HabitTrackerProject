import questionary # used to ask the user for input
from habit_tracker import HabitTracker
from habit import Habit
from db import Database
from datetime import datetime

# Create HabitTracker and Database instances
tracker = HabitTracker()
db = Database()

# On startup, load existing habits from the database and add them to the HabitTracker
for habit_data in db.load_habits():
    habit = Habit(habit_data['name'], habit_data['description'], habit_data['periodicity'])
    habit._creation_date = datetime.strptime(habit_data['creation_date'], "%Y-%m-%d %H:%M:%S")
    habit._completions = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date in habit_data['completions']]
    tracker.add_habit(habit)

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
            for habit_instance in tracker.habits:
                print(f"Habit '{habit_instance.get_name()}' has a streak of {habit_instance.streak()} days/weeks.")

        elif action == "Exit":
            break

if __name__ == "__main__":
    main()





