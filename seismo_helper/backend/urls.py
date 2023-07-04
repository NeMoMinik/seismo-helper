from django.contrib import admin
from django.urls import path, include
from .views import get_table
urlpatterns = [
    path('DataTable/', get_table)
]