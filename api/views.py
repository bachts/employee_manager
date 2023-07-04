from django.shortcuts import render
from django.http import Http404
from OKR.models import OKR, Log, KeyResult, Source, Formula, Objective

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, viewsets


from . import serializers
# Create your views here.


@api_view(['GET'])
def home(request):
    return Response({'message': 'This is home'})

class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = serializers.LogSerializer

class KeyResultViewSet(viewsets.ModelViewSet):
    queryset = KeyResult.objects.all()
    serializer_class = serializers.KeyResultSerializer

class OkrViewSet(viewsets.ModelViewSet):
    queryset = OKR.objects.all()
    serializer_class = serializers.OKRSerializers

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = serializers.SourceSerializer

class FormulaViewSet(viewsets.ModelViewSet):
    queryset = Formula.objects.all()
    serializer_class = serializers.FormulaSerializer

class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = serializers.ObjectiveSerializer