from django.contrib import admin

# Register your models here.
from .models import Employee, Team, Department

@admin.register(Employee, Team, Department)
class Employee(admin.ModelAdmin):
    pass