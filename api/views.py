from django.shortcuts import render
from django.http import Http404
from django.db import transaction

from OKR.models import OKR, Log, Source, Formula, Objective
from Employee.models import Employee, Team, Department

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, viewsets

from django_filters import rest_framework as filters

from OKR import serializers as okr_serializers
from Employee import serializers as employee_serializers
# Create your views here.

# OKR Viewset
class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = okr_serializers.LogSerializer
class OkrViewSet(viewsets.ModelViewSet):
    queryset = OKR.objects.all()
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('created_by', 'status', 'deadline_month', 'deadline_quarter', 'deadline_year')
    @action(detail=False, methods=['post', 'get'], url_path='no-objective', url_name='no_objective')
    def no_objective_create(self, request, *args, **kwargs):
        okr_data = request.data
        new_okr = OKR.objects.create(**okr_data)
        new_okr.save()
        serializer = okr_serializers.OKRCreate(new_okr)
        return Response(serializer.data)
    def get_serializer_class(self):
        print(self.action)
        if self.action == 'no_objective':
            return okr_serializers.OKRCreate
        if self.action == 'list' or self.action == 'retrieve':
            return okr_serializers.OKRRetrieve
        if self.action == 'update' or self.action == 'partial_update':
            return okr_serializers.OKRUpdate
        return okr_serializers.OKRFullCreate
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = okr_serializers.SourceSerializer
class FormulaViewSet(viewsets.ModelViewSet):
    queryset = Formula.objects.all()
    serializer_class = okr_serializers.FormulaSerializer
class ObjectiveViewSet(viewsets.ModelViewSet):
    queryset = Objective.objects.all()
    serializer_class = okr_serializers.ObjectiveSerializer
    # def get_serializer_class(self):
    #     print(self.action)
    #     if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         return okr_serializers.ObjectiveDetail
    #     return okr_serializers.ObjectiveSerializer


# Employee Viewsets
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = employee_serializers.EmployeeSerializer
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return employee_serializers.TeamSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return employee_serializers.TeamUpdate
        return employee_serializers.TeamCreate
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return employee_serializers.DepartmentSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return employee_serializers.DepartmentUpdate
        return employee_serializers.DepartmentCreate
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
