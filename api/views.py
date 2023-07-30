from django.shortcuts import render, redirect
from django.http import Http404
from django.db import transaction
from django.conf import settings
from sqlalchemy import create_engine
from OKR.models import OKR, Log, Source, Formula, Objective
from Employee.models import Employee, Team, Department

from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.decorators import  action
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status, permissions, mixins, viewsets
from rest_framework.authtoken.models import Token

from django_filters import rest_framework as filters
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.hashers import make_password
from django.db import connection


from OKR import serializers as okr_serializers
from Employee import serializers as employee_serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import pandas as pd
import pandas as pd
import os
import openpyxl

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
    serializer_class = employee_serializers.EmployeeSerializerExtended

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

# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/okr')

class ExcelView(APIView):
    permission_classes = [AllowAny,]
    def get(self,request):
        output_excel = 'F:/RnD/DjangoProject/employee_manager/outputExcel/KPI.xlsx'
        if os.path.exists(output_excel):
            os.remove(output_excel)
        nhanvien()
        
        #List all excel files in folder
        excel_folder= 'F:/RnD/DjangoProject/employee_manager/'
        excel_files = [os.path.join(root, file) for root, folder, files in os.walk(excel_folder) for file in files if file.endswith(".xlsx")]
        # print("gia tri excel:",excel_files)
        levels = {
                1: 'L1',
                2: 'L2',
                3: 'L3',
                -1: 'NoLevel',
                0: 'SVCNTS'
                }
        with pd.ExcelWriter(output_excel) as writer:
            for excel,(value,str) in zip(excel_files,levels.items()): #For each excel
                # sheet_name = pd.ExcelFile(excel).sheet_names[i] #Find the sheet name
                sheet_name=f'nhanvien{str}'
                # print("tên file excel:",sheet_name)
                df = pd.read_excel(excel, engine="openpyxl") #Create a dataframe
                df.to_excel(writer, sheet_name=sheet_name, index=False) #Write it to a sheet in the output excel

        wb_obj = openpyxl.load_workbook(output_excel)
        if os.path.exists(output_excel):
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=kpi.xlsx'
        wb_obj.save(response)
        return response


