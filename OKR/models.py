from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
# Create your models here.
class OKR(models.Model):
    id = models.BigAutoField(primary_key=True)
    objective = models.ForeignKey('Objective', null=True, on_delete=models.SET_NULL)

    key_result_1 = models.TextField(max_length=200, blank=False, null=True)
    key_result_2 = models.TextField(max_length=200, blank=False, null=True)
    key_result_3 = models.TextField(max_length=200, blank=False, null=True)

    formula = models.ForeignKey('Formula', null=True, on_delete=models.SET_NULL)
    source = models.ForeignKey('Source', null=True, on_delete= models.SET_NULL)
    
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
                                 blank=False,
                                 default=None) #ket qua tung phan

    ratio = models.IntegerField(validators=[MaxValueValidator(100),
                                            MinValueValidator(0)],
                                default=None) #weight * result
    
    class Status(models.TextChoices):
        P = 'P', _('Pending Approval')
        INP = 'INP', _('In Progress')
        OK = 'S', _('Satisfactory')
        NOK = 'NS', _('Not Satisfactory')
        
    status = models.CharField(choices=Status.choices, 
                              default=Status.P)

    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30, default=None)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    deadline = models.DateTimeField()
    # files = ArrayField(base_field=models.URLField(max_length=200), size=5)
    files = models.URLField(max_length=200)
    def __str__(self) -> int:
        return self.id

    def is_approved(self) -> bool:
        return self.status != self.Status.P
    

class Objective(models.Model):
    id = models.BigAutoField(primary_key=True)
    objective_name = models.CharField(max_length=50, null=False)
    objective_content = models.TextField(max_length=200)

    def __str__(self) -> str:
        return self.objective_name

class Formula(models.Model):
    id = models.BigAutoField(primary_key=True)
    formula_name = models.CharField(max_length=50, null=False)
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
    okr_id = models.ForeignKey(OKR, on_delete=models.CASCADE)
    note = models.TextField(max_length=200)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.updated_at

  