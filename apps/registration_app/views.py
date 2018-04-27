from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import bcrypt

def index(request):
  print User.objects.count()
  return render(request, 'registration_app/index.html')

def login(request):
  errors = User.objects.validator(request.POST)
  if len(errors):
    for tag, error in errors.iteritems():
      messages.error(request, error, extra_tags=tag)
    return redirect('/landing')
  else:
    encrypted = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if User.objects.filter(email=request.POST['email']):
      request.session['current_user'] = User.objects.filter(email=request.POST['email'])[0].id
      return redirect('/landing/success')
    else:
      print 'invalid email'
      return redirect('/landing')

def create(request):
  errors = User.objects.validator(request.POST)
  if len(errors):
    for tag, error in errors.iteritems():
      messages.error(request, error, extra_tags=tag)
    return redirect('/landing')
  else:
    encrypted = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(name=request.POST['name'],email=request.POST['email'],password=encrypted)
    if bcrypt.checkpw(request.POST['password_confirm'].encode(), encrypted.encode()):
      user.save()
      request.session['current_user'] = User.objects.filter(email=request.POST['email'])[0].id
      return redirect('/landing/success')
    else:
      return redirect('/landing')

def success(request):
  context = {
    'user': User.objects.filter(id=request.session['current_user'])
  }
  print request.session['current_user']
  return render(request, 'registration_app/success.html', context)

def logout(request):
  if request.session['current_user']:
    return redirect('/landing')