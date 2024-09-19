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

The application uses an SQLite database to save and load data. 

Users are able to interact with the CLI via Questionary.

## Installation

To install and run the Habit Tracker, follow these steps:

1. Clone or download the project to your computer using Git:
  ```bash
   git clone https://github.com/Lady-Pi/HabitTrackerProject.git
   ```
2. Navigate to the project directory:

```shell
cd path/to/HabitTrackerProject
```
3. Create a virtual environment and activate it to isolate project dependencies:

On Windows:
```shell
python -m venv .venv
.venv\Scripts\activate
```
On macOS/Linux:

```shell
python3 -m venv .venv
source .venv/bin/activate

```

4. Install the required dependencies (like third party libraries) from the requirements.txt file:

```shell
pip install -r requirements.txt
```

## Usage

The application relies on Questionary for CLI interaction. This works best when run from a terminal like cmd.exe (Windows),
or other terminals with full console support.

1. Open the Command Prompt: 
   - For Windows, press Win + R, type cmd, and hit Enter.

2. Before running the app, ensure the Virtual Environment is active. 

On Windows:

```shell
.venv\Scripts\activate

```
On macOS/Linux:

```shell
source .venv/bin/activate

```

3. Navigate to the root directory of the project and run the application: 
```shell
python main.py

```

4. Follow the instructions on the screen to interact with the habit tracker.
Use the arrow keys to navigate through the options and press Enter to confirm.

## Testing

To run tests for the Habit Tracker application

```shell
pytest . 
```
The tests include checks for creating and deleting habits, marking them as complete, and viewing streaks.
