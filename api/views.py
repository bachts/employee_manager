from django.shortcuts import render, redirect
from django.http import Http404
from django.db import transaction
from django.conf import settings

from OKR.models import OKR, Log, Source, Formula, Objective
from Employee.models import Employee, Team, Department

from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.decorators import  action
from rest_framework.response import Response
from rest_framework import status, permissions, mixins, viewsets
from rest_framework.authtoken.models import Token

from django_filters import rest_framework as filters
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.hashers import make_password


from OKR import serializers as okr_serializers
from Employee import serializers as employee_serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Create your views here.

# OKR Viewset
class LogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = okr_serializers.LogSerializer
class OkrViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    def get_queryset(self): # HIEN OKR DOI VOI USER CO OKR DO
        user = self.request.user
        if user.is_superuser:
            return OKR.objects.all()
        else:
            return OKR.objects.filter(user__id=user.id) 
    #TODO: CHO PHEP EDIT OKR VOI NGUOI MANAGE USER DO
        
class SourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Source.objects.all()
    serializer_class = okr_serializers.SourceSerializer
class FormulaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Formula.objects.all()
    serializer_class = okr_serializers.FormulaSerializer
class ObjectiveViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Objective.objects.all()
    serializer_class = okr_serializers.ObjectiveSerializer
    # def get_serializer_class(self):
    #     print(self.action)
    #     if self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         return okr_serializers.ObjectiveDetail
    #     return okr_serializers.ObjectiveSerializer



# Employee Viewsets

    
    
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
    def get_queryset(self): # XEM DEPARTMENT MINH O TRONG
        user = self.request.user
        if user.is_superuser:
            return Team.objects.all()
        if user.get_team():
            teams = Team.objects.get(pk=user.team.id)  
            return Team.objects.filter(department__department_id=teams)
        else:
            return Department.objects.none()
        
class DepartmentViewSet(viewsets.ModelViewSet):
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
    def get_queryset(self): # XEM DEPARTMENT MINH O TRONG
        user = self.request.user
        if user.is_superuser:
            return Department.objects.all()
        if user.get_department():
            departments = Department.objects.get(pk=user.department.id)  
            return Department.objects.filter(department__department_id=departments)
        else:
            return Department.objects.none()
    
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = employee_serializers.EmployeeSerializer

    #TODO: XEM EMPLOYEE MA MINH QUAN LY
    #TODO: LIMIT ACCESS EMPLOYEE DOI VOI MANAGER/SUPERUSER/BAN THAN



#TODO: TAO LOGOUT ENDPOINT

        

class RegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = employee_serializers.RegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])

        user = serializer.save()

        return Response({'message': 'registration ok',
                         'status': status.HTTP_201_CREATED})

class LoginView(APIView):
    permission_classes = [AllowAny,]
    serializer_class = employee_serializers.LoginSerializer
    # print("day la izerwtwe:")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print("day la serializer:",serializer)
        user = authenticate(request, 
                            username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])
        
        if user:
            refresh = TokenObtainPairSerializer.get_token(user)
            data = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
            }
            login(request,user=user)
            # print("day la user:",data)
            return Response(data,status=status.HTTP_200_OK)
        
        return Response({
            'error_message': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    serializer_class = employee_serializers.LogoutSerializer

    def post(self,request):
            print("gia tri cua session",request.get_authenticate_header)
            logout(request)
            print("day la user:",request)
            return Response(status=status.HTTP_200_OK)