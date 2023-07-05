from django.shortcuts import render
from django.http import Http404
from django.db import transaction
from OKR.models import OKR, Log, Source, Formula, Objective

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, viewsets


from . import serializers
# Create your views here.


@api_view(['GET'])
def home(request):
    return Response({'message': 'This is home'})

class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = serializers.LogSerializer

class OkrViewSet(viewsets.ModelViewSet):
    queryset = OKR.objects.all()
    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.OKRRetrieve
        if self.action == 'update' or self.action == 'partial_update':
            return serializers.OKRUpdate
        return serializers.OKRCreate

class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = serializers.SourceSerializer

class FormulaViewSet(viewsets.ModelViewSet):
    queryset = Formula.objects.all()
    serializer_class = serializers.FormulaSerializer

class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = serializers.ObjectiveSerializer

    # def get_serializer_class(self):
    #     print(self.action)
    #     if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         return serializers.ObjectiveDetail
    #     return serializers.ObjectiveSerializer