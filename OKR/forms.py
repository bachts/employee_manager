from django import forms
from .models import OKR, Objective, Formula, Source, Log


class OkrForm(forms.Form):
    
    objective_name = forms.CharField(max_length=50)
    objective_content = forms.CharField(max_length=200)
    formula_name = forms.CharField(max_length=50)
    formula_value = forms.CharField(max_length=50)
    source_name = forms.CharField(max_length=50)

    key_result_name = forms.CharField(max_length=50)
    key_result_content = forms.CharField(max_length=200)
    
    type = forms.ChoiceField(choices=[('OKR', 'OKR'),
                                      ('KPI', 'KPI')])
    regularity = forms.ChoiceField(choices=[('MO', 'MONTHLY'),
                                            ('QUAR', 'QUARTERLY')])
    unit = forms.CharField(max_length=20)

    condition = forms.IntegerField()
    norm = forms.IntegerField()
    weight = forms.IntegerField()
    result = forms.IntegerField()
    ratio = forms.IntegerField()

    status = forms.ChoiceField(choices=[('P', 'Pending Approval'),
                                        ('INP', 'In Progress'),
                                        ('NS', 'Not Satisfactory'),
                                        ('S', 'Satisfactory')])
    deadline = forms.DateTimeField()
    files = forms.URLField(max_length=200)
    note = forms.CharField(empty_value='no notes')

OkrFormSet = forms.formset_factory(OkrForm)


