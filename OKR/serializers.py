from rest_framework import serializers
from . import models



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

class OKRFullCreate(serializers.ModelSerializer):
    objective = ObjectiveSerializer()
    class Meta:
        model = models.OKR
        exclude = ['ratio', 'status', 'files', 'result', 'regularity', 'created_by', 'updated_by']
        # fields = '__all__'

    def create(self, validated_data):
        objective_data = validated_data.pop('objective')
        objective = models.Objective.objects.create(**objective_data)
        okr = models.OKR.objects.create(objective=objective, **validated_data) 
        return okr
    
class OKRCreate(serializers.ModelSerializer):

    class Meta:
        model = models.OKR
        exclude = ['ratio', 'status', 'files', 'result', 'regularity', 'created_by','updated_by']
        
class OKRRetrieve(serializers.ModelSerializer):
    class Meta:
        model = models.OKR
        fields = '__all__'
class OKRUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.OKR
        exclude = ['objective', 'source', 'regularity', 'ratio', 'created_by', 'updated_by']




# class ObjectiveDetail(serializers.ModelSerializer):
#     okrs = OKRSerializer()
#     class Meta:
#         model = models.Objective
#         fields = '__all__'
    # def get_okrs(self, obj):
    #     selected_okrs = models.OKR.objects.filter(
    #         okr__objective=obj).distinct()
    #     return OKRSerializer(selected_okrs, many=True).data
