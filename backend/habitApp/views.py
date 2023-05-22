from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from streakApp.models import Streak
from streakApp.serializer import StreakSerializer

from habitApp.models import Habit
from habitApp.serializer import HabitSerializer

'''The create a habit. It will be used a personalized function as it will also add the streak at the same time'''
@api_view(['POST'])
def habit_create(request, pk=None, *args, **kwargs):
    method = request.method
    dataReturn = {}
    data ={}

    if method == "POST":
        serializer = HabitSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            idUserFk = serializer.validated_data.get("idUserFk")
            habitDescription = serializer.validated_data.get("habitDescription")
            habitPeriodicity = serializer.validated_data.get("habitPeriodicity")    
            serializer.save(idUserFk=idUserFk, habitDescription=habitDescription,habitPeriodicity=habitPeriodicity)
            dataReturn = serializer.data

        if dataReturn != None:
            finalData = {}
            finalData["idHabitFk"]=Habit.objects.get(idHabit=dataReturn["idHabit"]).idHabit
            finalData["streakStartDate"]=str(datetime.today())
            finalData["streakNextDate"]=str(datetime.today()+ timedelta(days=habitPeriodicity))
            serializer = StreakSerializer(data=finalData)

            if serializer.is_valid(raise_exception=True):
                idHabitFk = serializer.validated_data.get("idHabitFk")
                streakStartDate = serializer.validated_data.get("streakStartDate")
                streakNextDate = serializer.validated_data.get("streakNextDate")
                serializer.save(idHabitFk=idHabitFk,streakStartDate=streakStartDate,streakNextDate=streakNextDate)
                data["idHabit"]=idHabitFk.get_id()
                data["idStreak"]=serializer.data["idStreak"]

                return Response(data)

'''Marks as complete or "status = false" for both the streak and the habit and adds the final dates for "streakLastDate'''
@api_view(['PUT'])
def habit_complete_status(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "PUT":
        if pk is not None:
            dataHabit = get_object_or_404(Habit, pk=pk)

            try:
                dataStreak = Streak.objects.get(idHabitFk=dataHabit.idHabit,streakStatus = False)
                dataHabit.set_habitStatus(True)
                dataStreak.set_streakLastDate(datetime.now())
                dataStreak.set_streakStatus(True)
                dataHabit.save()
                dataStreak.save()
                return Response("The habit is complete")
            except:
                return Response("This habit was already complete")

'''Using a previous created habit, it creates a new streak'''
@api_view(['PUT'])
def habit_reactivate_status(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "PUT":
        if pk is not None:
            dataHabit = get_object_or_404(Habit, pk=pk)
            
            if dataHabit != None and dataHabit.habitStatus != False:
                finalData = {}
                dataHabit.set_habitStatus(False)
                dataHabit.save()
                finalData["idHabitFk"]=Habit.objects.get(idHabit=dataHabit.idHabit).idHabit
                finalData["streakStartDate"]=str(datetime.today())
                finalData["streakNextDate"]=str(datetime.today()+ timedelta(days=dataHabit.habitPeriodicity))
                serializer = StreakSerializer(data=finalData)

                if serializer.is_valid(raise_exception=True):
                    idHabitFk = serializer.validated_data.get("idHabitFk")
                    streakStartDate = serializer.validated_data.get("streakStartDate")
                    streakNextDate = serializer.validated_data.get("streakNextDate")
                    serializer.save(idHabitFk=idHabitFk,streakStartDate=streakStartDate,streakNextDate=streakNextDate)

                    return Response("Habit ID: "+str(dataHabit.idHabit)+" "+"Streak ID: "+str(serializer.data["idStreak"]))


            return Response("It is already active")
    
'''return the details of a given habit by a PK'''    
@api_view(['GET'])
def detail_full_view(request, pk=None, *args,**kwargs):
    method = request.method

    if method == "GET":

        if pk is not None:
            data={}
            detail_habit = get_object_or_404(Habit, pk=pk)
            data["Habit"] = HabitSerializer(detail_habit, many=False).data

            if detail_habit.habitStatus != True:
                detail_streak = Streak.objects.get(idHabitFk=detail_habit.idHabit,streakStatus = False)
        
                data["Streak"]=StreakSerializer(detail_streak,many=False).data
                
                return Response(data)
            else:
                return Response(data)
    
'''return a list of all habits'''
class HabitListView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        return super().get_queryset()

'''return a list of all habits with the same periodicity'''
@api_view(['GET'])
def habit_same_periodicity(request, pk=None, *args, **kwargs):
    method = request.method    

    if method == 'GET':
        if pk is not None:
            queryset = Habit.objects.filter(habitPeriodicity=pk)
            data = HabitSerializer(queryset, many=True).data
            return Response(data)
    
'''deletes a given habit by a PK'''    
class HabitDeleteView(generics.DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
        
        

