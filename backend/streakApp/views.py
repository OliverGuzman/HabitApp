from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.http import JsonResponse

from habitApp.models import Habit

from streakApp.models import Streak
from streakApp.serializer import StreakSerializer

'''create a streak'''
class StreakCreateView(generics.CreateAPIView):
    queryset = Streak.objects.all()
    serializer_class = StreakSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

'''check off the current streak active for the habit'''
@api_view(['PUT'])
def streak_check_off(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'PUT':
        if pk is not None:
            dataHabit = get_object_or_404(Habit, pk=pk)

            try:
                currentStreak = Streak.objects.get(idHbitFk=dataHabit.idHabit, streakStatus=True)
                currentStreak.set_streakLastCheckOffDate(datetime.today())
                currentStreak.set_streakNextDate(datetime.today()+ timedelta(days=dataHabit.habitPeriodicity))
                currentStreak.set_streakCheckOff()
                currentStreak.save()

                return Response("CheckOff complete")
            
            except:
                return Response("No active Streak")

'''return the strak with the longest run for any habit'''    
@api_view(['GET'])
def streak_longest_run(request, *args, **kwargs):
    method = request.method

    if method == 'GET':
        queryset = list(Streak.objects.all())
        longest = 0
        resultStreak = {}
        for streakIn in queryset:
            if streakIn.streakCheckOff > longest:
                longest = streakIn.streakCheckOff
                resultStreak = StreakSerializer(streakIn).data
        return Response(resultStreak)

'''return the strak with the longest run for a specific habit''' 
@api_view(['GET'])
def streak_longest_run_specific(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        if pk != None:
            queryset = list(Streak.objects.filter(idHbitFk=pk))
            longest = 0
            resultStreak = {}
            for streakIn in queryset:
                if streakIn.streakCheckOff > longest:
                    longest = streakIn.streakCheckOff
                    resultStreak = StreakSerializer(streakIn).data
                elif longest == 0:
                    return Response("No streak has been checked off")
            return Response(resultStreak)

'''delete a given streak'''
class StreakDeleteView(generics.DestroyAPIView):
    queryset = Streak.objects.all()
    serializer_class = StreakSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)