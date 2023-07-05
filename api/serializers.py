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

class OKRCreate(serializers.ModelSerializer):
    objective = ObjectiveSerializer()
    formula = FormulaSerializer()
    source = SourceSerializer()

    class Meta:
        model = models.OKR
        exclude = ['ratio', 'status', 'files']
class OKRRetrieve(serializers.ModelSerializer):
    class Meta:
        model = models.OKR
        fields = '__all__'
class OKRUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.OKR
        exclude = ['source', 'regularity', 'ratio', 'created_by']


# class ObjectiveDetail(serializers.ModelSerializer):
#     okrs = OKRSerializer()
#     class Meta:
#         model = models.Objective
#         fields = '__all__'
    # def get_okrs(self, obj):
    #     selected_okrs = models.OKR.objects.filter(
    #         okr__objective=obj).distinct()
    #     return OKRSerializer(selected_okrs, many=True).data
