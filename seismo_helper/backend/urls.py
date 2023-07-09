from django.contrib import admin
from django.urls import path, include
from .views import get_table, get_chart, get_tutor, get_about
urlpatterns = [
    path('Events/', get_table),
    path('Events/<int:id_event>', get_chart),
    path('Tutorial/', get_tutor),
    path('About/', get_about),
]
