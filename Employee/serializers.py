from rest_framework import serializers
from . import models

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = '__all__'
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'

class TeamCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        exclude = ['updated_by', 'created_by']
class TeamUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        exclude = ['created_by', 'updated_by']


class DepartmentCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        exclude = ['updated_by', 'created_by']
class DepartmentUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        exclude = ['created_by', 'updated_by']