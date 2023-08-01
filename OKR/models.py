from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta

from Employee.models import Employee
# Create your models here.
class OKR(models.Model):
    id = models.BigAutoField(primary_key=True)

    note = models.TextField(max_length=200, null=True, blank=True)

    objective = models.ForeignKey('Objective', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    kr_id = models.BigIntegerField(max_length=200, null=True, default=1)
    key_result_department = models.TextField(max_length=200, blank=False, null=False, default='department')
    key_result_team = models.TextField(max_length=200, blank=False, null=False, default='team')
    key_result_personal = models.TextField(max_length=200, blank=False, null=False, default='personal')

    formula = models.ForeignKey('Formula', blank=False, null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey('Source', blank=False, null=True, on_delete= models.SET_NULL)
    
    class Types(models.TextChoices):
        OKR = 'OKR', _('OKR')
        KPI = 'KPI', _('KPI')
    type = models.CharField(choices=Types.choices) #OKR hay KPI

    class Regularity(models.TextChoices):
        MONTHLY = 'MO', _('MONTHLY')
        QUARTERLY = 'QUAR', _('QUARTERLY')
    regularity = models.CharField(choices=Regularity.choices) #quarterly hay monthly

    class Unit(models.TextChoices):
        NUM = 'NUM', _('NUMERIC')
        CAT = 'CAT', _('CATEGORICAL')
    unit = models.CharField(choices=Unit.choices) # don vi

    class Condition(models.TextChoices):
        L = 'LESS', _('LESS THAN')
        M = 'MORE', _('MORE THAN')
        E = 'EQUAL', _('EQUAL')
        LOE = 'LOE', _('LESS OR EQUAL')
        MOE = 'MOE', _('MORE OR EQUAL')
    condition = models.CharField(choices=Condition.choices) #pass condition

    norm = models.IntegerField() #max value
    weight = models.IntegerField(validators=[MaxValueValidator(100),
                                             MinValueValidator(1)],
                                 blank=False) #trong so
    result = models.IntegerField(validators=[MaxValueValidator(100),
                                             MinValueValidator(0)],
                                 blank=True,
                                 null=True,
                                 default=None) #ket qua tung phan

    ratio = models.IntegerField(validators=[MaxValueValidator(100),
                                            MinValueValidator(0)],
                                default=0, null=False) #weight * result
    
    class Status(models.TextChoices):
        P = 'P', _('Pending Approval')
        INP = 'INP', _('In Progress')
        OK = 'S', _('Satisfactory')
        NOK = 'NS', _('Not Satisfactory')
    
    estimated = models.CharField(max_length=200, null=True)
    actual = models.CharField(max_length=200, null=True)

    status = models.CharField(choices=Status.choices, 
                              default=Status.P)

    created_by = models.CharField(max_length=30, editable=False)
    updated_by = models.CharField(max_length=30, default=None, null=True)

    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    deadline = models.DateTimeField()
    
    class Quarter(models.TextChoices):
        q1 = 'Q1', _('First Quarter')
        q2 = 'Q2', _('Second Quarter')
        q3 = 'Q3', _('Third Quarter')
        q4 = 'Q4', _('Fourth Quarter')
    deadline_quarter = models.CharField(choices=Quarter.choices, null=True,editable=False)
    deadline_month = models.IntegerField(editable=False, null=True)
    deadline_year = models.CharField(editable=False, null=True)
    # files = ArrayField(base_field=models.URLField(max_length=200), size=5)
    files = models.URLField(max_length=200, null=True, blank=True)
    def __str__(self) -> int:
        return self.note

    def is_approved(self) -> bool:
        return self.status != self.Status.P
    

    

class Objective(models.Model):
    id = models.BigAutoField(primary_key=True)
    objective_name = models.CharField(max_length=50,null=True)
    objective_content = models.TextField(max_length=200, default='To be filled')

    def __str__(self) -> str:
        return self.objective_name

class Formula(models.Model):
    id = models.BigAutoField(primary_key=True)
    formula_name = models.CharField(max_length=50)
    formula_value = models.SlugField(max_length=50)

    def __str__(self) -> str:
        return self.formula_name

class Source(models.Model): #nguoi giao
    id = models.BigAutoField(primary_key=True)
    source_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.source_name
  
class Log(models.Model):
    id = models.BigAutoField(primary_key=True)
    okr = models.ForeignKey(OKR, on_delete=models.CASCADE)
    note = models.TextField(max_length=200)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.updated_at

  