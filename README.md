# HabitApp

This is an app using django framework for creating, tracking and managing habits.

## What is it?

This project focuses in the development of an app for habits. It allows to create, check off and complete habits with different periodicities. Additionally, it has a module that allows to analyze data from the current habits to provide an in deep view. 

## Structure

The django project has four main parts which are "habitProject", "habitApp", "streakApp" and "userApp":

## Activation of VENV

Please create a virtual enviroment using python 3.10 as it was the version used to developed the app and it is recommended using the name of "venv". Once the virtual enviroment is created, please go to root where it is such as ...OOFP\ the name of the venv \ to activate the virtual enviroment:

```shell
Scripts\activate
```

## Installation

With the VENV active, please go to the root "...OOFP\backend\" and install the requirments:

```shell
pip install -r requirements.txt
```

## Activation of Django project

With the VENV active, please go to the root "...OOFP\backend\" to activate the django project

```shell
python manage.py runserver 
```

## Testing

Before using the CLI, please launch the testing enviroment as it uses the data from the predefined habits to test the function in deep. The command "pytest" should be used from the root "...OOFP\backend\"

```shell
pytest -v
```

## Usage

In a separete command tab from which has the django applicatin active, please active the venv and then activation the CLI by going to the root "...OOFP\backend\"

```shell
python main.py
```
For using the CLI, it will give a menu that you can pick several options.

"Create a habit": ask you for a description and a periodicity to create the habit
"See the details of a habit": it will return the details of a habit
"List all habits": returns a list of all habits
"Check off a habit": ask you the idhabit so it can mark a check-off if it is on time
"Complete a habit": ask you the idhabit so it can mark as complete(marks the complete status of the streak as true)
"Reactivate a habit": ask you the idhabit so it can create a new streak for a given habit 
"See all habit with a specific periodicty": returns a list
"See the streak with the longest run": return the details of the streak
"See the streak with the longest run for a specific habit": return the details of the streak
