from django.contrib import admin

# Register your models here.
from .models import MyUser

@admin.register(MyUser)
class MyUser(admin.ModelAdmin):
    pass