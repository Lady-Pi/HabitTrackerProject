# Habit Tracker Application

This project provides the core back-end functionality of a habit tracker.
Users are able to create and manage their daily and weekly habits through a Command Line Interface (CLI). 

## What is it?

The Habit Tracker allows users to:

- Create and manage daily and weekly habits.
- Mark habits as complete for the current day or week.
- Track habit progress with a streak that shows how consistently the habit has been completed.
- View analytical insights, such as the habit with the longest streak.
- If a habit is not completed within the specified period, the streak is reset. 

The application uses an SQLite database to persist data, ensuring that habit data is stored and retrieved.

Users are able to interact with the CLI via Questionary.

## Installation

To install and run the Habit Tracker, follow these steps:

1. Clone or download the project to your computer.
2. Navigate to the project directory.

```shell
cd path/to/HabitTrackerProject
```
3. Install the required dependencies (like third party libraries) from the requirements.txt file:

```shell
pip install -r requirements.txt
```

## Usage

This application provides back-end functionality only, and all interactions takes place via the Command Line Interface (CLI). 
To run the application, you must use a terminal or cmd.exe (on Windows) to ensure compatibility with Questionary.

1. Open the Command Prompt: 
   - For Windows, press Win + R, type cmd, and hit Enter.


2. Navigate to the project directory: 
```shell
cd path/to/HabitTrackerProject
```

3. Run the Application:

```shell
python main.py
```

4. Follow the instructions on the screen. You will be presented with a menu.
Use the arrow keys to navigate through the options and press Enter to select.

## Testing

To run tests for the Habit Tracker application, run pytest.py in the IDE use the following command:

```shell
pytest . 
```
The tests include checks for creating and deleting habits, marking them as complete, and viewing streaks.
