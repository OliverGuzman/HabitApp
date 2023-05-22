# HabitApp

This is an app using django framework for creating, tracking and managing habits.

## What is it?

This project focuses in the development of an app for habits. It allows to create, check off and complete habits with different periodicities. Additionally, it has a module that allows to analyze data from the current habits to provide an in deep view. 

## Structure

The django project has four main parts which are "habitProject", "habitApp", "streakApp" and "userApp":

## Activation of VENV

Please create a virtual enviroment using python 3.10 as it was the version used to developed the app. Once the virtual enviroment is created, please go to root where it is such as ...OOFP\ the name of the venv \ to activate the virtual enviroment:

```shell
Scripts\activate
```

## Installation

With the VENV activatate, please go to the root "...OOFP\backend\" and install the requirments:

```shell
pip install -r requirements.txt
```

## Activation of Django project

Please go to the root "...OOFP\backend\" to activate the django project

```shell
python manage.py runserver 
```

## Testing

Before using the CLI, please launch the testing enviroment as it uses the data from the predefined habits to test the function in deep. The command "pytest" should be used from the root "...OOFP\backend\"

```shell
pytest -v
```

## Usage

For activation of the CLI, please go to the root "...OOFP\backend\"

```shell
python main.py
```