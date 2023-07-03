from rest_framework import serializers
from OKR.models import OKR, Log

# class OKRSerializers(serializers.ModelSerializer):
#     id = serializers
#     class Meta:
#         model = OKR
#         fields = ('id', 'objective_id', 'created_by', 'status', 'deadline')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ('okr_id', 'updated_by', 'updated_at')