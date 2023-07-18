import datetime
import jwt
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

from django.utils import timezone

# Create your models here.

LEVEL_CHOICES = (
    ('0', 'SVCNTS'),
    ('1', 'L1'),
    ('2', 'L2'),
    ('3', 'L3')
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, gender, birthday, phone_number, job_code, job_title,
                    officer_title, location_address, organization_name_path, organization_code_path,
                    level, date_in, password=None, **kwargs):
        if not email:
            raise ValueError('Email must be supplied')
        
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            gender = gender,
            birthday = birthday,
            phone_number = phone_number,
            job_code = job_code,
            job_title = job_title,
            officer_title = officer_title,
            location_address = location_address,
            organization_name_path = organization_name_path,
            organization_code_path = organization_code_path,
            level = level,
            date_in = date_in,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, full_name, gender, birthday, phone_number, job_code, job_title,
                    officer_title, location_address, organization_name_path, organization_code_path,
                    level, date_in, password=None, **kwargs):
        
        user = self.create_user(
            email = self.normalize_email(email),
            full_name = full_name,
            gender = gender,
            birthday = birthday,
            phone_number = phone_number,
            job_code = job_code,
            job_title = job_title,
            officer_title = officer_title,
            location_address = location_address,
            organization_name_path = organization_name_path,
            organization_code_path = organization_code_path,
            level = level,
            date_in = date_in,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
            

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name', 'gender', 'birthday', 'phone_number', 'job_code', 'job_title',
                       'officer_title', 'location_address', 'organization_name_path', 'organization_code_path',
                       'level', 'date_in']


    #PERSONAL INFO
    full_name = models.CharField(max_length=50)

    class Gender(models.IntegerChoices):
        Male = 1, 'Male'
        Female = 2, 'Female'
        Other = 3, 'Other'
        Unk = 4, 'Unknown'
    gender = models.PositiveSmallIntegerField(choices=Gender.choices, default=Gender.Unk)
    birthday = models.DateField(null=True)
    phone_number = models.CharField(max_length=12, null=True)
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

    created_by = models.CharField(editable=False)
    updated_by = models.CharField(default=None, null=True)

    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)

    date_in = models.DateField(default=None, null=True)
    date_out = models.DateField(default=None, null=True)

    #ADMIN INFO
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    #FUNCTIONS
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    #PROPERTY
    objects = MyUserManager()
    @property
    def is_staff(self):
        return self.is_admin
    def get_full_name(self):
        return self.full_name
    def token(self):
        return self._generate_jwt_token()
    def _generate_jwt_token(self):
        dt = datetime.datetime.now() + datetime.timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return jwt.decode(jwt=token,
                          key=settings.SECRET_KEY,
                          algorithms='HS256')
