from rest_framework import serializers
from OKR.models import OKR, Log, Objective, Formula, Source, KeyResult

class OKRSerializers(serializers.ModelSerializer):
    class Meta:
        model = OKR
        fields = ('id', 'objective_id', 'created_by', 'status', 'deadline')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('id', 'okr_id', 'updated_by', 'updated_at')

class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objective
        fields = ('id', 'objective_name', 'objective_content')

class FormulaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Formula
        fields = ('id', 'formula_name', 'formula_value')

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formula
        fields = ('id', 'source_name')

class KeyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResult
        fields = ('id', 'okr_id', 'key_result_name')