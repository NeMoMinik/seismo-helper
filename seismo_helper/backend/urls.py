from django.contrib import admin
from django.urls import path, include
from .views import get_table, get_chart
urlpatterns = [
    path('DataTable/', get_table),
    path('DataTable/<int:id_event>', get_chart)
]