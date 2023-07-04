from django.shortcuts import render
# from .models import 
# Create your views here.

def get_table(request):
    template = 'datatable/Datatable.html'
    return render(request, template)