import questionary
from habit_tracker import HabitTracker
from habit import Habit
from db import Database, initialize_predefined_habits
from datetime import datetime
from analyse import list_habits_by_periodicity, longest_streak_all_habits

# Create HabitTracker and Database instances
tracker = HabitTracker()
db = Database()

# Initialize predefined habits
initialize_predefined_habits(db)

# Load existing habits from the database on startup
for habit_data in db.load_habits():
    loaded_habit = Habit(habit_data['name'], habit_data['description'], habit_data['periodicity'])
    loaded_habit._creation_date = datetime.strptime(habit_data['creation_date'], "%Y-%m-%d %H:%M:%S.%f")
    loaded_habit._completions = habit_data['completions']
    tracker.add_habit(loaded_habit)


def main():
    """Main function to handle the habit tracker operations, interaction with main menu."""
    while True:
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Add Habit",
                "Edit Habit",
                "Delete Habit",
                "View Specific Habit",
                "Mark Habit as Complete",
                "View All Habits",
                "View Habits by Periodicity",
                "View Habit with Longest Streak",
                "Exit"
            ]
        ).ask()

        if action == "Add Habit":
            name = questionary.text("Enter habit name:").ask().lower()
            # Check if habit already exists
            if db.habit_exists(name):
                print(f"Habit '{name}' already exists. Please choose a different name.")
            else:
                description = questionary.text("Enter habit description:").ask()
                periodicity = questionary.select("Choose periodicity:", choices=["daily", "weekly"]).ask()
                new_habit = Habit(name, description, periodicity)
                tracker.add_habit(new_habit)
                db.save_habit(new_habit)
                print(f"Habit '{name}' added successfully.")

        elif action == "Edit Habit":
            name = questionary.text("Enter habit name to edit:").ask().lower()
            habit_to_edit = tracker.get_habit(name.lower())
            if habit_to_edit:
                edit_choice = questionary.select(
                    "What would you like to update?",
                    choices=["Name", "Description"]
                ).ask()
                if edit_choice == "Name":
                    new_name = questionary.text("Enter new habit name:").ask().lower()
                    if db.habit_exists(new_name):
                        print(f"Habit with the name '{new_name}' already exists. Please choose a different name.")
                    else:
                        habit_id = db.get_habit_id(name)
                        db.update_habit(habit_id, new_name, habit_to_edit.get_description())
                        habit_to_edit.edit_habit(new_name, habit_to_edit.get_description())
                        print(f"Habit name updated to '{new_name.title()}'.")
                elif edit_choice == "Description":
                    new_description = questionary.text("Enter new habit description:").ask()
                    habit_id = db.get_habit_id(name)
                    db.update_habit(habit_id, habit_to_edit.get_name(), new_description)
                    habit_to_edit.edit_habit(habit_to_edit.get_name(), new_description)
                    print(f"Habit description updated to '{new_description}'.")
            else:
                print("Habit not found.")

        elif action == "View Specific Habit":
            name = questionary.text("Enter habit name to view:").ask()
            habit_to_view = tracker.get_habit(name.lower())  # convert to lowercase
            if habit_to_view:
                print(f"\nHabit: {habit_to_view.get_name().title()}")
                print(f"Description: {habit_to_view.get_description()}")
                print(f"Periodicity: {habit_to_view.get_periodicity()}")
                print(f"Creation Date: {habit_to_view.get_creation_date().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Streak: {habit_to_view.streak() or 0}")
                completions_list = habit_to_view.get_completions()
                if completions_list:
                    print(f"Completions: {', '.join(str(completion) for completion in completions_list)}")
                else:
                    print("Completions: 0")
            else:
                print("Habit not found.")

        elif action == "Delete Habit":
            name = questionary.text("Enter habit name to delete:").ask()
            habit_to_delete = tracker.get_habit(name.lower())
            if habit_to_delete:
                habit_id = db.get_habit_id(habit_to_delete.get_name().lower())
                db.delete_habit(habit_id)
                tracker.delete_habit(name)
                print(f"Habit '{name.title()}' deleted.")
            else:
                print("Habit not found.")

        elif action == "Mark Habit as Complete":
            name = questionary.text("Enter habit name to mark as complete:").ask()
            habit_to_complete = tracker.get_habit(name.lower())
            if habit_to_complete:
                now = datetime.now()
                # Check for duplicate completion
                habit_periodicity = habit_to_complete.get_periodicity()
                if habit_periodicity == "daily":
                    for completion in habit_to_complete.get_completions():
                        if completion.date() == now.date():
                            print(
                                f"Cannot mark '{name.title()}' as complete. It has already been marked complete today.")
                            break
                    else:
                        habit_to_complete.complete_habit()
                        habit_id = db.get_habit_id(name)
                        db.save_completion(habit_id, now)
                        print(f"Marked '{name.title()}' as complete.")
                        print(
                            f"Completions for '{name.title()}': {', '.join(str(completion) for completion in habit_to_complete.get_completions())}")

                elif habit_periodicity == "weekly":
                    current_week = now.isocalendar()[1]
                    current_year = now.isocalendar()[0]
                    for completion in habit_to_complete.get_completions():
                        comp_week = completion.isocalendar()[1]
                        comp_year = completion.isocalendar()[0]
                        if comp_week == current_week and comp_year == current_year:
                            print(
                                f"Cannot mark '{name.title()}' as complete. It has already been marked complete this week.")
                            break
                    else:
                        habit_to_complete.complete_habit()
                        habit_id = db.get_habit_id(name)
                        db.save_completion(habit_id, now)
                        print(f"Marked '{name.title()}' as complete.")
                        print(
                            f"Completions for '{name.title()}': {', '.join(str(completion) for completion in habit_to_complete.get_completions())}")

            else:
                print("Habit not found.")

        elif action == "View All Habits":
            all_habits = tracker.habits
            if not all_habits:
                print("No habits found.")
            else:
                print("\nAll Habits:")
                for habit in all_habits:
                    # Get the latest completion date
                    completions = habit.get_completions()
                    if completions:
                        latest_completion = max(completions)
                        latest_completion_str = latest_completion.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        latest_completion_str = "No completions yet"

                    print(f"- Habit: {habit.get_name()}")
                    print(f"  Description: {habit.get_description()}")
                    print(f"  Periodicity: {habit.get_periodicity().capitalize()}")
                    print(f"  Creation Date: {habit.get_creation_date().strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"  Streak: {habit.streak() or 0} consecutive completions")
                    print(f"  Latest Completion: {latest_completion_str}\n")

        elif action == "View Habits by Periodicity":
            periodicity = questionary.select("Choose periodicity to view:", choices=["daily", "weekly"]).ask()
            habits_by_period = list_habits_by_periodicity(tracker.habits, periodicity)
            habit_names = [habit.get_name() for habit in habits_by_period]
            print(f"\n{periodicity.capitalize()} Habits:", ", ".join(habit_names))

        elif action == "View Habit with Longest Streak":
            longest_streak_habit = longest_streak_all_habits(tracker.habits)
            if longest_streak_habit:
                print(
                    f"\nThe habit with the longest streak is '{longest_streak_habit.get_name().title()}' with a streak of {longest_streak_habit.streak() or 0}")
            else:
                print("No habits found.")

        elif action == "Exit":
            break


if __name__ == "__main__":
    main()










