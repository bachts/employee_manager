import jwt

from datetime import datetime
from datetime import timedelta

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import gettext_lazy as _


# Create your models here.

class Department(models.Model):
    department_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, default='Department name')
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)    


    def __str__(self):
        return self.name
    
class Team(models.Model):
    team_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, default='Team name')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 


class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    employee_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Position(models.TextChoices):
        c1 = 'C1', _('Position 1')
        c2 = 'C2', _('Position 2')
    position = models.CharField(choices=Position.choices)

    is_manager = models.BooleanField(default=False)
    manages = models.ManyToManyField('self', symmetrical=False)
    def __str__(self):
        return self.name
