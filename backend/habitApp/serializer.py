from rest_framework import serializers

from habitApp.models import Habit
'''serializer for habit'''
class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
                "idHabit",
                'idUserFk',
                'habitDescription',
                'habitPeriodicity',
                'habitStatus'
                   ]

    '''how the JSON will be send a response or receive'''        
    def to_representation(self, obj):
        habit = Habit.objects.get(idHabit = obj.idHabit)
        return {
                'idHabit': habit.idHabit,
                'idUserFk': habit.idUserFk.get_idUserApp(),
                'habitDescription': habit.habitDescription,
                'habitPeriodicity': habit.habitPeriodicity,
                'habitStatus': habit.habitStatus,
        }