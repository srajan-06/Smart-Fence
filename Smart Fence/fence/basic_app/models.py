from django.db import models
from django.contrib.auth.models import User,PermissionsMixin

#Using builting user model to create users
class User(User,PermissionsMixin):
  def __str__(self):
    return "@{}".format(self.username)
