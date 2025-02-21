from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("سلام، این اولین صفحه من در Django است! 🚀")
