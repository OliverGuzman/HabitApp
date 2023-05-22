import questionary
import requests
import json
from pprint import pprint

session = requests.Session()

def cli():
    turn_off = True
    
    if questionary.confirm("Hello. Welcome to the HabitApp, really?").ask() == True:
        while turn_off:
            answer = questionary.select("What would you like to do?",
                                            choices=["Create a habit",
                                                    "See the details of a habit",
                                                    "List all habits",
                                                    "Check off a habit",
                                                    "Complete a habit",
                                                    "Reactivate a habit",
                                                    "See all habit with a specific periodicty",
                                                    "See the streak with the longest run",
                                                    "See the streak with the longest run for a specific habit",
                                                    "Exit"]).ask()
            
            if answer == "Create a habit":
                data = {}
                data["idUserFk"] = "1"
                habitDescription = questionary.text("What is the description of the habit?").ask()
                count=1
                while count <= 3:
                    if habitDescription != "":
                        data["habitDescription"] = habitDescription
                        break

                    elif count < 3 and habitDescription == "":
                        print("Not a valid habit description as it cannot be empty...")
                        habitDescription = questionary.text("What is the description of the habit?").ask()
                        count+=1
                    
                    elif count ==3:
                        print("Too many attempts, thanks for using the HabitApp")
                        return None      

                habitPeriodicity = str(questionary.text("What is the periodicity? Enter a number").ask())
                count=1
                while count <= 3:
                    if habitPeriodicity.isnumeric() and habitPeriodicity != "":
                        data["habitPeriodicity"] = habitPeriodicity
                        break

                    elif count < 3 and habitPeriodicity.isnumeric() == False:
                        print("Not a valid habit periodicity as it is not a number...")
                        habitPeriodicity = str(questionary.text("What is the periodicity? Enter a number").ask())
                        count+=1
                    
                    elif count ==3:
                        print("Too many attempts, thanks for using the HabitApp")
                        return None 
                    
                post_habit = str(session.post("http://localhost:8000/habit/create/", data).content)
                dicc_post_habit = json.loads(post_habit[2:-1])
                print(f"The habit was created correctly and the idHabit is {dicc_post_habit['idHabit']}")

            elif answer == "See the details of a habit":
                count = 1
                while count <= 3:
                    in_question_habit = str(questionary.text("Which habit do you want to see? Enter a the idHabit number").ask())

                    if in_question_habit.isnumeric() and in_question_habit != "":
                        detail_habit = str(session.get(f"http://localhost:8000/habit/detail/{int(in_question_habit)}/").content)
                        dicc_detail_habit = json.loads(detail_habit[2:-1])

                        try:
                            if dicc_detail_habit['detail'] == 'Not found.':
                                print("No current habit has the provided ID")
                                count+=1

                                if count == 4:
                                    print("Too many attempts, thanks for using the HabitApp")
                                    return None
                                
                                continue

                        except:
                            pprint(dicc_detail_habit)
                            break

                    elif count < 3 and in_question_habit.isnumeric() == False or in_question_habit != "":
                        print("Not a valid idHabit as it is not a number...")
                        count+=1
                    
                    elif count ==3:
                        print("Not a valid idHabit as it is not a number...")
                        print("Too many attempts, thanks for using the HabitApp")
                        return None 

            elif answer == "List all habits":
                result = str(session.get("http://localhost:8000/habit/list").content)
                list_objects_all = list(result[4:-3].split("},{"))
                for object in list_objects_all:
                    print(object)

            elif answer == "Check off a habit":
                count = 1
                while count <= 3:
                    in_question_habit = str(questionary.text("Which habit do you want to check off? Enter a the idHabit number").ask())

                    if in_question_habit.isnumeric() and in_question_habit != "":
                        result_checkoff = str(session.put(f"http://localhost:8000/streak/checkoff/{int(in_question_habit)}/").content)

                        if result_checkoff[3:-2] == "CheckOff complete":
                            print("CheckOff complete")
                            break
                        
                        elif result_checkoff[3:-2] == "No active Streak":
                            print("No active Streak")
                            break

                        elif result_checkoff[3:-2] == "The habit was missed":
                            print("The habit was missed")
                            break

                        elif result_checkoff[2:-1] == '{"detail":"Not found."}':
                            print("No current habit has the provided ID")
                            count +=1
                            if count == 4:
                                print("Too many attempts, thanks for using the HabitApp")
                                return None
                            
                    elif count < 3 and in_question_habit.isnumeric() == False or in_question_habit != "":
                        print("Not a valid idHabit as it is not a number...")
                        count+=1
                    
                    elif count == 3:
                                print("Not a valid idHabit as it is not a number...")
                                print("Too many attempts, thanks for using the HabitApp")
                                return None

            elif answer == "Complete a habit":
                count = 1
                while count <= 3:
                    in_question_habit = str(questionary.text("Which habit do you want to mark as complete? Enter a the idHabit number").ask())

                    if in_question_habit.isnumeric() and in_question_habit != "":
                        result_complete = str(session.put(f"http://localhost:8000/habit/complete/{int(in_question_habit)}/").content)

                        if result_complete[3:-2] == "The habit is complete":
                            print("The habit is complete")
                            break
                        
                        elif result_complete[3:-2] == "This habit was already complete":
                            print("This habit was already complete")
                            break

                        elif result_complete[2:-1] == '{"detail":"Not found."}':
                            print("No current habit has the provided ID")
                            count +=1
                            if count == 4:
                                print("Too many attempts, thanks for using the HabitApp")
                                return None

                    elif count < 3 and in_question_habit.isnumeric() == False or in_question_habit != "":
                        print("Not a valid idHabit as it is not a number...")
                        count+=1
                    
                    elif count == 3:
                                print("Not a valid idHabit as it is not a number...")
                                print("Too many attempts, thanks for using the HabitApp")
                                return None                        

            elif answer == "Reactivate a habit":
                count = 1
                while count <= 3:
                    in_question_habit = str(questionary.text("Which habit do you want to reactivate? Enter a the idHabit number").ask())

                    if in_question_habit.isnumeric() and in_question_habit != "":
                        result_reactivate = str(session.put(f"http://localhost:8000/habit/reactivate/{int(in_question_habit)}/").content)

                        if result_reactivate[3:-2] == "It is already active":
                            print("It is already active")
                            break

                        elif result_reactivate[2:-1] == '{"detail":"Not found."}':
                            print("No current habit has the provided ID")
                            count +=1
                            if count == 4:
                                print("Too many attempts, thanks for using the HabitApp")
                                return None
                        else:
                            print(result_reactivate)
                            break
                    
                    elif count < 3 and in_question_habit.isnumeric() == False or in_question_habit != "":
                        print("Not a valid idHabit as it is not a number...")
                        count+=1
                    
                    elif count == 3:
                                print("Not a valid idHabit as it is not a number...")
                                print("Too many attempts, thanks for using the HabitApp")
                                return None 

            elif answer == "See all habit with a specific periodicty":
                count = 1
                while count <= 3:
                    in_question_habit = str(questionary.text("Which periodicity do you want to check? Enter a the idHabit number").ask())
                    
                    if in_question_habit.isnumeric() and in_question_habit != "":
                        result = str(session.get(f"http://localhost:8000/habit/periodicity/{int(in_question_habit)}/").content)
                        list_objects_all = list(result[4:-3].split("},{"))
                        for object in list_objects_all:
                            print(object)
                        break

                    elif count < 3 and in_question_habit.isnumeric() == False or in_question_habit != "":
                        print("Not a valid idHabit as it is not a number...")
                        count+=1
                    
                    elif count == 3:
                                print("Not a valid idHabit as it is not a number...")
                                print("Too many attempts, thanks for using the HabitApp")
                                return None 

            elif answer == "See the streak with the longest run":
                result = str(session.get(f"http://localhost:8000/streak/longest_run/").content)
                list_objects_all = list(result[4:-3].split("},{"))
                for object in list_objects_all:
                    print(object)

            elif answer == "See the streak with the longest run for a specific habit":
                count = 1
                while count <= 3:
                    in_question_habit = str(questionary.text("Which habit do you want to check? Enter a the idHabit number").ask())

                    if in_question_habit.isnumeric() and in_question_habit != "":
                        result = str(session.get(f"http://localhost:8000/streak/longest_run_specific/{int(in_question_habit)}/").content)
                        list_objects_all = list(result[4:-3].split("},{"))
                        for object in list_objects_all:
                            print(object)
                            break

                    elif count < 3 and in_question_habit.isnumeric() == False or in_question_habit != "":
                        print("Not a valid idHabit as it is not a number...")
                        count+=1
                    
                    elif count == 3:
                                print("Not a valid idHabit as it is not a number...")
                                print("Too many attempts, thanks for using the HabitApp")
                                return None 
            
            elif answer == "Exit":
                print("Thanks for using HabitApp")
                turn_off = False
        
    else:
        print("Thanks for using HabitApp")
        turn_off = False


if __name__ == '__main__':
    cli()