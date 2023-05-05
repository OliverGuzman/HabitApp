from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

'''Verifies that the information and save the user'''
class UserManager(BaseUserManager):
    def create_user(self, username, password = None):
        if not username:
            raise ValueError('Username not valid')
        user = self.model(username = username)
        user.set_password(password)
        user.save(using = self._db)
        return user

'''Model for user's attributes and creates save function'''
class User(AbstractBaseUser, PermissionsMixin):
    idUserApp = models.BigAutoField(primary_key = True)
    username = models.CharField('Username',max_length = 11, unique = True)
    password = models.CharField('Password', max_length = 128)

    def save(self,*args ,**kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_idUserApp(self):
        return self.idUserApp


    objects = UserManager()
    USERNAME_FIELD = 'username'

    