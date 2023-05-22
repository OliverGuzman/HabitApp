from rest_framework import serializers

from streakApp.models import Streak
'''serializer for streak'''
class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = [
            'idStreak',
            'idHabitFk',
            'streakStartDate',
            'streakNextDate',
        ]
    '''how the JSON will be send a response or receive'''
    def to_representation(self, obj):
        streak = Streak.objects.get(idStreak = obj.idStreak)
        return {
                'idStreak':streak.idStreak,
                'idHabitFk':streak.idHabitFk.idHabit,
                'streakStartDate': streak.streakStartDate,
                'streakLastCheckOffDate': streak.streakLastCheckOffDate,
                'streakNextDate': streak.streakNextDate,
                'streakLastDate': streak.streakLastDate,
                'streakCheckOff': streak.streakCheckOff,
                'streakStatus':streak.streakStatus,
        }

