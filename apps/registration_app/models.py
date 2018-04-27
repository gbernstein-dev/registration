from __future__ import unicode_literals
from django.db import models
import bcrypt

class BlogManager(models.Manager):
  def validator(self, data):
    errors = {}
    for key in data:
      if 'login' in key:
        if len(data['email']) == 0 or len(data['password']) == 0:
          errors['email'] = 'email/password cannot be empty.'
        elif User.objects.filter(email = data['email']).exists() == False:
          errors['email'] = 'email does not exist in database.'
        elif bcrypt.checkpw(data['password'].encode(), User.objects.filter(email = data['email']).first().password.encode()) == False:
          errors['password'] = 'incorrect password.'
    return errors

class User(models.Model):
  name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = BlogManager()


  
