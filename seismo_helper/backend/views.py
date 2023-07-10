from django.shortcuts import render
from .models import Trace, Event
from data_table.dash.MainPage import update_output
from django.template import RequestContext
from django.http import HttpResponse, HttpRequest
import requests as rq
from django.views.decorators.csrf import csrf_exempt
import flask
rq.session()

def get_table(request):
    update_output('Все')
    template = 'datatable/Datatable.html'
    return render(request, template)


def get_chart(request, id_event):
    template = 'datatable/Chart.html'
    context = {'dash_context': {'id_event': {'value': id_event}}}
    print(request.COOKIES)
    response = render(request, template, context=context)
    response.set_cookie('last_connection', "123321")
    return response


def get_tutor(request):
    template = 'datatable/TutorPage.html'
    return render(request, template)


def get_about(request):
    template = 'datatable/AboutPage.html'
    return render(request, template)


@csrf_exempt
def logged(request):
    if request.method == "POST":
        print(request.POST)
        response = render(request, 'datatable/Datatable.html')
        response.set_cookie('Authorization', f'Token {request.POST["Authorization"]}')
    else:
        response = render(request, 'datatable/LoginPage.html')
    #     r = rq.post("http://127.0.0.1:8088/auth/token/login/", data=request.POST).json()
    #     print(r)
    #     if "auth_token" in r:
    # r = rq.post("http://127.0.0.1:8000/auth/token/login/", data={"username": username, "password": password}).json()
    return response


def get_profile(request):
    template = 'datatable/ProfilePage.html'
    return render(request, template)


def get_login(request):
    template = 'datatable/LoginPage.html'
    print(request.COOKIES)
    return render(request, template)


def get_stations(request):
    template = 'datatable/AddStations.html'
    return render(request, template)


def get_start(request):
    template = 'datatable/StartPage.html'
    return render(request, template)