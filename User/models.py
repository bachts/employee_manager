import jwt

from django.db import models
from datetime import datetime
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from Employee.models import Employee

class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not username: 
            raise ValueError('The username must be provided')
        if not email:
            raise ValueError('The email must be provided')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

class User(PermissionsMixin, AbstractBaseUser):
    
    full_name = models.CharField(max_length=50)
    employee = models.OneToOneField(Employee,
                                    on_delete=models.SET_NULL,
                                    primary_key=True)
    class Gender(models.TextChoices):
        m = 'M', _('Male')
        f = 'F', _('Female')
        other = 'Other', _('Other')
    gender = models.CharField(choices=Gender.choices)

    birth_date = models.DateField()
    phone_number = PhoneNumberField(region='VN')
    
    email_address = models.EmailField(validators=[validators.validate_email],
                                      unique=True,
                                      blank=False)
    USERNAME_FIELD = 'email_address'
    objects = UserManager()
    def __str__(self):
        return self.email_address
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def get_full_name(self):
        return self.full_name
    def get_short_name(self):
        return self.employee.employee_id
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SERCET_KEY, algorithm='HS256')


    job_code = models.SlugField(max_length=10)
    job_title = models.CharField(max_length=50)
    officer_title = models.CharField(max_length=50)

    location_address = models.CharField(max_length=200)
    organization_name_path = models.CharField(max_length=50)
    organization_code_path = models.SlugField(max_length=10)

    class Level(models.TextChoices):
        l0 = 'SVCNTS', _('SVCNTS')
        l1 = 'L1', _('L1')
        l2 = 'L2', _('L2')
        l3 = 'L3', _('L3')
    level = models.CharField(choices=Level.choices)
    created_by = models.CharField(max_length=50)
    updated_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)