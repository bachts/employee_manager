from datetime import datetime
from datetime import timedelta

from django.db import models
from django.core import validators

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
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


class Employee(AbstractUser):
    #PERSONAL INFO
    first_name = None
    last_name = None
    email = None

    username = models.EmailField(
        validators=[validators.validate_email],
        max_length=255,
        unique=True,
        editable=False,
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    full_name = models.CharField(max_length=50)

    class Gender(models.IntegerChoices):
        Male = 1, 'Male'
        Female = 2, 'Female'
        Other = 3, 'Other'
        Unk = 4, 'Unknown'
    gender = models.PositiveSmallIntegerField(choices=Gender.choices, default=Gender.Unk, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    job_code = models.CharField(max_length=20)
    job_title = models.CharField(max_length=50)
    officer_title = models.CharField(max_length=50)

    location_address = models.CharField(max_length=200)
    organization_name_path = models.CharField(max_length=50)
    organization_code_path = models.CharField(max_length=50)


    class Level(models.IntegerChoices):
        NO_LEVEL = -1, 'No Level'
        SVCNTS = 0, 'SVCNTS'
        L1 = 1, 'L1'
        L2 = 2, 'L2'
        L3 = 3, 'L3' 

    level = models.SmallIntegerField(choices=Level.choices, default=Level.NO_LEVEL)

    created_by = models.CharField(editable=False, null=True)
    updated_by = models.CharField(default=None, null=True)

    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)

    date_in = models.DateField(default=None, null=True)
    date_out = models.DateField(default=None, null=True)

    #ADMIN INFO
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)




    #Employee Info
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    id = models.BigAutoField(primary_key=True)

    class Position(models.TextChoices):
        c1 = 'C1', _('Position 1')
        c2 = 'C2', _('Position 2')
    position = models.CharField(choices=Position.choices)

    is_manager = models.BooleanField(default=False, editable=False)
    manages = models.ManyToManyField('self', symmetrical=False, null=True, blank=True)
    def __str__(self):
        return self.full_name
   
    