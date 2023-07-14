from django.contrib import admin
from django.urls import path, include
from .views import get_table, get_chart, get_tutor, get_about, get_start, get_profile, logging, get_stations, get_login, \
    get_auth

urlpatterns = [
    path('Events/', get_table),
    path('Events/<int:id_event>', get_chart),
    path('Tutorial/', get_tutor),
    path('About/', get_about),
    path('Stations/', get_stations),
    path('Login/', get_login),
    path('SignUp/', get_auth),
    path('Profile/', get_profile),
    path('Logging/<int:user_id>', logging),
    path('', get_start)
]
