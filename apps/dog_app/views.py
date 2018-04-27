from django.shortcuts import render, HttpResponse, redirect
from models import *
import bcrypt

def index(request):
  return render(request, 'dog_app/index.html')