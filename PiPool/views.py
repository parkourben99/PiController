from django.http import HttpResponse
from django.shortcuts import render_to_response
from PiPool.gpio import *


def index(request):
    return HttpResponse("Hello, world.")


def login(request):
    return render_to_response("login.html")


def dashboard(request):
    return HttpResponse("Dash")
