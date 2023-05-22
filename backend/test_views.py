import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habitProject.settings")

import django
django.setup()

import requests
from django.shortcuts import get_object_or_404
from habitApp.models import Habit
from streakApp.models import Streak
import json


session = requests.Session()

'''COMPONENTS MODULE'''

'''In this part, it will be tested the functions that allow the creation, return the details of a habit,
marks a check off when the user completes the task and, mask the habit as complete. Additionally, for this testing
the habit is removed as the analytic module is based in the predefined habits'''

'''create a habit function sends a dicc with the data, post the data in the db which returns a string that it is converted
into a dicc so it can be tested in the function. The function looks for the object in the db and compares the description to 
confirm that it was added correctly'''

data= {"idUserFk":"1",
    "habitDescription":"habit to be tested",
    "habitPeriodicity":"8"}

post_habit = str(session.post("http://localhost:8000/habit/create/", data).content)
dicc_post_habit = json.loads(post_habit[2:-1])

def test_create():
    assert str(Habit.objects.get(idHabit=dicc_post_habit["idHabit"]).habitDescription) == "habit to be tested"

'''returns the detail of a given habit which is going to be the same that was created with the previous test and compares
the data returned by the function above with the data return by the function for detail which is converted in both cases to 
a dictionary accesibility'''

detail_habit = str(session.get(f"http://localhost:8000/habit/detail/{int(dicc_post_habit['idHabit'])}/").content)
dicc_detail_habit = json.loads(detail_habit[2:-1])

def test_detail():
    assert dicc_detail_habit["Habit"]["idHabit"] == dicc_post_habit["idHabit"]

'''to check off a habit, it is sent the ID of the habit which is found in the db and increases the checkoff count in the streak which is 
currently active for the habit. In this case, it is checked off 4 times the streak so the streak is searched and compared the 
attribute for checkoff with the amount of time it was done'''

session.put(f"http://localhost:8000/streak/checkoff/{int(dicc_post_habit['idHabit'])}/")
session.put(f"http://localhost:8000/streak/checkoff/{int(dicc_post_habit['idHabit'])}/")
session.put(f"http://localhost:8000/streak/checkoff/{int(dicc_post_habit['idHabit'])}/")
session.put(f"http://localhost:8000/streak/checkoff/{int(dicc_post_habit['idHabit'])}/")

def test_check_off():
    test_habit = get_object_or_404(Habit, pk=dicc_post_habit['idHabit'])
    test_streak = Streak.objects.get(idHabitFk=test_habit.idHabit,streakStatus = True)
    assert test_streak.streakCheckOff == 4

'''To mark a habit as complete, it uses the data from the first function to send the habit that we want to mark as complete
and then it is searched the habit in the db to compare the attribute for the status'''

session.put(f"http://localhost:8000/habit/complete/{dicc_post_habit['idHabit']}/")

def test_complete_habit():
    test_habit = get_object_or_404(Habit, pk=dicc_post_habit['idHabit'])
    assert test_habit.habitStatus == True


'''finally to maintain the predeifne data, the habit is deleted from database'''
def test_delete_habit():
    session.delete(f"http://localhost:8000/habit/delete/{dicc_post_habit['idHabit']}/").content

'''ANALYTICS MODULE'''

'''For this part of the testing, it is important to not use any services from the CLI yet as the tests were created
using the predefined habits to highlight the benftis of these'''

'''the function returns a json of all currently tracked habits which is then converted into a list to find the amount of 
entries that the db has'''

def test_list():
    result = str(session.get("http://localhost:8000/habit/list").content)
    list_objects_all = list(result[4:-3].split("},{"))
    assert len(list_objects_all) == 6

'''the function returns a list of all habits with the same periodicity for this example, the periodicity will be 1 day'''

def test_periodicity():
    result = str(session.get("http://localhost:8000/habit/periodicity/1/").content)
    list_periodicity = list(result[4:-3].split("},{"))
    assert len(list_periodicity) == 2

'''the function returns the longest run streak of all defined habits and for this case is 29 days'''

def test_longest_run():
    post_habit = str(session.get("http://localhost:8000/streak/longest_run/").content)
    dicc_post_habit = json.loads(post_habit[2:-1])
    assert dicc_post_habit["streakCheckOff"] == 29

'''return the longest run streak for a given habit which is the habit #1 and the longest is 16.'''

def test_spec_longest_run():
    post_habit = str(session.get("http://localhost:8000/streak/longest_run_specific/1/").content)
    dicc_post_habit = json.loads(post_habit[2:-1])
    assert dicc_post_habit["streakCheckOff"] == 16