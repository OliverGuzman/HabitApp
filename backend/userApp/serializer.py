from rest_framework import serializers
from .models import User

'''serializer for user'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