def nhanvien() -> None:
    # NO_LEVEL = -1, 'No Level'
    #     SVCNTS = 0, 'SVCNTS'
    #     L1 = 1, 'L1'
    #     L2 = 2, 'L2'
    #     L3 = 3, 'L3' 
    cursor= connection.cursor()
    cursor.execute(
            '''select   ee.id as employeecode,
                        full_name as fullName,
                        level,
                        ee.team_id as teamId,
                        name as teamName,
                        type,
                        oo.key_result_department as krDep,
                        oo.key_result_team as krTeam,
                        oo.key_result_personal as krPer,
                        ofo.formula_name as formulaName,
                        ofo.formula_value as formulaValue,
                        os.source_name as sourceName,
                        oo.regularity,
                        oo.unit,
                        oo.condition,
                        oo.weight,
                        oo.result,
                        oo.weight*oo.result as ratio,
                        oo.estimated,
                        oo.actual,
                        oo.note
                        FROM "Employee_employee" as ee,
                            "Employee_team" as et,
                            "OKR_okr" as oo,
                            "OKR_formula" as ofo,
                            "OKR_source" as os
                        where ee.team_id=et.team_id 
                            and ee.id=oo.user_id 
                            and oo.formula_id=ofo.id 
                            and oo.source_id=os.id'''

            )
    result = cursor.fetchall()
    dataframe= pd.DataFrame(result)
    # column_order = ['employeeId', 'fullName', 'level', 'teamId', 'teamName',
    #                 'Loại', 'KR phòng', 'KR team', 'KR cá nhân', 'Công thức tính', 
    #                 'Nguồn dữ liệu', 'Định kỳ tính', 'Đơn vị tính', 'Điều kiện', 'Norm',
    #                 '% Trọng số chỉ tiêu', 'Kết quả', 'Tỷ lệ', 'Tổng thời gian dự kiến/ ước tính công việc (giờ)',
    #                     'Tổng thời gian thực hiện công việc thực tế (giờ)', 'Note']
    dataframe.columns= ['employeeId', 'fullName', 'level', 'teamId', 'teamName',
                    'Loại', 'KR phòng', 'KR team', 'KR cá nhân', 'Công thức tính', 
                    'Nguồn dữ liệu', 'Định kỳ tính', 'Đơn vị tính', 'Điều kiện', 'Norm',
                    '% Trọng số chỉ tiêu', 'Kết quả', 'Tỷ lệ', 'Tổng thời gian dự kiến/ ước tính công việc (giờ)',
                        'Tổng thời gian thực hiện công việc thực tế (giờ)', 'Note']               
    # dataframe.rename(columns={"0": "employeeId"}, inplace=True)
    # dataframe.rename(columns={"1": "fullName"}, inplace=True)
    # dataframe.rename(columns={"2": "level"}, inplace=True)
    # dataframe.rename(columns={"3": "teamId"}, inplace=True)
    # dataframe.rename(columns={"4": "teamName"}, inplace=True)
    # dataframe.rename(columns={"5": "Loại"}, inplace=True)
    # dataframe.rename(columns={"6": "KR phòng"}, inplace=True)
    # dataframe.rename(columns={"7": "KR team"}, inplace=True)
    # dataframe.rename(columns={"8": "KR cá nhân"}, inplace=True)
    # dataframe.rename(columns={"9": "Công thức tính"}, inplace=True)
    # dataframe.rename(columns={"10": "Nguồn dữ liệu"}, inplace=True)
    # dataframe.rename(columns={"11": "Định kỳ tính"}, inplace=True)
    # dataframe.rename(columns={"12": "Đơn vị tính"}, inplace=True)
    # dataframe.rename(columns={"13": "Điều kiện"}, inplace=True)
    # dataframe.rename(columns={"14": "Norm"}, inplace=True)
    # dataframe.rename(columns={"15": "% Trọng số chỉ tiêu"}, inplace=True)
    # dataframe.rename(columns={"16": "Kết quả"}, inplace=True)
    # dataframe.rename(columns={"17": "Tỷ lệ"}, inplace=True)
    # dataframe.rename(columns={"18": "Tổng thời gian dự kiến/ ước tính công việc (giờ)"}, inplace=True)
    # dataframe.rename(columns={"19": "Tổng thời gian thực hiện công việc thực tế (giờ)"}, inplace=True)
    # dataframe.rename(columns={"20": "Note"}, inplace=True)

    # print("gia tri cua dataframe:",dataframe)

    nhanvien_df = dataframe
    # print(nhanvien_df.dtypes)
    # nhanvien_df.sort_values('employeeId', inplace=True)
    nhanvien_df.fillna('No data', inplace=True)
    # nhanvien_df.set_index(['id', 'full_name', 'department_name', 'team_name', 'type', 'okr_kpi_id', 'objective_name', 'type'], inplace=True)
    
    levels = {
        1: 'L1',
        2: 'L2',
        3: 'L3',
        -1: 'NoLevel',
        0: 'SVCNTS'
    }
    for value, str in levels.items():
        temp_df = nhanvien_df.loc[nhanvien_df['level']==value]
        temp_df.drop(columns=['level'], axis=1)
        if os.path.exists(f"F:/RnD/DjangoProject/employee_manager/nhanvien{str}.xlsx"):
            os.remove(f"F:/RnD/DjangoProject/employee_manager/nhanvien{str}.xlsx")
        temp_df.to_excel(f'nhanvien{str}.xlsx')


def department() -> None:
    column_order = ['okr_kpi_id', 'full_name', 'department_name', 'type',
                    'objective_name', 'kr_phong', 'kr_team', 'kr_personal', 'unit',
                    'condition', 'norm', 'weight', 'ratio',  'result', 'status', 'deadline'] 

    department_df = full_df[column_order]
    department_df['deadline'] = department_df['deadline'].dt.tz_localize(None)

    def do_nothing(x):
        return x

    # department_df.set_index(['department_name', 'type'], inplace=True)
    # print(department_df)
    department_df = department_df.fillna('No data')
    # department_df = department_df.groupby(['department_name', 'type', 'okr_kpi_id', 'objective_name', 'weight']).agg({
    #     'full_name': do_nothing, # lambda x: ', '.join(x),
    #     'kr_phong': do_nothing,
    #     'kr_team': do_nothing,
    #     'unit': do_nothing,
    #     'condition': do_nothing,
    #     'norm': do_nothing,
    #     'weight': do_nothing,
    #     'ratio': do_nothing,
    #     'result': do_nothing,
    #     'deadline': do_nothing,
    # })
    department_df = department_df.set_index(['department_name', 'type', 'okr_kpi_id', 'objective_name', 'kr_phong', 'kr_team'])


    department_df.to_excel('department.xlsx')

def okr_quarter() -> None:

    

    quarter_df = full_df.loc[full_df['type'] == 'okr']
    quarter_df['deadline'] = quarter_df['deadline'].dt.tz_localize(None)
    column_order = ['okr_kpi_id', 'id', 'full_name', 'department_name', 'team_name',
                    'objective_name', 'kr_phong', 'regularity', 'unit', 'condition',
                    'result', 'deadline', 'status', 'files']
    quarter_df = quarter_df[column_order]
    quarter_df = quarter_df.fillna('No data')
    quarter_df = quarter_df.set_index(['department_name', 'team_name', 'id', 'full_name', 'okr_kpi_id', 'objective_name'])
    quarter_df.to_excel('quarter.xlsx')