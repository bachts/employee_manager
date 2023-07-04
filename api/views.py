from django.shortcuts import render
from django.http import Http404
from OKR.models import OKR, Log, Objective, Source, KeyResult, Formula

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, mixins
from rest_framework.views import APIView


from .serializers import  LogSerializer, ObjectiveSerializer, KeyResultSerializer, OKRSerializers, FormulaSerializer, SourceSerializer
# Create your views here.


# @api_view(['GET'])
# def get_okr(request):
    
#     if request.query_params:
#         queryset = OKR.objects.filter(**request.query_params.dict())
#     else: 
#         queryset = OKR.objects.all()

#     if queryset:
#         serializer = OKRSerializers(queryset, many=True)
#         return Response(serializer.data)
#     else: 
#         return Response(status=status.HTTP_404_NOT_FOUND)
class LogAPI(APIView):
    
    def get_object(self, pk):
        try:
            return Log.objects.get(pk=pk)
        except Log.DoesNotExist:
            raise Http404
    #RETRIEVE ALL
    def get_all(self, request, format=None):
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)
    
    #CREATE
    def post(self, request, format=None):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #RETRIEVE BY PK
    def get(self, response, pk, format=None):
        log = self.get_object(pk)
        serializer = LogSerializer(log)
        return Response(serializer.data)
    
    #UPDATE
    def put(self, request, pk, format=None):
        log = self.get_object(pk)
        serializer = LogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #DELETE
    def delete(self, request, pk, format=None):
        log = self.get_object(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ObjectiveAPI(APIView):
    
    def get_object(self, pk):
        try:
            return Objective.objects.get(pk=pk)
        except Objective.DoesNotExist:
            raise Http404
    # RETRIEVE ALL
    def get_all(self, request, format=None):
        objectives = Objective.objects.all()
        serializer =  ObjectiveSerializer(objectives, many=True)
        return Response(objectives.data)
    # CREATE
    def post(self, request, format=None):
        serializer = ObjectiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #RETRIEVE
    def get(self, response, pk, format=None):
        objective = self.get_object(pk)
        serializer = ObjectiveSerializer(objective)
        return Response(serializer.data)
    #UPDATE
    def put(self, request, pk, format=None):
        objective = self.get_object(pk)
        serializer = ObjectiveSerializer(objective, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    def delete(self, request, pk, format=None):
        objective = self.get_object(pk)
        objective.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SourceAPI(APIView):
    
    def get_object(self, pk):
        try:
            return Source.objects.get(pk=pk)
        except Source.DoesNotExist:
            raise Http404
    # RETRIEVE ALL
    def get_all(self, request, format=None):
        sources = Objective.objects.all()
        serializer =  SourceSerializer(sources, many=True)
        return Response(sources.data)
    # CREATE
    def post(self, request, format=None):
        serializer = ObjectiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #RETRIEVE
    def get(self, response, pk, format=None):
        source = self.get_object(pk)
        serializer = SourceSerializer(source)
        return Response(serializer.data)
    #UPDATE
    def put(self, request, pk, format=None):
        source = self.get_object(pk)
        serializer = ObjectiveSerializer(source, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    def delete(self, request, pk, format=None):
        source = self.get_object(pk)
        source.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
