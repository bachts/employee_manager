from django.shortcuts import render
from django.http import Http404
from OKR.models import OKR, Log

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, mixins
from rest_framework.views import APIView


from .serializers import  LogSerializer#, OKRSerializers
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
class LogList(APIView):
    
    def get(self, request, format=None):
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = LogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Log.objects.get(pk=pk)
        except Log.DoesNotExist:
            raise Http404
        
    def get(self, response, pk, format=None):
        log = self.get_object(pk)
        serializer = LogSerializer(log)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        log = self.get_object(pk)
        serializer = LogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        log = self.get_object(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
