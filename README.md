# Habit Tracker Application

This application provides a Python-based backend functionality of a habit tracker.
Users are able to create and manage their daily and weekly habits through a Command Line Interface (CLI). 

## What is it?

The Habit Tracker allows users to:

- Create and manage daily and weekly habits.
- Mark habits as complete for the current day or calendar week.
- Edit  the name and description of habits.
- Track habit progress with a streak that shows how consistently the habit has been completed.
- View analytic insights, such as the habit with the longest streak.
- If a habit is not completed within the specified period, the streak is reset. 

The application uses an SQLite database to save and load data between sessions.  
Users are able to interact with the CLI via Questionary.
The application comes with five predefined habits for demonstration and testing purposes. 

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

2. Ensure the Virtual Environment is active. 

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
Use the keyboard to enter text when prompted. 

## Testing

To run tests for the Habit Tracker application, we use 'pytest'. Execute the following command:

```shell
pytest
```
The tests include checks for creating, editing and deleting habits, marking them as complete, and viewing streaks.
The test file includes data for five predefined habits with tracking date for four weeks, which allows testing for streak logic and analytic functions.
