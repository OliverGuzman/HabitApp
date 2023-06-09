from django.db import models
from userApp.models import User

'''model for habit'''
class Habit(models.Model):
    idHabit = models.BigAutoField(primary_key = True, unique=True, editable=True)
    idUserFk = models.ForeignKey(User, related_name = 'habit', on_delete = models.CASCADE, null=False)
    habitDescription = models.CharField('Description', max_length= 256)
    habitPeriodicity = models.IntegerField()
    habitStatus = models.BooleanField(default=False)

    '''return the idHabit as an int'''
    def get_id(self):
        return self.idHabit
    
    '''set the habitStatus according to the input'''
    def set_habitStatus(self, status):
        self.habitStatus=status