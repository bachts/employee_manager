from rest_framework import serializers
from OKR import models



class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = '__all__'
class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Objective
        fields = '__all__'
class FormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Formula
        fields = '__all__'
class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = '__all__'

class OKRSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OKR
        fields = '__all__'
