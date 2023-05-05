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
            finalData["idHbitFk"]=Habit.objects.get(idHabit=dataReturn["idHabit"]).idHabit
            finalData["streakStartDate"]=str(datetime.today())
            finalData["streakNextDate"]=str(datetime.today()+ timedelta(days=habitPeriodicity))
            serializer = StreakSerializer(data=finalData)

            if serializer.is_valid(raise_exception=True):
                idHbitFk = serializer.validated_data.get("idHbitFk")
                streakStartDate = serializer.validated_data.get("streakStartDate")
                streakNextDate = serializer.validated_data.get("streakNextDate")
                serializer.save(idHbitFk=idHbitFk,streakStartDate=streakStartDate,streakNextDate=streakNextDate)

                return Response("Habit ID: "+str(idHbitFk.get_id())+" "+"Streak ID: "+str(serializer.data["idStreak"]))

'''Marks as complete or "status = false" for both the streak and the habit and adds the final dates for "streakLastDate'''
@api_view(['PUT'])
def habit_complete_status(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "PUT":
        if pk is not None:
            dataHabit = get_object_or_404(Habit, pk=pk)

            try:
                dataStreak = Streak.objects.get(idHbitFk=dataHabit.idHabit,streakStatus = True)
                dataHabit.set_habitStatus(False)
                dataStreak.set_streakLastDate(datetime.now())
                dataStreak.set_streakStatus(False)
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
            dataHabit.set_habitStatus(True)
            dataHabit.save()
            
            if dataHabit != None:
                finalData = {}
                finalData["idHbitFk"]=Habit.objects.get(idHabit=dataHabit.idHabit).idHabit
                finalData["streakStartDate"]=str(datetime.today())
                finalData["streakNextDate"]=str(datetime.today()+ timedelta(days=dataHabit.habitPeriodicity))
                serializer = StreakSerializer(data=finalData)

                if serializer.is_valid(raise_exception=True):
                    idHbitFk = serializer.validated_data.get("idHbitFk")
                    streakStartDate = serializer.validated_data.get("streakStartDate")
                    streakNextDate = serializer.validated_data.get("streakNextDate")
                    serializer.save(idHbitFk=idHbitFk,streakStartDate=streakStartDate,streakNextDate=streakNextDate)

                    return Response("Habit ID: "+str(dataHabit.idHabit)+" "+"Streak ID: "+str(serializer.data["idStreak"]))


            return Response("Complete")
    
'''return the details of a given habit by a PK'''
class HabitDetailView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) 
    
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
        
        

