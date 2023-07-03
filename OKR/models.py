from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
# Create your models here.
class OKR(models.Model):
    id = models.BigAutoField(primary_key=True)
    objective_id = models.ForeignKey('Objective', on_delete=models.CASCADE)

    key_result_name = models.CharField(max_length=50)
    key_result_content = models.TextField(max_length=200)

    formula_id = models.ForeignKey('Formula', on_delete=models.CASCADE)
    source_id = models.ForeignKey('Source', on_delete=models.CASCADE)
    
    class Types(models.TextChoices):
        OKR = 'OKR', _('OKR')
        KPI = 'KPI', _('KPI')
    type = models.CharField(choices=Types.choices) #OKR hay KPI

    class Regularity(models.TextChoices):
        MONTHLY = 'MO', _('MONTHLY')
        QUARTERLY = 'QUAR', _('QUARTERLY')
    regularity = models.CharField(choices=Regularity.choices) #quarterly hay monthly

    unit = models.CharField(max_length=20) # don vi

    condition = models.IntegerField() #pass condition
    norm = models.IntegerField() #max value
    weight = models.IntegerField() #trong so
    result = models.IntegerField() #ket qua tung phan

    ratio = models.IntegerField() #weight * result

    class Status(models.TextChoices):
        OK = 'S', _('Satisfactory')
        NOK = 'NS', _('Not Satisfactory')
        INP = 'INP', _('In Progress')
    status = models.CharField(choices=Status.choices)

    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    deadline = models.DateTimeField()
    files = ArrayField(base_field=models.URLField(max_length=200), size=10)

    def __str__(self) -> int:
        return self.id



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
        return self.formula_value

class Source(models.Model):
    id = models.BigAutoField(primary_key=True)
    source_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.source_name
    
class KeyResult(models.Model):
    id = models.BigAutoField(primary_key=True)
    okr_id = models.ForeignKey('OKR', on_delete=models.CASCADE)
    key_result_name = models.CharField(max_length=50)
    key_result_content = models.TextField(max_length=200)

    def __str__(self) -> str:
        return self.key_result_name
  
class Log(models.Model):
    id = models.BigAutoField(primary_key=True)
    okr_id = models.ForeignKey('OKR', on_delete=models.CASCADE)
    note = models.TextField(max_length=200)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.updated_at

  