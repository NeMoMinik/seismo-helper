from django.contrib import admin
from django.urls import path, include
from .views import get_table, get_chart, get_tutor, get_about, get_start, get_profile, get_login, get_stations
urlpatterns = [
    path('Events/', get_table),
    path('Events/<int:id_event>', get_chart),
    path('Tutorial/', get_tutor),
    path('About/', get_about),
    path('Stations/', get_stations),
    path('Login/', get_login),
    path('Profile/', get_profile),
    path('', get_start)
]
