from django.shortcuts import render, redirect
from data_table.dash.MainPage import update_output
from data_table.dash.ProfilePage import load_profile
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import requests as rq
from django.contrib.auth import login, logout
from seismo_helper.settings import ALLOWED_HOSTS, BASE_LINK, BASE_DIR


def get_token(request):
    token = {"dash_context": {"session": {'data': {"Authorization": ""}}}}
    if request.user.is_authenticated:
        token["dash_context"]["session"]["data"]["Authorization"] = f"Token {Token.objects.get(user=request.user).key}"
    return token


def get_table(request):
    if request.user.is_authenticated:
        token = get_token(request)
        update_output('Все локации', token["dash_context"]["session"]["data"])
        template = 'datatable/Datatable.html'
        return render(request, template, context=token)
    return redirect(f'{BASE_LINK}Login/')


def get_chart(request, id_event):
    template = 'datatable/Chart.html'
    token = get_token(request)
    context = {'dash_context': {'id_event': {'value': id_event}, 'session': {"data": token['dash_context']['session']['data']}}}
    response = render(request, template, context=context)
    return response


def get_tutor(request):
    template = 'datatable/TutorPage.html'
    return render(request, template)


def get_about(request):
    template = 'datatable/AboutPage.html'
    print(request.user)
    return render(request, template)


def get_profile(request):
    template = 'datatable/ProfilePage.html'
    return render(request, template, context=get_token(request))


def get_login(request):
    template = 'datatable/LoginPage.html'
    return render(request, template, context=get_token(request))


def get_stations(request):
    template = 'datatable/AddStations.html'
    context = get_token(request)
    print(request.user)
    return render(request, template, context=context)


def get_start(request):
    template = 'datatable/StartPage.html'
    return render(request, template)


def get_auth(request):
    template = 'datatable/SignUpPage.html'
    return render(request, template, context=get_token(request))


def logging(request, user_id):
    u = get_user_model().objects.get(id=user_id)
    login(request, u)
    return redirect(f"{BASE_LINK}About/")


def get_logout(request):
    r = rq.post(f"{BASE_LINK}auth/token/logout/").json()
    print(r)
    logout(request)
    return redirect(f"{BASE_LINK}About/")


def get_locations(request):
    template = 'datatable/AddLocations.html'
    context = get_token(request)
    print(request.user)
    return render(request, template, context=context)
