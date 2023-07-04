from rest_framework import serializers
from OKR import models

class OKRSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.OKR
        fields = ('id', 'objective_id', 'created_by', 'status', 'deadline')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Log
        fields = ('okr_id', 'updated_by', 'updated_at')

class KeyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KeyResult
        fields = ('id', 'okr_id', 'key_result_name')

class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Objective
        fields = ('id', 'objective_name')

class FormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Formula
        fields = ('id', 'formula_name', 'formula_value')

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Source
        fields = ('id', 'source_name')
