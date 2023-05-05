from django.urls import path

from . import views

'''urls for user CRUD'''
urlpatterns = [
    path('create/',views.UserCreateView.as_view(), name ='user-create'),
    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='user-delete')
]