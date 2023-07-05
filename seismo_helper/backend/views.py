from django.shortcuts import render
import plotly.express as px
from .models import Trace, Event
import obspy


def get_table(request):
    template = 'datatable/Datatable.html'
    return render(request, template)


def get_chart(request, id_event):
    template = 'datatable/Chart.html'
    context = {'dash_context': {'id_event': {'value': id_event}}}
    return render(request, template, context=context)
