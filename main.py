import questionary
import sqlite3
from db import get_db
from habit_tracker import HabitTracker


def add_predefined_habits(db, tracker):
    """
    Adds predefined habits to the tracker when the program starts.

    Args:
        db (sqlite3.Connection): The database connection.
        tracker (HabitTracker): The HabitTracker instance.
    """
    predefined_habits = [
        ("Meditation", "Daily meditation for mindfulness", "daily"),
        ("Reading", "Read for 30 minutes", "daily"),
        ("Practice Guitar", "Practice playing the guitar", "weekly"),
        ("Practice Yoga", "Practice yoga ", "weekly"),
        ("Walk", "Go for an outside walk", "daily")
    ]
    for name, description, periodicity in predefined_habits:
        try:
            tracker.add_habit(db, name, description, periodicity)
        except Exception as e:
            print(f"Could not add habit {name}: {e}")

def cli():
    """
    Command-line interface (CLI) for interacting with the habit tracker.

    This function allows the user to:
    - Create a new habit.
    - Complete an existing habit.
    - Analyse how many times a habit has been completed.
    - Exit the application.

    The CLI interacts with the user using the Questionary package,
    and stores and retrieves habit data using the HabitTracker and database.
    """
    # Connect to the production database
    db = get_db("main.db")

    # Initialize the habit tracker
    tracker = HabitTracker()

    stop = False
    while not stop:
        # Ask the user what they want to do
        choice = questionary.select(
            "What do you want to do?",
            choices=["Create", "Complete Habit", "Analyse", "Exit"]
        ).ask()

        # Handle case where user cancels the choice prompt
        if choice is None:
            print("You exited the program. Goodbye!")
            stop = True
            continue

        # Ask for the habit name
        name = questionary.text("What's the name of your habit?").ask()

        if choice == "Create":
            # Ask for a description
            description = questionary.text("What's the description of your habit?").ask()
            # Ask for the periodicity (daily or weekly)
            periodicity = questionary.select(
                "Is this habit daily or weekly?",
                choices=["daily", "weekly"]
            ).ask()

            # Error handling: Ensure the user input is valid
            if not name or not description or not periodicity:
                print("Error: Name, description, and periodicity are required.")
                continue

            try:
                # Create a new habit and store it in the tracker
                tracker.add_habit(db, name, description, periodicity)
                print(f"Habit '{name}' has been created.")
            except sqlite3.IntegrityError:
                # Catch IntegrityError if the habit already exists
                print(f"Error: A habit with the name '{name}' already exists.")
            except Exception as e:
                # General exception handling for any other issues
                print(f"Error while creating habit: {e}")

        elif choice == "Complete Habit":
            try:
                # Check off (complete) the habit
                tracker.check_off_habit(db, name)
                print(f"Habit '{name}' has been completed.")
            except KeyError:
                # Catch a KeyError if the habit name is not found
                print(f"Error: Habit '{name}' does not exist.")
            except Exception as e:
                # General exception handling for any other issues
                print(f"Error while completing habit: {e}")

        elif choice == "Analyse":
            try:
                # Analyse the habit and calculate the completion count
                completion_count = tracker.calculate_completion_count(db, name)
                print(f"Habit '{name}' has been completed {completion_count} times.")
            except KeyError:
                # Catch a KeyError if the habit name is not found
                print(f"Error: Habit '{name}' does not exist.")
            except Exception as e:
                # General exception handling for any other issues
                print(f"Error while analysing habit: {e}")

        elif choice == "Exit":
            # Exit the loop
            print("Goodbye!")
            stop = True


if __name__ == "__main__":
    cli()


