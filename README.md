# My Habit Tracker App

This project provides the basic functionality of a habit tracker. 

## What is it?

Users are able to create weekly and daily habits, that can be checked-off at any time.
If the habit is not completed during the specified period, one day for daily habits or seven days 
for weekly habits, the streak is broken. 
The application includes an analytics module, allowing users to analyse their habits. 
Data is saved and loaded with sqlite3. Users interact with the Command Line Interface via Questionary.


## Installation

```shell
pip install -r requirements.txt
```

## Usage

Start

```shell
python main.py
```

and follow instructions on screen

## Tests

```shell
pytest . 
```