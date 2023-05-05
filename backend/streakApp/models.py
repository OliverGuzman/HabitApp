from django.db import models
from habitApp.models import Habit

'''model for streak'''
class Streak(models.Model):
    idStreak = models.BigAutoField(primary_key=True)
    idHbitFk = models.ForeignKey(Habit, related_name = 'streak', on_delete = models.CASCADE, null=False)
    '''date when the streak was created'''
    streakStartDate = models.DateTimeField()
    '''date when the streak was checked on time'''
    streakLastCheckOffDate = models.DateTimeField(null=True)
    '''date for next check'''
    streakNextDate = models.DateTimeField()
    '''date when the streak was closed'''
    streakLastDate = models.DateTimeField(null=True)
    '''check off count'''
    streakCheckOff = models.IntegerField(default=0)
    streakStatus = models.BooleanField(default=True)

    def set_streakLastCheckOffDate(self, date):
        self.streakLastCheckOffDate = date
    
    def set_streakNextDate(self, date):
        self.streakNextDate = date
    
    def set_streakLastDate(self, date):
        self.streakLastDate = date

    def set_streakCheckOff(self):
        self.streakCheckOff += 1

    def set_streakStatus(self, status):
        self.streakStatus = status

    

    
    
