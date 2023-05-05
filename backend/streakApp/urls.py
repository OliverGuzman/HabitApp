from django.urls import path

from . import views

'''urls for streak CRUD'''
urlpatterns = [
    path('create/',views.StreakCreateView.as_view(), name ='streak-create'),
    path('checkoff/<int:pk>/',views.streak_check_off, name ='streak-checkOff'),
    path('longest_run/',views.streak_longest_run, name ='streak-longest-run'),
    path('longest_run_specific/<int:pk>/',views.streak_longest_run_specific, name ='streak-longest-run-specific'),
    path('delete/<int:pk>/',views.StreakDeleteView.as_view(), name ='streak-delete'),
]