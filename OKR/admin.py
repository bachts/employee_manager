from django.contrib import admin

from .models import OKR, Log, Objective, Source, Formula
# Register your models here.
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_at'

@admin.register(Objective)
class Result(admin.ModelAdmin):
    pass

@admin.register(OKR, Formula, Source)
class OKR(admin.ModelAdmin):
    pass
