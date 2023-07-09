from django.shortcuts import render
from .models import Trace, Event
from data_table.dash.MainPage import update_output


def get_table(request):
    update_output('Все')
    template = 'datatable/Datatable.html'
    return render(request, template)


def get_chart(request, id_event):
    template = 'datatable/Chart.html'
    context = {'dash_context': {'id_event': {'value': id_event}}}
    return render(request, template, context=context)

def get_tutor(request):
    template = 'datatable/TutorPage.html'
    return render(request, template)

def get_about(request):
    template = 'datatable/AboutPage.html'
    return render(request, template)

def get_profile(request):
    template = 'datatable/ProfilePage.html'
    return render(request, template)

def get_login(request):
    template = 'datatable/LoginPage.html'
    return render(request, template)

def get_stations(request):
    template = 'datatable/AddStations.html'
    return render(request, template)

def get_start(request):
    template = 'datatable/StartPage.html'
    return render(request, template)