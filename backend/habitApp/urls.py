from django.urls import path

from . import views

'''urls for habit CRUD'''
urlpatterns = [
    #path('create/',views.HabitCreateView.as_view(), name ='habit-create'),
    path('create/',views.habit_create, name ='habit-create'),
    path('detail/<int:pk>/',views.HabitDetailView.as_view(), name ='habit-detail'),
    path('list/',views.HabitListView.as_view(), name ='habit-list'),
    path('periodicity/<int:pk>/',views.habit_same_periodicity, name ='habit-periodicity'),
    path('reactivate/<int:pk>/',views.habit_reactivate_status, name ='habit-reactivate'),
    path('complete/<int:pk>/',views.habit_complete_status, name ='habit-complete'),
    path('delete/<int:pk>/',views.HabitDeleteView.as_view(), name ='habit-delete'),
]